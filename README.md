# Keyphrase Generation for Scientific Document Retrieval

This repository contains the code for reproducing the experiments from the paper:

 - **Keyphrase Generation for Scientific Document Retrieval.**
   Florian Boudin, Ygor Gallina, Akiko Aizawa.
   Association for Computational Linguistics (ACL), 2020.

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
Below are the installation steps for a mac computer (tested on OSX 10.14) based on their [colab demo](https://colab.research.google.com/drive/1s44ylhEkXDzqNgkJSyXDYetGIxO9TWZn).


```bash
# install maven
brew cask install adoptopenjdk
brew install maven

# cloning / installing anserini
git clone https://github.com/castorini/anserini.git --recurse-submodules
cd anserini/
# changing jacoco from 0.8.2 to 0.8.3 in pom.xml to build correctly
mvn clean package appassembler:assemble

# compile evaluation tools and other scripts
cd tools/eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make && cd ../../..
cd tools/eval/ndeval && make && cd ../../..
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
sh src/0_create_data.sh
```

Some statistics about the generated data:

```
ntc1-e1: 187,080 documents, 185,061 with keywords
ntc2-e1g: 77,433 documents, 75,081 with keywords
ntc2-e1k: 57,545 documents, 57,443 with keywords

all 322,058 documents, 317,585 with keywords (98.6%)
```


### Creating indexes

We are now ready for indexing!

```bash
sh src/1_create_indexes.sh
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

Topics are categorized into fields:

1. Electricity, information and control
2. Chemistry
3. Architecture, civil engineering and landscape gardening
4. Biology and agriculture
5. Science
6. Engineering
7. Medicine and dentistry
8. Cultural and social science


### Retrieving documents

We are now ready to retrieve !

```bash
sh src/2_retrieve.sh 
```

Note that the default topic field used for retrieving 
documents is set to `title` by default according to anserini
`SearchCollection` helper:

```
 -topicfield VAL             : Which field of the query should be used, default
                               "title". For TREC ad hoc topics, description or
                               narrative can be used. (default: title)
```


## Evaluation

```bash
sh src/3_evaluate.sh
```

## Results


Results for retrieval models using keyphrase generation are reported in the
table below.  Two initial indexing configurations are examined: title and 
abstract only (T+A), and title, abstract and author keywords (T+A+K).


| MAP                        | BM25   | +RM3   | QL     | +RM3   |
:----------------------------|--------|--------|--------|--------|
| T+A                        | 0.2916 | 0.3193 | 0.2898 | 0.3147 |
| +s2s-copy-top5-all         | 0.3045 | 0.3356 | 0.3012 | 0.3233 |
| +s2s-corr-top5-all         | 0.3010 | 0.3306 | 0.2941 | 0.3079 |
| +multipartiterank-top5     | 0.2924 | 0.3227 | 0.2956 | 0.3269 |
|                            |        |        |        |        |
| T+A+K                      | 0.3138 | 0.3517 | 0.3063 | 0.3300 |
| +s2s-copy-top5-all         | 0.3157 | 0.3652 | 0.3163 | 0.3367 |
| +s2s-corr-top5-all         | 0.3137 | 0.3526 | 0.3101 | 0.3260 |
| +multipartiterank-top5     | 0.3138 | 0.3518 | 0.3123 | 0.3347 |
