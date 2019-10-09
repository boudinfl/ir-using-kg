#!/usr/bin/env bash

# create standard TREC data files
EXP="ntcir-2"
for FILE in data/docs/*.gz
do
    python3 src/ntcir_to_trec.py --input ${FILE} \
                                 --output data/docs/${EXP}/${FILE##*/}
done

# create TREC data files with (author) keywords information
EXP="ntcir-2+kw"
for FILE in data/docs/*.gz
do
    python3 src/ntcir_to_trec.py --input ${FILE} \
                                 --output data/docs/${EXP}/${FILE##*/} \
                                 --include_keywords
done

# create TREC data files with (automatically) generated keyphrases information
for TOP in 5 10
do
    EXP="ntcir-2+copyrnn-top${TOP}-all"
    for FILE in data/docs/*.gz
    do
        python3 src/ntcir_to_trec.py --input ${FILE} \
                                     --output data/docs/${EXP}/${FILE##*/} \
                                     --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyRNN.all.json.gz \
                                     --nb_keyphrases ${TOP}
    done
    EXP="ntcir-2+copyrnn-top${TOP}-abs"
    for FILE in data/docs/*.gz
    do
        python3 src/ntcir_to_trec.py --input ${FILE} \
                                     --output data/docs/${EXP}/${FILE##*/} \
                                     --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyRNN.abs.json.gz \
                                     --nb_keyphrases ${TOP}
    done
    EXP="ntcir-2+copyrnn-top${TOP}-pres"
    for FILE in data/docs/*.gz
    do
        python3 src/ntcir_to_trec.py --input ${FILE} \
                                     --output data/docs/${EXP}/${FILE##*/} \
                                     --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyRNN.pres.json.gz \
                                     --nb_keyphrases ${TOP}
    done
    EXP="ntcir-2+multipartiterank-top${TOP}"
    for FILE in data/docs/*.gz
    do
        python3 src/ntcir_to_trec.py --input ${FILE} \
                                     --output data/docs/${EXP}/${FILE##*/} \
                                     --path_to_keyphrases data/keyphrases/${FILE##*/}.MultipartiteRank.pres.json.gz \
                                     --nb_keyphrases ${TOP}
    done
done

# create TREC data files with (automatically) generated keyphrases and keyword information
for TOP in 5 10
do
    EXP="ntcir-2+kw+copyrnn-top${TOP}-all"
    for FILE in data/docs/*.gz
    do
        python3 src/ntcir_to_trec.py --input ${FILE} \
                                     --output data/docs/${EXP}/${FILE##*/} \
                                     --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyRNN.all.json.gz \
                                     --nb_keyphrases ${TOP} \
                                     --include_keywords
    done
    EXP="ntcir-2+kw+multipartiterank-top${TOP}"
    for FILE in data/docs/*.gz
    do
        python3 src/ntcir_to_trec.py --input ${FILE} \
                                     --output data/docs/${EXP}/${FILE##*/} \
                                     --path_to_keyphrases data/keyphrases/${FILE##*/}.MultipartiteRank.pres.json.gz \
                                     --nb_keyphrases ${TOP} \
                                     --include_keywords
    done
done