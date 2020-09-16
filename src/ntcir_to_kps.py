# -*- coding: utf-8 -*-

"""Convert NTCIR formatted files to TREC format."""

import os
import json
import gzip
import argparse
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

import spacy
nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser", "ner"])


def tokenize(s):
    """tokenize an input text."""
    doc = nlp(s)
    return [word.text for word in doc]


def lowercase_and_stem(_words):
    """lowercase and stem sequence of words."""
    return " ".join([PorterStemmer().stem(w.lower()) for w in _words])


def pre_process_text(s):
    """lowercase, tokenize and stem text."""
    doc = nlp(s)
    words = [word.text for word in doc]
    return " ".join([PorterStemmer().stem(w.lower()) for w in words])


# get the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--input",
                    help="input file in NTCIR format.",
                    type=str)

parser.add_argument("--output",
                    help="output file.",
                    type=str)

parser.add_argument('--present',
                    action='store_true',
                    help='keep the present keywords.')

parser.add_argument('--absent',
                    action='store_true',
                    help='keep the absent keywords.')

parser.add_argument('--absent_case1',
                    action='store_true',
                    help='keep the absent keywords.')

parser.add_argument('--absent_case2',
                    action='store_true',
                    help='keep the absent keywords.')

parser.add_argument('--absent_case3',
                    action='store_true',
                    help='keep the absent keywords.')

parser.add_argument('--present_words',
                    action='store_true',
                    help='keep the present words from keyphrases.')

parser.add_argument('--absent_words',
                    action='store_true',
                    help='keep the present words from keyphrases.')

args = parser.parse_args()

# creating output path if it does not exist
output_dir = os.path.split(args.output)[0]
if not os.path.isdir(output_dir):
    os.makedirs(output_dir, exist_ok=True)

# skip if file already exists
#if os.path.isfile(args.output):
#    print("file {} already exists - stopping now".format(args.output))
#    sys.exit(0)

# looping through the files
with gzip.open(args.input, 'rt') as f:
    with gzip.open(args.output, 'wt') as o:
        is_in_document = False
        doc_id = None
        keyphrases = {}
        for i, line in enumerate(f):
            if line.startswith('<REC>'):
                is_in_document = True

            # document identifier
            elif line.startswith('<ACCN'):
                doc_id = BeautifulSoup(line.strip(), 'html.parser').text

            # title
            elif line.startswith('<TITE') or line.startswith('<PJNE'):
                title = BeautifulSoup(line.strip(), 'html.parser').text

            # abstract
            elif line.startswith('<ABSE'):
                abstract = BeautifulSoup(line.strip(), 'html.parser').text

            # keywords
            elif line.startswith('<KYWE'):
                keywords = BeautifulSoup(line.strip(), 'html.parser').text
                keywords = [kp.strip() for kp in keywords.split('//')]

                # special case of " , " separator
                if len(keywords) < 2:
                    if "," in keywords[0]:
                        keywords = keywords[0].split(",")
                    if ' / ' in keywords[0]:
                        keywords = keywords[0].split(" / ")
                    if ' ; ' in keywords[0]:
                        keywords = keywords[0].split(" ; ")

                tok_kw = [tokenize(kp) for kp in keywords]
                pp_kw =  [lowercase_and_stem(kp) for kp in tok_kw]


                pp_keywords = [pre_process_text(kp) for kp in keywords]
                pp_title = pre_process_text(title)
                pp_abstract = pre_process_text(abstract)

                if len(pp_kw) < 2:
                    print("ERROR, kps no valid: {} {}".format(pp_kw, keywords))

                # loop through the keyphrases
                gold = []
                for i, kp in enumerate(pp_kw):

                    # keyphrase is present
                    if kp in pp_title or kp in pp_abstract:
                        if args.present:
                            gold.append([keywords[i]])

                    # else keyphrase is absent
                    else:
                        if args.absent:
                            gold.append([keywords[i]])

                        else:

                            nb_present_words = 0
                            words = kp.split()
                            for word in words:
                                if word in pp_title or word in pp_abstract:
                                    nb_present_words += 1
                                elif args.absent_words:
                                    gold.append([keywords[i]])

                            # Case 1: every word but not the sequence
                            if nb_present_words == len(words):
                                if args.absent_case1:
                                    gold.append([keywords[i]])

                            # Case 2: some words appear
                            elif nb_present_words > 0:
                                if args.absent_case2:
                                    gold.append([keywords[i]])

                            # Case 3: no word appears
                            elif args.absent_case3:
                                gold.append([keywords[i]])

                keyphrases[doc_id] = gold

            elif line.startswith('</REC>'):
                if not is_in_document:
                    print("ERROR, document no valid at line {}".format(i))
                is_in_document = False
                doc_id = None
                if len(keyphrases) % 1000 == 0:
                    print("INFO, {} documents processed".format(len(keyphrases)))

            if len(keyphrases) > 4:
                break

        o.write(json.dumps(keyphrases, indent=4, sort_keys=True))
