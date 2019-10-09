#!/usr/bin/env bash
for EXP in data/docs/ntcir-2*
do
    if [[ ! -d "data/indexes/lucene-index.${EXP##*/}" ]]
    then
        sh anserini/target/appassembler/bin/IndexCollection \
            -collection TrecCollection \
            -generator JsoupGenerator \
            -threads 2 \
            -input ${EXP}/ \
            -index data/indexes/lucene-index.${EXP##*/} \
            -storePositions -storeDocvectors -storeRawDocs
    else
        echo "Index for ${EXP##*/} already exists"
    fi
done