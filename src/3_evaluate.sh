#!/usr/bin/env bash
for RUN in output/*.txt
do
    echo "Evaluating ${RUN}"
    # -m P.30
    # -q
    anserini/tools/eval/trec_eval.9.0.4/trec_eval -m map -q \
                                            data/rels/rel1_ntc2-e2_0101-0149 \
                                            ${RUN} > ${RUN%.*}.results
    anserini/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.10 -q \
                                            data/rels/rel1_ntc2-e2_0101-0149 \
                                            ${RUN}
done