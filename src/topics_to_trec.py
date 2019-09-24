# -*- coding: utf-8 -*-

"""Convert NTCIR format to TREC format."""


import re
import argparse
from bs4 import BeautifulSoup

# get the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--input",
                    help="input file in NTCIR format.",
                    type=str)

parser.add_argument("--output",
                    help="output file in TREC format.",
                    type=str)

parser.add_argument('--keep_narrative',
                    action='store_true',
                    help='keep the narrative part in the output file.')

args = parser.parse_args()

with open(args.input, 'r') as f:
    with open(args.output, 'w') as o:
        content = ""
        for i, line in enumerate(f):
            if line.startswith('</TOPIC>'):
                document = BeautifulSoup(content, 'html.parser')
                o.write('<top>\n')
                o.write("<num> Number: {}\n".format(int(document.topic['q'])))
                o.write("<title>{}\n\n".format(document.title.text.strip()))
                o.write("<desc> Description:\n{}\n\n".format(
                    document.description.text.strip()))
                if args.keep_narrative:
                    o.write("<narr> Narrative:\n{}\n\n".format(
                        document.narrative.text.strip()))
                o.write('</top>\n\n')
                content = ""
            else:
                content += line

