# -*- coding: utf-8 -*-

"""Convert NTCIR formatted files to TREC format."""

import os
import sys
import json
import gzip
import argparse
from bs4 import BeautifulSoup

# get the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--input",
                    help="input file in NTCIR format.",
                    type=str)

parser.add_argument("--output",
                    help="output directory in TREC format.",
                    type=str)

parser.add_argument('--include_keywords',
                    action='store_true',
                    help='keep the author keywords.')

parser.add_argument('--path_to_keyphrases',
                    help='path to the (json formatted) keyphrases.',
                    type=str,
                    default=None)

parser.add_argument('--nb_keyphrases',
                    type=int,
                    help='top-n keyphrases to include.',
                    default=5)

args = parser.parse_args()

# creating output path if it does not exist
output_dir = os.path.split(args.output)[0]
if not os.path.isdir(output_dir):
    os.makedirs(output_dir, exist_ok=True)

# skip if file already exists
if os.path.isfile(args.output):
    print("file {} already exists - stopping now".format(args.output))
    sys.exit(0)

# loading keyphrases if provided
if args.path_to_keyphrases:
    with gzip.open(args.path_to_keyphrases, "rt") as f:
        keyphrases = json.loads(f.read())
        print("{} docids loaded for keyphrases".format(len(keyphrases)))

# looping through the files
with gzip.open(args.input, 'rt') as f:
    with gzip.open(args.output, 'wt') as o:
        is_in_document = False
        doc_id = None
        for i, line in enumerate(f):
            if line.startswith('<REC>'):
                o.write("<DOC>\n")
                is_in_document = True

            # document identifier
            elif line.startswith('<ACCN'):
                doc_id = BeautifulSoup(line.strip(), 'html.parser').text
                o.write("<DOCNO>{}</DOCNO>\n".format(doc_id))

            # title
            elif line.startswith('<TITE') or line.startswith('<PJNE'):
                title = BeautifulSoup(line.strip(), 'html.parser').text
                o.write("<TITLE>{}</TITLE>\n".format(title.strip()))

            # abstract
            elif line.startswith('<ABSE'):
                abstract = BeautifulSoup(line.strip(), 'html.parser').text
                o.write("<TEXT>{}</TEXT>\n".format(abstract.strip()))

            # keywords
            elif args.include_keywords and line.startswith('<KYWE'):
                keywords = BeautifulSoup(line.strip(), 'html.parser').text
                # keywords = re.sub('\s+', " ", keywords.replace("//", " "))
                o.write("<HEAD>{}</HEAD>\n".format(keywords.strip()))

            elif line.startswith('</REC>'):
                if not is_in_document:
                    print("ERROR, document no valid at line {}".format(i))
                if args.path_to_keyphrases and doc_id in keyphrases:
                    kps = keyphrases[doc_id]
                    kps = kps[:min(len(kps), args.nb_keyphrases)]
                    kps = [k[0] for k in kps]
                    o.write("<HEAD>{}</HEAD>\n".format(' // '.join(kps)))
                o.write("</DOC>\n\n")
                is_in_document = False
                doc_id = None
