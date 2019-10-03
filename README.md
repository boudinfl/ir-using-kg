# IR Evaluation of Keyphrase Generation 

## Data

* [Data](#data)
* [Installing anserini](#installing-anserini)
* [Indexing](#indexing)
  * [Converting documents to TREC format](#converting-documents-to-trec-format)
  * [Creating indexes](#creating-indexes)
* [Retrieval](#retrieval)
  * [Converting topics to TREC format](#converting-topics-to-trec-format)
  * [Retrieving documents](#retrieving-documents)
* [Evaluation](#evaluation)
 
## Data

Here, we use the [NTCIR-2](http://research.nii.ac.jp/ntcir/ntcir-ws2/) ad-hoc monolingual (English) IR test collection.
The test collection contains 322,058 documents, 49 search topics and relevance judgments.

```
|-- data
    |-- docs
        |-- ntc1.e1.gz  // NTCIR-1 (#187,080) collection converted with ACCN-e.pl 
        |-- ntc2-e1g.gz // NTCIR-2 (#77,433) NACSIS Academic Conference Papers Database
        |-- ntc2-e1k.gz // NTCIR-2 (#57,545) NACSIS Grant-in-Aid Scientific Research Database
    |-- rels
        |-- rel1_ntc2-e2_0101-0149 // judgments for relevant documents 
        |-- rel2_ntc2-e2_0101-0149 // judgments for partially relevant documents 
    |-- topics
        |-- topic-e0101-0149 // English topics for NTCIR-2
```

## Installing anserini

Here, we use the open-source information retrieval toolkit [anserini](http://anserini.io/) which is built on [Lucene](https://lucene.apache.org/).
Below are the installation steps on a mac based on their [colab demo](https://colab.research.google.com/drive/1s44ylhEkXDzqNgkJSyXDYetGIxO9TWZn).


```bash
# install maven
brew cask install adoptopenjdk
brew install maven

# cloning / installing anserini
git clone https://github.com/castorini/anserini.git
cd anserini/
cd eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make
cd eval && cd ndeval && make
mvn clean package appassembler:assemble -q -Dmaven.javadoc.skip=true
```

## Indexing

### Converting documents to TREC format

First, we convert NTCIR SGML formatted documents to TREC format for easier indexing.

From

```xml
<REC>
    <ACCN>...</ACCN> // doc_id
    <TITE>...</TITE> or <PJNE>...</PJNE> // Title
    <AUPE>...</AUPE> // Authors
    <CNFE>...</CNFE> // Conference name
    <CNFD>...</CNFD> // Conference date
    <ABSE>           // Abstract
        <ABSE.P>...</ABSE.P> // paragraph
    </ABSE>
    <KYWE>...</KYWE> // Keywords
    <SOCE>...</SOCE> // Host society
</REC>
```

to

```xml
<DOC>
    <DOCNO>...</DOCNO>  // doc_id
    <TITLE>...</TITLE>  // title
    <TEXT>...</TEXT>    // abstract
    <HEAD>...</HEAD>    // keywords (optional)
</DOC>
```

by doing:

```bash
# create standard TREC data files
EXP="ntcir-2"
for FILE in data/docs/*.gz
do
    python3 src/ntcir_to_trec.py --input ${FILE} \
                                 --output data/docs/${EXP}/${FILE##*/}
done

# create TREC data files with (author) keywords information
EXP="ntcir-2+keywords"
for FILE in data/docs/*.gz
do
    python3 src/ntcir_to_trec.py --input ${FILE} \
                                 --output data/docs/${EXP}/${FILE##*/} \
                                 --include_keywords
done

# create TREC data files with (automatically) generated keyphrases information
for TOP in 5 10
do
    EXP="ntcir-2+top${TOP}-all.keyphrases"
    for FILE in data/docs/*.gz
    do
        python3 src/ntcir_to_trec.py --input ${FILE} \
                                     --output data/docs/${EXP}/${FILE##*/} \
                                     --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyRNN.all.json.gz \
                                     --nb_keyphrases ${TOP}
    done
    EXP="ntcir-2+top${TOP}-abs.keyphrases"
    for FILE in data/docs/*.gz
    do
        python3 src/ntcir_to_trec.py --input ${FILE} \
                                     --output data/docs/${EXP}/${FILE##*/} \
                                     --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyRNN.abs.json.gz \
                                     --nb_keyphrases ${TOP}
    done
    EXP="ntcir-2+top${TOP}-pres.keyphrases"
    for FILE in data/docs/*.gz
    do
        python3 src/ntcir_to_trec.py --input ${FILE} \
                                     --output data/docs/${EXP}/${FILE##*/} \
                                     --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyRNN.pres.json.gz \
                                     --nb_keyphrases ${TOP}
    done
done

# create TREC data files with (automatically) generated keyphrases and keyword information
for TOP in 5 10
do
    EXP="ntcir-2+keywords+top${TOP}-all.keyphrases"
    for FILE in data/docs/*.gz
    do
        python3 src/ntcir_to_trec.py --input ${FILE} \
                                     --output data/docs/${EXP}/${FILE##*/} \
                                     --path_to_keyphrases data/keyphrases/${FILE##*/}.CopyRNN.all.json.gz \
                                     --nb_keyphrases ${TOP} \
                                     --include_keywords
    done
done
```

### Creating indexes

We are now ready for indexing!

```bash
# create indexes
# for EXP in "ntcir-2" "ntcir-2+keywords" "ntcir-2+top5-all.keyphrases" "ntcir-2+top5-abs.keyphrases" "ntcir-2+top5-pres.keyphrases" "ntcir-2+top10-all.keyphrases" "ntcir-2+top10-abs.keyphrases" "ntcir-2+top10-pres.keyphrases"
for EXP in "ntcir-2+keywords+top5-all.keyphrases" "ntcir-2+keywords+top10-all.keyphrases" 
do
    sh anserini/target/appassembler/bin/IndexCollection \
        -collection TrecCollection \
        -generator JsoupGenerator \
        -threads 2 \
        -input data/docs/${EXP}/ \
        -index data/indexes/lucene-index.${EXP}.pos+docvectors+rawdocs \
        -storePositions -storeDocvectors -storeRawDocs
done
```

## Retrieval

### Converting topics to TREC format

Again, we have to convert NTCIR topics to TREC format for easier retrieval.

From

```xml
<TOPIC q=0101> // topic number is an attribute here

    <TITLE>       // title part
    ...
    </TITLE>
    
    <DESCRIPTION> // sentence-length description
    ...
    </DESCRIPTION>
    
    <NARRATIVE>  // longer narrative
    ...
    </NARRATIVE>
     
    <CONCEPT>  // concepts (?)
    ...
    </CONCEPT>
    
    <FIELD>  // fields (?)
    ...
    </FIELD>

</TOPIC>
```

to

```xml
<top>
    <num> Number: XXX 
    <title> ...
    
    <desc> Description: 
    ...
    
    <narr> Narrative: 
    ...
</top>
```

by doing:

```bash
# create topic file with title / description / narrative
python3 src/topics_to_trec.py \
        --input data/topics/topic-e0101-0149 \
        --output data/topics/topic-e0101-0149.title+desc+narr.trec \
        --keep_narrative
```

### Retrieving documents

We are now ready to retrieve !

```bash
# for EXP in "ntcir-2" "ntcir-2+keywords" "ntcir-2+top5-all.keyphrases" "ntcir-2+top5-abs.keyphrases" "ntcir-2+top5-pres.keyphrases" "ntcir-2+top10-all.keyphrases" "ntcir-2+top10-abs.keyphrases" "ntcir-2+top10-pres.keyphrases"
for EXP in "ntcir-2+keywords+top5-all.keyphrases" "ntcir-2+keywords+top10-all.keyphrases" 
do
    for MODEL in "bm25" "ql"
    do
        # compute model
        sh anserini/target/appassembler/bin/SearchCollection \
           -topicreader Trec \
           -index data/indexes/lucene-index.${EXP}.pos+docvectors+rawdocs \
           -topics data/topics/topic-e0101-0149.title+desc+narr.trec \
           -output output/run.${EXP}.${MODEL}.txt -${MODEL}
        
        # compute model with pseudo-relevance feedback RM3
        sh anserini/target/appassembler/bin/SearchCollection \
           -topicreader Trec \
           -index data/indexes/lucene-index.${EXP}.pos+docvectors+rawdocs \
           -topics data/topics/topic-e0101-0149.title+desc+narr.trec \
           -output output/run.${EXP}.${MODEL}+rm3.txt -${MODEL} -rm3
    done
done
```

## Evaluation

```bash
# for EXP in "ntcir-2" "ntcir-2+keywords" "ntcir-2+top5-all.keyphrases" "ntcir-2+top5-abs.keyphrases" "ntcir-2+top5-pres.keyphrases" "ntcir-2+top10-all.keyphrases" "ntcir-2+top10-abs.keyphrases" "ntcir-2+top10-pres.keyphrases"
for EXP in "ntcir-2+keywords+top5-all.keyphrases" "ntcir-2+keywords+top10-all.keyphrases" 
do
    echo "Experiment: ${EXP}"
    for MODEL in "bm25" "ql"
    do
        echo "Eval: ${MODEL}"
        anserini/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
            data/rels/rel1_ntc2-e2_0101-0149 \
            output/run.${EXP}.${MODEL}.txt
        
        echo "Eval: ${MODEL} + RM3"
        anserini/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
            data/rels/rel1_ntc2-e2_0101-0149 \
            output/run.${EXP}.${MODEL}+rm3.txt
    done
done
```

## Results


| MAP               | BM25   | +RM3   | QL     | +RM3   |
:-------------------|--------|--------|--------|--------|
| NTCIR-2           | 0.2212 | 0.2374 | 0.2164 | 0.2067 |
| +keywords         | 0.2379 | 0.2592 | 0.2376 | 0.2373 |
|                   |        |        |        |        |
| +top5-all.keyphrases   | 0.2228 | 0.2453 | 0.2221 | 0.2260 |
| +top5-pres.keyphrases  | 0.2214 | 0.2405 | 0.2169 | 0.2143 |
| +top5-abs.keyphrases   | 0.2204 | 0.2367 | 0.2164 | 0.2172 |
|                        |        |        |        |        |
| +top10-all.keyphrases  | 0.2211 | 0.2382 | 0.2223 | 0.2212 |
| +top10-pres.keyphrases | 0.2216 | 0.2420 | 0.2162 | 0.2098 |
| +top10-abs.keyphrases  | 0.2219 | 0.2332 | 0.2147 | 0.2108 |
|                        |        |        |        |        |
| +keywords+top5-all.keyphrases | 0.2380 | 0.2612 | 0.2413 | 0.2362 |
| +keywords+top10-all.keyphrases | 0.2341 | 0.2544 | 0.2398 | 0.2392 |



| P30               | BM25   | +RM3   | QL     | +RM3   |
:-------------------|--------|--------|--------|--------|
| NTCIR-2           | 0.1531 | 0.1714 | 0.1544 | 0.1626 |
| +keywords         | 0.1571 | 0.1769 | 0.1605 | 0.1707 |
|                   |        |        |        |        |
| +top5-all.keyphrases   | 0.1578 | 0.1701 | 0.1605 | 0.1701 |
| +top5-pres.keyphrases  | 0.1517 | 0.1714 | 0.1510 | 0.1660 |
| +top5-abs.keyphrases   | 0.1592 | 0.1673 | 0.1592 | 0.1707 |
|                        |        |        |        |        |
| +top10-all.keyphrases  | 0.1585 | 0.1680 | 0.1578 | 0.1694 |
| +top10-pres.keyphrases | 0.1517 | 0.1714 | 0.1503 | 0.1633 |
| +top10-abs.keyphrases  | 0.1558 | 0.1660 | 0.1558 | 0.1578 |
|                        |        |        |        |        |
| +keywords+top5-all.keyphrases | 0.1633 | 0.1776 | 0.1653 | 0.1762 |
| +keywords+top10-all.keyphrases | 0.1633 | 0.1762 | 0.1646 | 0.1735 |


## Automatic keyphrase generation

Example (no author's keywords provided)

```
<DOC>
    <DOCNO>gakkai-e-0000000538</DOCNO>
    <TITLE>
        A Hybrid PWM for Controlling the Harmonic Contents in the output of
        Voltage Inuerter
    </TITLE>
    <TEXT>
        The generalized method of harmonics elimination £1 is one of the few
        methods that deal with general solution for the harmonics problem.
        However, because the complex solution of the nonlinear equations in
        this method only a limited number of harmonics can be eliminated with a
        reasonable time and design constrains. To overcome these limitations and
        have a generalized method for harmonics reduction a simplified method to
        minimize and control the harmonic contents in the output of voltage
        inverter is introduced. With presented method any group of harmonics
        can be controlled within the design requirements while the other
        harmonics up to any order are kept within a minimum allowable range.
    </TEXT>
</DOC>
```

CopyRNN

```
|-- gakkai-e-0000000538
    |-- present: ["hybrid"], ["pwm"], ["\u00a31"], ["design"], 
                 ["control"], ["method"], ["group"]
    |-- absent: ["harmonics"], ["voltage inverter"], ["generalized method"], 
                ["voltage inuerter"], ["nonlinear equations"], ["voltage"], 
                ["inuerter"], ["inverter"], ["general"], 
                ["minimum allowable range"], ["finite element"], 
                ["allowable range"], ["nonlinear systems"]
    |-- all: ["harmonics"], ["voltage inverter"], ["hybrid"],
             ["generalized method"], ["pwm"], ["voltage inuerter"], 
             ["nonlinear equations"], ["voltage"], ["inuerter"], 
             ["\u00a31"], ["design"], ["control"], ["inverter"], 
             ["method"], ["general"], ["minimum allowable range"], 
             ["finite element"], ["allowable range"], ["group"], 
             ["nonlinear systems"]]
```

MultipartiteRank

```
|-- gakkai-e-0000000538
  |-- all: ["harmonic contents"], ["method"], ["output"], ["limited number"], 
           ["design"], ["general solution"], ["harmonics"], ["voltage inverter"],
           ["reasonable time"], ["group"], ["nonlinear equations"],
           ["hybrid pwm"], ["limitations"], ["complex solution"], ["order"],
           ["minimum allowable range"]
  |-- absent: ["harmonic contents"], ["limited number"], ["general solution"],
              ["harmonics"], ["voltage inverter"], ["reasonable time"],
              ["nonlinear equations"], ["limitations"], ["complex solution"],
              ["minimum allowable range"]
  |-- present: ["method"], ["output"], ["design"], ["group"], ["hybrid pwm"],
               ["order"]
```
