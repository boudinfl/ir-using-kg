# IR Evaluation of Keyphrase Generation 
 
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
# create data files WITHOUT keyword information 
exp_name="ntcir1+2"
mkdir data/docs/${exp_name}
python3 src/ntcir_to_trec.py --input data/docs/ntc1-e1.mod \
                             --output data/docs/${exp_name}/ntc1-e1.trec
python3 src/ntcir_to_trec.py --input data/docs/ntc2-e1g \
                             --output data/docs/${exp_name}/ntc2-e1g.trec
python3 src/ntcir_to_trec.py --input data/docs/ntc2-e1k \
                             --output data/docs/${exp_name}/ntc2-e1k.trec

# create data files WITH keyword information
exp_name="ntcir1+2.keywords"
mkdir data/docs/${exp_name}/
python3 src/ntcir_to_trec.py --input data/docs/ntc1-e1.mod \
                             --keep_keywords \
                             --output data/docs/${exp_name}/ntc1-e1.trec
python3 src/ntcir_to_trec.py --input data/docs/ntc2-e1g \
                             --keep_keywords \
                             --output data/docs/${exp_name}/ntc2-e1g.trec
python3 src/ntcir_to_trec.py --input data/docs/ntc2-e1k \
                             --keep_keywords \
                             --output data/docs/${exp_name}/ntc2-e1k.trec
```

We are now ready for indexing!

```bash
# create index WITHOUT keyword information
exp_name="ntcir1+2"
sh anserini/target/appassembler/bin/IndexCollection -collection TrecCollection \
    -generator JsoupGenerator \
    -threads 2 \
    -input data/docs/${exp_name}/ \
    -index data/indexes/lucene-index.${exp_name}.pos+docvectors+rawdocs \
    -storePositions -storeDocvectors -storeRawDocs

# create index WITH keyword information
exp_name="ntcir1+2.keywords"
sh anserini/target/appassembler/bin/IndexCollection -collection TrecCollection \
    -generator JsoupGenerator \
    -threads 2 \
    -input data/docs/${exp_name}/ \
    -index data/indexes/lucene-index.${exp_name}.pos+docvectors+rawdocs \
    -storePositions -storeDocvectors -storeRawDocs
```

## Retrieval

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
python3 src/topics_to_trec.py --input data/topics/topic-e0101-0149 \
     --output data/topics/topic-e0101-0149.title+desc+narr.trec --keep_narrative
```

We are now ready to retrieve !

```bash
# retrieve topics on the index WITHOUT keywords
exp_name="ntcir1+2"

sh anserini/target/appassembler/bin/SearchCollection -topicreader Trec \
   -index data/indexes/lucene-index.${exp_name}.pos+docvectors+rawdocs \
   -topics data/topics/topic-e0101-0149.title+desc+narr.trec \
   -output output/run.${exp_name}.bm25.txt -bm25

sh anserini/target/appassembler/bin/SearchCollection -topicreader Trec \
   -index data/indexes/lucene-index.${exp_name}.pos+docvectors+rawdocs \
   -topics data/topics/topic-e0101-0149.title+desc+narr.trec \
   -output output/run.${exp_name}.bm25+rm3.txt -bm25 -rm3

sh anserini/target/appassembler/bin/SearchCollection -topicreader Trec \
   -index data/indexes/lucene-index.${exp_name}.pos+docvectors+rawdocs \
   -topics data/topics/topic-e0101-0149.title+desc+narr.trec \
   -output output/run.${exp_name}.ql.txt -ql 

sh anserini/target/appassembler/bin/SearchCollection -topicreader Trec \
   -index data/indexes/lucene-index.${exp_name}.pos+docvectors+rawdocs \
   -topics data/topics/topic-e0101-0149.title+desc+narr.trec \
   -output output/run.${exp_name}.ql+rm3.txt -ql -rm3

# retrieve topics on the index WITH keywords
exp_name="ntcir1+2.keywords"

sh anserini/target/appassembler/bin/SearchCollection -topicreader Trec \
   -index data/indexes/lucene-index.${exp_name}.pos+docvectors+rawdocs \
   -topics data/topics/topic-e0101-0149.title+desc+narr.trec \
   -output output/run.${exp_name}.bm25.txt -bm25

sh anserini/target/appassembler/bin/SearchCollection -topicreader Trec \
   -index data/indexes/lucene-index.${exp_name}.pos+docvectors+rawdocs \
   -topics data/topics/topic-e0101-0149.title+desc+narr.trec \
   -output output/run.${exp_name}.bm25+rm3.txt -bm25 -rm3

sh anserini/target/appassembler/bin/SearchCollection -topicreader Trec \
   -index data/indexes/lucene-index.${exp_name}.pos+docvectors+rawdocs \
   -topics data/topics/topic-e0101-0149.title+desc+narr.trec \
   -output output/run.${exp_name}.ql.txt -ql 

sh anserini/target/appassembler/bin/SearchCollection -topicreader Trec \
   -index data/indexes/lucene-index.${exp_name}.pos+docvectors+rawdocs \
   -topics data/topics/topic-e0101-0149.title+desc+narr.trec \
   -output output/run.${exp_name}.ql+rm3.txt -ql -rm3
```

## Evaluation

```bash

# Eval WITHOUT keywords
exp_name="ntcir1+2"

# Eval BM25 / BM25+RM3 WITHOUT keywords
anserini/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
    data/rels/rel1_ntc2-e2_0101-0149 output/run.${exp_name}.bm25.txt
    
anserini/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
    data/rels/rel1_ntc2-e2_0101-0149 output/run.${exp_name}.bm25+rm3.txt
    
# Eval QL / QL+RM3 WITHOUT keywords 
anserini/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
    data/rels/rel1_ntc2-e2_0101-0149 output/run.${exp_name}.ql.txt
    
anserini/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
    data/rels/rel1_ntc2-e2_0101-0149 output/run.${exp_name}.ql+rm3.txt
 
# Eval WITH keywords
exp_name="ntcir1+2.keywords"

# Eval BM25 / BM25+RM3 WITH keywords 
anserini/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
    data/rels/rel1_ntc2-e2_0101-0149 output/run.${exp_name}.bm25.txt

anserini/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
    data/rels/rel1_ntc2-e2_0101-0149 output/run.${exp_name}.bm25+rm3.txt

# Eval QL / QL+RM3 WITH keywords 
anserini/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
    data/rels/rel1_ntc2-e2_0101-0149 output/run.${exp_name}.ql.txt
    
anserini/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
    data/rels/rel1_ntc2-e2_0101-0149 output/run.${exp_name}.ql+rm3.txt
```

## Results


| MAP       | BM25   | +RM3   | QL     | +RM3   |
:-----------|--------|--------|--------|--------|
| NTCIR-1+2 | 0.2212 | 0.2374 | 0.2164 | 0.2067 |
| +keywords | 0.2379 | 0.2592 | 0.2376 | 0.2373 |


| P30       | BM25   | +RM3   | QL     | +RM3   |
:-----------|--------|--------|--------|--------|
| NTCIR-1+2 | 0.1531 | 0.1714 | 0.1544 | 0.1626 |
| +keywords | 0.1571 | 0.1769 | 0.1605 | 0.1707 |

## Automatic keyphrase generation

First, we convert NTCIR SGML formatted documents to jsonl format for easier processing.

```bash
# create data files WITHOUT keyword information 
python3 src/ntcir_to_jsonl.py --input data/docs/ntc1-e1.mod \
                              --output data/docs/ntc1-e1.jsonl
python3 src/ntcir_to_jsonl.py --input data/docs/ntc2-e1g \
                              --output data/docs/ntc2-e1g.jsonl
python3 src/ntcir_to_jsonl.py --input data/docs/ntc2-e1k \
                              --output data/docs/ntc2-e1k.jsonl
```
