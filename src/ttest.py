# -*- coding: utf-8 -*-

"""Compute statistical test on trec results."""

import sys
import re
import json
import numpy
from collections import defaultdict
from scipy import stats


def load_trec_results(input):
    keys, scores = [], []
    with open(input, 'r') as f:
        for line in f:
            line = line.strip()
            line = re.sub("\s+", " ", line)
            cols = line.split()
            if len(cols) == 3:
                keys.append(cols[1])
                scores.append(float(cols[2]))
    return (keys, scores)


def get_field_scores(scores, ids):
    tmp = []
    for i, id in enumerate(scores[0]):
        if id in ids:
            tmp.append(scores[1][i])
    return tmp


with open('data/topics/domains.json') as json_file:
    fields = json.load(json_file)
    field_to_topic_ids = defaultdict(list)
    for topic_id in fields:
        for field in fields[topic_id]:
            field_to_topic_ids[field].append(topic_id)

scores_a = load_trec_results(sys.argv[1])
scores_b = load_trec_results(sys.argv[2])

assert(scores_a[0][:-1] == scores_b[0][:-1])

print('scoring for file: {}'.format(sys.argv[1]))
print('all: {0:.4f}'.format(numpy.average(scores_a[1][:-1])))

print('scoring for file: {}'.format(sys.argv[2]))
print('all: {0:.4f}'.format(numpy.average(scores_b[1][:-1])))

print(stats.ttest_rel(a=scores_a[1][:-1],
                      b=scores_b[1][:-1]))

print('statistics for fields')
# for field_id in range(1, 9):
for field_id in range(1, 3):

    field_scores_a = get_field_scores(scores_a, field_to_topic_ids[field_id])
    field_scores_b = get_field_scores(scores_b, field_to_topic_ids[field_id])

    print('field: {0}, size: {1}, score 1: {2:.4f}, score 2: {3:.4f}, delta: {4:.1f}, {5}, {6:.4f}'.format(
          field_id,
          len(field_to_topic_ids[field_id]),
          numpy.average(field_scores_a),
          numpy.average(field_scores_b),
          ((numpy.average(field_scores_b) / numpy.average(field_scores_a)) - 1 ) *100,
          stats.ttest_rel(a=field_scores_a, b=field_scores_b),
          (numpy.average(field_scores_b) - numpy.average(field_scores_a)) * 100
          ))

# print('statistics for queries')
# for i, id in enumerate(scores_a[0][:-1]):
#   print('query: {0}\t{1:.4f}\t{2:.4f}\t{3}'.format(
#         id, 
#         scores_a[1][i],
#         scores_b[1][i],
#         fields[id]
#         ))





