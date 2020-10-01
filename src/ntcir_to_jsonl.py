# -*- coding: utf-8 -*-

"""Convert NTCIR format to TREC format."""


import re
import json
import argparse
from bs4 import BeautifulSoup


def punctuation_mark_cleanser(s):
    """Add spacing in muddled sentences."""
    s = re.sub(r'([A-Za-z])([\.\?\!\(\)])([A-Za-z\(\)])', r'\g<1>\g<2> \g<3>', s)
    return s


# get the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--input",
                    help="input file in NTCIR format.",
                    type=str)

parser.add_argument("--output",
                    help="output file in jsonl format.",
                    type=str)

args = parser.parse_args()

with open(args.input, 'r') as f:
    with open(args.output, 'w') as o:
        is_in_document = False
        document = {}
        for i, line in enumerate(f):
            if line.startswith('<REC>'):
                is_in_document = True

            # document identifier
            elif line.startswith('<ACCN'):
                doc_id = BeautifulSoup(line.strip(), 'html.parser').text
                document["id"] = doc_id

            # title
            elif line.startswith('<TITE') or line.startswith('<PJNE'):
                title = BeautifulSoup(line.strip(), 'html.parser').text
                document["title"] = title

            # abstract
            elif line.startswith('<ABSE'):
                abstract = BeautifulSoup(line.strip(), 'html.parser').text
                abstract = punctuation_mark_cleanser(abstract)
                document["abstract"] = abstract

            # keywords
            elif line.startswith('<KYWE'):
                keywords = BeautifulSoup(line.strip(), 'html.parser').text
                keywords = re.split(" / |//|;|,", keywords)
                keywords = ';'.join([k.strip() for k in keywords])
                document["keyword"] = keywords

            elif line.startswith('</REC>'):
                if not is_in_document:
                    print("ERROR, document no valid at line {}".format(i))
                is_in_document = False
                o.write(json.dumps(document) + '\n')
                document = {}

