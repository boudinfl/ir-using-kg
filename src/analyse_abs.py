# -*- coding: utf-8 -*-

"""
    Analyse the absent keyphrases from the TREC-formatted files to compute some
    interesting statistics.
"""

import re
import sys
import gzip
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

import spacy
nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser", "ner"])


def pptext(s):
    """lowercase, tokenize and stem text."""
    doc = nlp(s)
    words = [word.text for word in doc]
    return " ".join([PorterStemmer().stem(w.lower()) for w in words])


sum_ratio_present_kps = 0
sum_ratio_absent_kps = 0
sum_ratio_absent_kps_case_1 = 0
sum_ratio_absent_kps_case_2 = 0
sum_ratio_absent_kps_case_3 = 0
nb_documents_with_kps = 0


with gzip.open(sys.argv[1], 'rt') as f:
    document = ''
    for i, line in enumerate(f):
        line = line.strip()
        if line:
            document += line
        else:
            try:
                parse = BeautifulSoup(document, 'html.parser')
            except:
                pass

            document = ''
            # test whether document includes keyphrases
            if parse.head is not None:
                print(parse.docno.text)

                title = pptext(parse.title.text)
                abstract = pptext(parse.find('text').text)

                keyphrases = [kp.strip() for kp in parse.head.text.split("//")]
                if len(keyphrases) < 2:
                    if "," in keyphrases[0]:
                        keyphrases = keyphrases[0].split(",")
                    if ' / ' in keyphrases[0]:
                        keyphrases = keyphrases[0].split(" / ")
                    if ' ; ' in keyphrases[0]:
                        keyphrases = keyphrases[0].split(" ; ")
                keyphrases = [pptext(k) for k in keyphrases]

                nb_present_kps = 0
                nb_absent_kps = 0
                nb_absent_kps_case_1 = 0
                nb_absent_kps_case_2 = 0
                nb_absent_kps_case_3 = 0
                for keyphrase in keyphrases:
                    if keyphrase in title or keyphrase in abstract:
                        nb_present_kps += 1
                    else:

                        nb_present_words = 0
                        words = keyphrase.split()
                        for word in words:
                            if word in title or word in abstract:
                                nb_present_words += 1

                        # Case 1: every word but not the sequence
                        if nb_present_words == len(words):
                            nb_absent_kps_case_1 += 1

                        # Case 2: some words appear
                        elif nb_present_words > 0:
                            nb_absent_kps_case_2 += 1

                        # Case 3: no word appears
                        else:
                            nb_absent_kps_case_3 += 1

                        nb_absent_kps += 1

                sum_ratio_present_kps += nb_present_kps / len(keyphrases)
                sum_ratio_absent_kps += nb_absent_kps / len(keyphrases)
                sum_ratio_absent_kps_case_1 += nb_absent_kps_case_1 / len(keyphrases)
                sum_ratio_absent_kps_case_2 += nb_absent_kps_case_2 / len(keyphrases)
                sum_ratio_absent_kps_case_3 += nb_absent_kps_case_3 / len(keyphrases)
                nb_documents_with_kps += 1


print("present: {}".format(sum_ratio_present_kps/nb_documents_with_kps))
print("absent: {}".format(sum_ratio_absent_kps/nb_documents_with_kps))
print("|-> case 1 (all words): {}".format(sum_ratio_absent_kps_case_1/nb_documents_with_kps))
print("|-> case 2 (some words): {}".format(sum_ratio_absent_kps_case_2/nb_documents_with_kps))
print("|-> case 3 (no words): {}".format(sum_ratio_absent_kps_case_3/nb_documents_with_kps))

print("nb_documents_with_kps: {}".format(nb_documents_with_kps))
print("sum_ratio_present_kps: {}".format(sum_ratio_present_kps))
print("sum_ratio_absent_kps: {}".format(sum_ratio_absent_kps))
print("sum_ratio_absent_kps_case_1: {}".format(sum_ratio_absent_kps_case_1))
print("sum_ratio_absent_kps_case_2: {}".format(sum_ratio_absent_kps_case_2))
print("sum_ratio_absent_kps_case_3: {}".format(sum_ratio_absent_kps_case_3))

