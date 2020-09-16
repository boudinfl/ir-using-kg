#!/usr/bin/env bash

# T+A
EXP="ntcir-2-t+a"
for FILE in data/docs/*.gz
do
    python3 src/ntcir_to_trec.py --input ${FILE} \
                                 --output data/docs/${EXP}/${FILE##*/}
done

# T+A+K
EXP="ntcir-2-t+a+k"
for FILE in data/docs/*.gz
do
    python3 src/ntcir_to_trec.py --input ${FILE} \
                                 --output data/docs/${EXP}/${FILE##*/} \
                                 --include_keywords
done

# T+A + absent K or present K
for VARIANT in "abs" "pres" "abs_c1" "abs_c2" "abs_c3"
do
    EXP="ntcir-2-t+a+k-${VARIANT}"
    for FILE in data/docs/*.gz
    do

        python3 src/ntcir_to_trec.py --input ${FILE} \
                                     --output data/docs/${EXP}/${FILE##*/} \
                                     --path_to_keyphrases data/keyphrases/${FILE##*/}.gold.${VARIANT}.json.gz \
                                     --nb_keyphrases 100
    done
done

# T+A + Kps
# for TOP in 1 2 3 4 5 6 7 8 9 10
for TOP in 5
do
    #for VARIANT in "all" "abs" "pres"
    for VARIANT in "all"
    do
        # seq2seq + copy
        EXP="ntcir-2-t+a+s2s-copy-top${TOP}-${VARIANT}"
        for FILE in data/docs/*.gz
        do
            python3 src/ntcir_to_trec.py --input ${FILE} \
                                         --output data/docs/${EXP}/${FILE##*/} \
                                         --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyRNN.${VARIANT}.json.gz \
                                         --nb_keyphrases ${TOP}
        done
        # seq2seq + corr
        EXP="ntcir-2-t+a+s2s-corr-top${TOP}-${VARIANT}"
        for FILE in data/docs/*.gz
        do
            python3 src/ntcir_to_trec.py --input ${FILE} \
                                         --output data/docs/${EXP}/${FILE##*/} \
                                         --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyCorrRNN.${VARIANT}.json.gz \
                                         --nb_keyphrases ${TOP}
        done
    done

    # multipartiterank
    EXP="ntcir-2-t+a+mp-rank-top${TOP}"
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
        EXP="ntcir-2-t+a+k+s2s-copy-top${TOP}-${VARIANT}"
        for FILE in data/docs/*.gz
        do
            python3 src/ntcir_to_trec.py --input ${FILE} \
                                         --output data/docs/${EXP}/${FILE##*/} \
                                         --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyRNN.${VARIANT}.json.gz \
                                         --nb_keyphrases ${TOP} \
                                         --include_keywords
        done

        # CORRRNN
        EXP="ntcir-2-t+a+k+s2s-corr-top${TOP}-${VARIANT}"
        for FILE in data/docs/*.gz
        do
            python3 src/ntcir_to_trec.py --input ${FILE} \
                                         --output data/docs/${EXP}/${FILE##*/} \
                                         --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyCorrRNN.${VARIANT}.json.gz \
                                         --nb_keyphrases ${TOP} \
                                         --include_keywords
        done

    done

    # multipartiterank
    EXP="ntcir-2-t+a+k+mp-rank-top${TOP}"
    for FILE in data/docs/*.gz
    do
        python3 src/ntcir_to_trec.py --input ${FILE} \
                                     --output data/docs/${EXP}/${FILE##*/} \
                                     --path_to_keyphrases data/keyphrases/${FILE##*/}.MultipartiteRank.pres.json.gz \
                                     --nb_keyphrases ${TOP} \
                                     --include_keywords
    done

done