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

Note that we did not modify the default topic field used for retrieving 
documents. It is set to `title` by default according to anserini
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


| MAP                        | BM25   | +RM3   |
:----------------------------|--------|--------|
| NTCIR-2                    | 0.2212 | 0.2374 |
| +keywords                  | 0.2379 | 0.2592 |
|                            |        |        |
| +copyrnn-top5-all          | 0.2228 | 0.2453 |
| +copyrnn-top5-pres         | 0.2233 | 0.2460 |
| +copyrnn-top5-abs          | 0.2144 | 0.2149 |
| +copyrnn-top10-all         | 0.2211 | 0.2381 |
| +copyrnn-top10-pres        | 0.2205 | 0.2343 |
| +copyrnn-top10-abs         | 0.2113 | 0.2094 |
|                            |        |        |
| +multipartiterank-top5     | 0.2214 | 0.2322 |
| +multipartiterank-top10    | 0.2170 | 0.2273 |
|                            |        |        |
| +kw+copyrnn-top5-all       | 0.2380 | 0.2612 |
| +kw+copyrnn-top10-all      | 0.2341 | 0.2544 |
| +kw+multipartiterank-top5  | 0.2403 | 0.2582 |
| +kw+multipartiterank-top10 | 0.2351 | 0.2558 |

| P30                        | BM25   | +RM3   |
:----------------------------|--------|--------|
| NTCIR-2                    | 0.1531 | 0.1714 |
| +keywords                  | 0.1571 | 0.1769 |
|                            |        |        |
| +copyrnn-top5-all          | 0.1578 | 0.1701 |
| +copyrnn-top5-pres         | 0.1571 | 0.1680 |
| +copyrnn-top5-abs          | 0.1483 | 0.1599 |
| +copyrnn-top10-all         | 0.1578 | 0.1680 |
| +copyrnn-top10-pres        | 0.1585 | 0.1673 |
| +copyrnn-top10-abs         | 0.1469 | 0.1592 |
|                            |        |        |
| +multipartiterank-top5     | 0.1537 | 0.1714 |
| +multipartiterank-top10    | 0.1517 | 0.1673 |
|                            |        |        |
| +kw+copyrnn-top5-all       | 0.1633 | 0.1776 |
| +kw+copyrnn-top10-all      | 0.1633 | 0.1762 |
| +kw+multipartiterank-top5  | 0.1605 | 0.1748 |
| +kw+multipartiterank-top10 | 0.1537 | 0.1796 |


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

    |-- present: ['harmonics'], ['voltage inverter'], ['hybrid'],
                 ['generalized method'], ['pwm'], ['voltage inuerter'],
                 ['nonlinear equations'], ['voltage'], ['inuerter'], ['£1'],
                 ['design'], ['control'], ['inverter'], ['method'], ['general'],
                 ['minimum allowable range'], ['allowable range'], ['group'],
                 ['nonlinear'], ['elimination']
                 
    |-- absent: ['finite element'], ['nonlinear systems'], ['optimization'],
                ['wavelets'], ['chaos'], ['stability'],
                ['computational geometry'], ['65n30'], ['preconditioning'],
                ['fem'], ['convergence'], ['regularization'],
                ['numerical analysis'], ['simulation'], ['uncertainty'],
                ['computational fluid dynamics'], ['interpolation'],
                ['algorithms'], ['cryptography'], ['electromagnetics']]

    |-- all: ['harmonics'], ['voltage inverter'], ['hybrid'],
             ['generalized method'], ['pwm'], ['voltage inuerter'],
             ['nonlinear equations'], ['voltage'], ['inuerter'], ['£1'],
             ['design'], ['control'], ['inverter'], ['method'], ['general'],
             ['minimum allowable range'], ['finite element'],
             ['allowable range'], ['group'], ['nonlinear systems']
```

MultipartiteRank

```
with gzip.open('ntc1-e1.gz.MultipartiteRank.pres.json.gz', 'rt') as f:
    key = json.loads(f.read())
    print(key["gakkai-e-0000000538"])

|-- gakkai-e-0000000538

  |-- present: ['harmonic contents'], ['method'], ['output'],
               ['voltage inuerter'], ['limited number'], ['general solution'],
               ['design'], ['harmonics'], ['voltage inverter'],
               ['reasonable time'], ['group'], ['nonlinear equations'],
               ['hybrid pwm'], ['limitations'], ['complex solution'],
               ['order'], ['minimum allowable range']
```
