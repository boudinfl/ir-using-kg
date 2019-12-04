#!/usr/bin/env bash
TOPICFIELD="description"
for INDEX in data/indexes/lucene-index.*
do
    EXP=${INDEX##*/lucene-index.}
    # for MODEL in "bm25" "ql"
    for MODEL in "bm25"
    do
        if [[ ! -f "output/run.${EXP}.${TOPICFIELD}.${MODEL}.txt" ]]
        then
            # retrieve documents using the given model
            sh anserini/target/appassembler/bin/SearchCollection \
               -topicreader Trec \
               -index ${INDEX} \
               -topics data/topics/topic-e0101-0149.title+desc+narr.trec \
               -output output/run.${EXP}.${TOPICFIELD}.${MODEL}.txt -${MODEL} \
               -topicfield ${TOPICFIELD}
        fi

        if [[ ! -f "output/run.${EXP}.${TOPICFIELD}.${MODEL}+rm3.txt" ]]
        then
            # compute model with pseudo-relevance feedback RM3
            sh anserini/target/appassembler/bin/SearchCollection \
               -topicreader Trec \
               -index ${INDEX} \
               -topics data/topics/topic-e0101-0149.title+desc+narr.trec \
               -output output/run.${EXP}.${TOPICFIELD}.${MODEL}+rm3.txt -${MODEL} -rm3 \
               -topicfield ${TOPICFIELD}
        fi
    done
done