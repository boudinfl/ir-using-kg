#!/usr/bin/env bash

# T+A
EXP="ntcir-2"
for FILE in data/docs/*.gz
do
    python3 src/ntcir_to_trec.py --input ${FILE} \
                                 --output data/docs/${EXP}/${FILE##*/}
done

# T+A+K
EXP="ntcir-2+kw"
for FILE in data/docs/*.gz
do
    python3 src/ntcir_to_trec.py --input ${FILE} \
                                 --output data/docs/${EXP}/${FILE##*/} \
                                 --include_keywords
done

# T+A + Kps
# for TOP in 1 2 3 4 5 6 7 8 9 10
for TOP in 5
do
    #for VARIANT in "all" "abs" "pres"
    for VARIANT in "all"
    do
        # COPYRNN
        EXP="ntcir-2+copyrnn-top${TOP}-${VARIANT}"
        for FILE in data/docs/*.gz
        do
            python3 src/ntcir_to_trec.py --input ${FILE} \
                                         --output data/docs/${EXP}/${FILE##*/} \
                                         --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyRNN.${VARIANT}.json.gz \
                                         --nb_keyphrases ${TOP}
        done
        # CORRRNN
        EXP="ntcir-2+corrrnn-top${TOP}-${VARIANT}"
        for FILE in data/docs/*.gz
        do
            python3 src/ntcir_to_trec.py --input ${FILE} \
                                         --output data/docs/${EXP}/${FILE##*/} \
                                         --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyCorrRNN.${VARIANT}.json.gz \
                                         --nb_keyphrases ${TOP}
        done
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

# T+A+K + Kps
# for TOP in 1 2 3 4 5 6 7 8 9 10
for TOP in 5
do
    #for VARIANT in "all" "abs" "pres"
    for VARIANT in "all"
    do
        # COPYRNN
        EXP="ntcir-2+kw+copyrnn-top${TOP}-${VARIANT}"
        for FILE in data/docs/*.gz
        do
            python3 src/ntcir_to_trec.py --input ${FILE} \
                                         --output data/docs/${EXP}/${FILE##*/} \
                                         --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyRNN.${VARIANT}.json.gz \
                                         --nb_keyphrases ${TOP} \
                                         --include_keywords
        done

        # CORRRNN
        EXP="ntcir-2+kw+corrrnn-top${TOP}-${VARIANT}"
        for FILE in data/docs/*.gz
        do
            python3 src/ntcir_to_trec.py --input ${FILE} \
                                         --output data/docs/${EXP}/${FILE##*/} \
                                         --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyCorrRNN.${VARIANT}.json.gz \
                                         --nb_keyphrases ${TOP} \
                                         --include_keywords
        done

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