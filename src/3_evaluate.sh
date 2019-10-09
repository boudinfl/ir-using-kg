#!/usr/bin/env bash
for RUN in output/*.txt
do
    echo "Evaluating ${RUN}"
    anserini/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                                            data/rels/rel1_ntc2-e2_0101-0149 \
                                            ${RUN}
done