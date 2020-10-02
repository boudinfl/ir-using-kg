# -*- coding: utf-8 -*-

"""Convert NTCIR formatted files to TREC format."""

import re
import json
import gzip
import argparse
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import word_tokenize
from collections import defaultdict


def punctuation_mark_cleanser(s):
    """Add spacing in muddled sentences."""
    s = re.sub(r'([A-Za-z])([\.\?\!\(\)])([A-Za-z\(\)])', r'\g<1>\g<2> \g<3>', s)
    return s


def tokenize(s):
    """Tokenize an input text."""
    return word_tokenize(s)


def lowercase_and_stem(_words):
    """lowercase and stem sequence of words."""
    return " ".join([PorterStemmer().stem(w.lower()) for w in _words])


def contains(subseq, inseq):
    return any(inseq[pos:pos + len(subseq)] == subseq for pos in range(0, len(inseq) - len(subseq) + 1))


# get the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--input",
                    help="input file in NTCIR format.",
                    type=str)

parser.add_argument("--output",
                    help="output file.",
                    type=str)

args = parser.parse_args()


# looping through the files
with gzip.open(args.input, 'rt') as f:
    is_in_document = False
    doc_id = None

    # initialize gold annotation sub-containers
    all_kps = defaultdict(list)
    present_kps = defaultdict(list)
    absent_kps = defaultdict(list)
    absent_kps_case_1 = defaultdict(list)
    absent_kps_case_2 = defaultdict(list)
    absent_kps_case_3 = defaultdict(list)
    present_and_case_1_kps = defaultdict(list)
    absent_case_2_and_3_kps = defaultdict(list)

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
            abstract = punctuation_mark_cleanser(abstract)

        # keywords
        elif line.startswith('<KYWE'):
            keywords = BeautifulSoup(line.strip(), 'html.parser').text

            keywords = re.split(" / |//|;|,", keywords)
            keywords = [kp.strip() for kp in keywords]

            # special case of " , " separator
            if len(keywords) < 2:
                print("COCOCOCOCOCOOC", keywords)

            if any(['/' in kp for kp in keywords]):
                print(keywords)

            tok_kw = [tokenize(kp) for kp in keywords]
            pp_kw = [lowercase_and_stem(kp) for kp in tok_kw]

            pp_ti = lowercase_and_stem(tokenize(title))
            pp_ab = lowercase_and_stem(tokenize(abstract))

            if not len(pp_kw):
                print("ERROR, kps no valid: {} {}".format(pp_kw, keywords))

            # loop through the keyphrases
            for j, kp in enumerate(pp_kw):

                # keyphrase is present
                if contains(kp.split(), pp_ti.split()) or \
                   contains(kp.split(), pp_ab.split()):
                    present_kps[doc_id].append([keywords[j]])
                    present_and_case_1_kps[doc_id].append([keywords[j]])
                    all_kps[doc_id].append([keywords[j]])

                # keyphrase is absent
                else:
                    absent_kps[doc_id].append([keywords[j]])
                    all_kps[doc_id].append([keywords[j]])

                    nb_present_words = 0
                    words = kp.split()
                    for word in words:
                        if word in pp_ti or word in pp_ab:
                            nb_present_words += 1

                    # Case 1: every word but not the sequence
                    if nb_present_words == len(words):
                        absent_kps_case_1[doc_id].append([keywords[j]])
                        present_and_case_1_kps[doc_id].append([keywords[j]])

                    # Case 2: some words appear
                    elif nb_present_words > 0:
                        absent_kps_case_2[doc_id].append([keywords[j]])
                        absent_case_2_and_3_kps[doc_id].append([keywords[j]])

                    # Case 3: no word appears
                    else:
                        absent_kps_case_3[doc_id].append([keywords[j]])
                        absent_case_2_and_3_kps[doc_id].append([keywords[j]])

        elif line.startswith('</REC>'):
            if not is_in_document:
                print("ERROR, document no valid at line {}".format(i))
            is_in_document = False
            doc_id = None
            if len(present_kps) % 1000 == 0:
                print("INFO, {} documents processed".format(len(present_kps)))

    with gzip.open(args.output + '.all.json.gz', 'wt') as o:
        o.write(json.dumps(all_kps, indent=4, sort_keys=True))

    with gzip.open(args.output + '.pres.json.gz', 'wt') as o:
        o.write(json.dumps(present_kps, indent=4, sort_keys=True))

    with gzip.open(args.output + '.abs.json.gz', 'wt') as o:
        o.write(json.dumps(absent_kps, indent=4, sort_keys=True))

    with gzip.open(args.output + '.abs_c1.json.gz', 'wt') as o:
        o.write(json.dumps(absent_kps_case_1, indent=4, sort_keys=True))

    with gzip.open(args.output + '.abs_c2.json.gz', 'wt') as o:
        o.write(json.dumps(absent_kps_case_2, indent=4, sort_keys=True))

    with gzip.open(args.output + '.abs_c3.json.gz', 'wt') as o:
        o.write(json.dumps(absent_kps_case_3, indent=4, sort_keys=True))

    with gzip.open(args.output + '.pres+abs_c1.json.gz', 'wt') as o:
        o.write(json.dumps(present_and_case_1_kps, indent=4, sort_keys=True))

    with gzip.open(args.output + '.abs_c2+abs_c3.json.gz', 'wt') as o:
        o.write(json.dumps(absent_case_2_and_3_kps, indent=4, sort_keys=True))
