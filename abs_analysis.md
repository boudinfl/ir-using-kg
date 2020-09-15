# Looking at absent keyphrases

## Retrieval results

Results for retrieval models using keyphrase generation are reported in the
table below.  Two initial indexing configurations are examined: title and 
abstract only (T+A), and title, abstract and author keywords (T+A+K).


| MAP                        | BM25   | +RM3   | QL     | +RM3   |
:----------------------------|--------|--------|--------|--------|
| T+A                        | 0.2916 | 0.3193 | 0.2898 | 0.3147 |
| T+A+K-pres                 | 0.2999 | 0.3276 | 0.3004 | 0.3163 |
| T+A+K-abs                  | 0.3012 | 0.3425 | 0.2955 | 0.3102 |
| T+A+K                      | 0.3138 | 0.3517 | 0.3063 | 0.3300 |

## Analysis of query qrels

### Positive example

```
<top>
<num> Number: 110
<title>Visualization of information retrieval

<desc> Description:
Are there documents about systems supporting information retrieval with 
information visualization?

<narr> Narrative:
As information available through the Internet increases, the burden of
retrieving information becomes greater. There are limitations to the customary
method, which simply displays document titles agreeing with the retrieval query.
I want to survey papers about systems that reduce the burden on users by using
information visualization to realize efficient information retrieval. Even if a
paper does not discuss a retrieval system on networks, if it concerns systems
that support users visually, it is relevant.

</top>
```

| MAP 110                    | BM25   | +RM3   |
:----------------------------|--------|--------|
| T+A                        | 0.0896 | 0.0961 |
| T+A+K-pres                 | 0.0972 | 0.1014 |
| T+A+K-abs                  | 0.1127 | 0.1741 |
| T+A+K                      | 0.1179 | 0.1361 |


The `qrels` for query 110

```
110	A	gakkai-e-0000020424	1
110	A	gakkai-e-0000055960	1
110	A	gakkai-e-0000065393	1
110	A	gakkai-e-0000065523	1
110	S	gakkai-e-0000157334	1
110	S	gakkai-e-0000161414	1
110	A	gakkai-e-0000168539	1
110	A	gakkai-e-0000174697	1
110	A	gakkai-e-0000175574	1
110	A	gakkai-e-0000183376	1
110	A	gakkai-e-0000183392	1
110	A	gakkai-e-0000218302	1
110	A	gakkai-e-0000220027	1
110	A	gakkai-e-0000223246	1
110	A	gakkai-e-0000223257	1
110	A	gakkai-e-0000234076	1
110	S	gakkai-e-0000235917	1
110	S	gakkai-e-0000244185	1
110	A	gakkai-e-0000244244	1
110	A	gakkai-e-0000244630	1
110	A	gakkai-e-0000261275	1
110	A	gakkai-e-0000267360	1
110	A	gakkai-e-0000267361	1
110	A	gakkai-e-0000272373	1
110	A	gakkai-e-0000272608	1
110	A	gakkai-e-0000277464	1
110	A	gakkai-e-0000277465	1
110	A	gakkai-e-0000280233	1
110	A	gakkai-e-0000285940	1
110	A	gakkai-e-0000296390	1
110	S	gakkai-e-0000297914	1
110	A	gakkai-e-0000298291	1
110	A	gakkai-e-0000301384	1
110	A	gakkai-e-0000306600	1
110	A	gakkai-e-0000308233	1
110	A	gakkai-e-0000308240	1
110	S	gakkai-e-0000308291	1
110	A	gakkai-e-0000319396	1
110	A	gakkai-e-0000327172	1
110	A	gakkai-e-0001134897	1
110	A	gakkai-e-0001194867	1
110	A	gakkai-e-0001344684	1
110	A	gakkai-e-0001374800	1
110	A	gakkai-e-0001444561	1
110	A	gakkai-e-0001463592	1
110	A	gakkai-e-0001474251	1
110	A	gakkai-e-0001513245	1
110	S	gakkai-e-0001523276	1
110	A	gakkai-e-0001523445	1
110	S	gakkai-e-0001553175	1
110	S	gakkai-e-0001563275	1
110	A	gakkai-e-0001563545	1
110	A	gakkai-e-0001574295	1
110	A	gakkai-e-0001653046	1
110	A	gakkai-e-0001663055	1
110	A	gakkai-e-0001673555	1
110	A	gakkai-e-0001693216	1
110	A	gakkai-e-0001783875	1
110	A	gakkai-e-0001963103	1
110	A	kaken-e-1179524700	1
110	A	kaken-e-1519452200	1
```

The top 10 retrieved for query 110 with bm25 on t+a:

```
110 Q0 gakkai-e-0000283794 1 17.298000 Anserini
110 Q0 gakkai-e-0000301384 2 17.159201 Anserini X
110 Q0 gakkai-e-0001643545 3 16.988899 Anserini
110 Q0 gakkai-e-0001563545 4 16.684000 Anserini X
110 Q0 gakkai-e-0000261266 5 15.994500 Anserini
110 Q0 gakkai-e-0000320027 6 15.645400 Anserini
110 Q0 kaken-e-1179524700 7 15.414800 Anserini X
110 Q0 gakkai-e-0000223246 8 15.399300 Anserini X
110 Q0 gakkai-e-0000210337 9 15.136800 Anserini
110 Q0 gakkai-e-0000277714 10 14.859900 Anserini

map                   	110	0.0896
P_10                  	110	0.4000
```

The top 10 retrieved for query 110 with bm25 on t+a+k-pres:

```
110 Q0 gakkai-e-0000283794 1 17.394501 Anserini
110 Q0 gakkai-e-0000301384 2 17.234100 Anserini X
110 Q0 gakkai-e-0001563545 3 17.109100 Anserini X
110 Q0 gakkai-e-0001643545 4 17.064400 Anserini
110 Q0 kaken-e-1179524700 5 16.450899 Anserini X
110 Q0 gakkai-e-0000320027 6 16.077200 Anserini
110 Q0 gakkai-e-0000261266 7 15.979300 Anserini
110 Q0 gakkai-e-0000223246 8 15.490200 Anserini X
110 Q0 gakkai-e-0000277714 9 15.479500 Anserini
110 Q0 gakkai-e-0000210337 10 15.412300 Anserini

map                   	110	0.0972
P_10                  	110	0.4000
```

The top 10 retrieved for query 110 with bm25 on t+a+k-abs:

```
110 Q0 gakkai-e-0000283794 1 18.412300 Anserini
110 Q0 gakkai-e-0000301384 2 17.649401 Anserini X
110 Q0 gakkai-e-0001643545 3 16.970301 Anserini
110 Q0 gakkai-e-0001563545 4 16.399200 Anserini X
110 Q0 gakkai-e-0000261266 5 16.379601 Anserini
110 Q0 kaken-e-1179524700 6 15.970300 Anserini X
110 Q0 gakkai-e-0000320027 7 15.701600 Anserini
110 Q0 gakkai-e-0000223246 8 15.661400 Anserini X
110 Q0 gakkai-e-0000285939 9 15.637500 Anserini
110 Q0 gakkai-e-0000280233 10 15.395600 Anserini X

map                   	110	0.1127
P_10                  	110	0.5000
```

The top 10 retrieved for query 110 with bm25 on t+a+k:

```
110 Q0 gakkai-e-0000283794 1 18.498699 Anserini
110 Q0 gakkai-e-0000301384 2 17.713400 Anserini X
110 Q0 gakkai-e-0001643545 3 17.041901 Anserini
110 Q0 gakkai-e-0001563545 4 16.755501 Anserini X
110 Q0 kaken-e-1179524700 5 16.577299 Anserini X
110 Q0 gakkai-e-0000261266 6 16.372000 Anserini
110 Q0 gakkai-e-0000320027 7 16.036100 Anserini
110 Q0 gakkai-e-0000223246 8 15.805100 Anserini X
110 Q0 gakkai-e-0000285939 9 15.799000 Anserini
110 Q0 gakkai-e-0000254537 10 15.520000 Anserini

map                   	110	0.1179
P_10                  	110	0.4000
```

Let's look at `kaken-e-1179524700`:

```
<DOC>
<DOCNO>kaken-e-1179524700</DOCNO>
<TITLE>Multmedia Information Retrieval and Acquisition Interface with
       Interactive Information Visualization</TITLE>
<TEXT>We have developed new visual interaction techniques to obtain information
      from a very large and broad collection of data. Our techniques organize
      and visualize information dynamically, and navigate a user to explore the
      information space.First, We have developed a dynamic layout algorithm of
      documents and keywords and a visual interaction technique based on this
      algorithm to explore a large collection of documents. This algorithm,
      "forcedirected dynamic layout algorithm", introduces a spring model to
      represent the document space and lays out documents and keywords according
      to these relevance. By introducing dynamic and continuous manipulation of
      visualized data into the visual clustering, our technique enables a user
      to explore the information space according to his/her own point of view.
      We have implemented an experimental visualization system, dalled
      "DocSpace", based on our technique.Second, we have developed a visual
      interface for information mediating systems. There have been proposed
      "collaborative filtering" techniques that utilize recommendations of
      others to customize information filters. However, we need not only
      filtered data but also their relationships in the context of the whole
      information that has various trends of interests. We have therefore
      developed an information mediating system that vesualizes information
      space composed of reviewers and reviewed items. We have implemented the
      experimental system, "CinemaScape", that mediates movie reviews.</TEXT>
</DOC>
```

`absent` keyphrases are:

```
    User Interface / rel. term
    Retrieval Interface / rel. term
    Multimedia Information / pres. but OCR error in title
    Interactive System / general term
    Dynamic Querying / rel. term
```

`present` keyphrases are:

```
    Information Visualization / 
    Information Retrieval /
```

Let's look at `gakkai-e-0000280233`:

```
<DOC>
<DOCNO>gakkai-e-0000280233</DOCNO>
<TITLE>Visual Interaction for Exploration in Information Space of Documents</TITLE>
<TEXT>We propose a new visual interaction technique to handle document corpus. 
      The document corpus is visualized with a technique called "visual
      clustering" that layouts documents and, or keywords according to these
      relevance. By introducing dynamic and continuous manipulation of
      visualized data into the visual clustering, our technique enables a user
      to explore the information space according to his/her own point of view.
      In this paper, we describe our layout algorithm and visual operations
      provided for users. An example of visual interaction is demonstrated on
      our experimental system.</TEXT>
</DOC>
```

`absent` keyphrases are:

```
"Information Visualization"
"Information Retrieval"
"Browsing"
"Interactive Systems"
"User Interfaces"
"Graph Layout"
```

`present` keyphrases are:

```

```


### Negative example

```
<top>
<num> Number: 142
<title>Paraphrase

<desc> Description:
Papers which discuss paraphrasing

<narr> Narrative:
I want papers written about paraphrase, which is defined as the transformation 
of an expression to a different one with the same meaning in the same language.
Paraphrase includes not only syntactical transformation but also morphological
or semantic transformation in which derivatives or synonyms appear. Further,
paraphrase is not necessarily a transformation to a simpler expression. A paper
written about the application of paraphrase also satisfies this retrieval
request.

</top>
```

| MAP 142                    | BM25   | +RM3   |
:----------------------------|--------|--------|
| T+A                        | 0.3228 | 0.3883 |
| T+A+K-pres                 | 0.3171 | 0.3453 |
| T+A+K-abs                  | 0.3228 | 0.3882 |
| T+A+K                      | 0.3172 | 0.3465 |

### Absent keyphrases fine-grained analysis

```bash
# python3 src/analyse_abs.py data/docs/ntcir-2-t+a+k/ntc2-e1k.gz
present: 0.6324005199403194
absent: 0.3675994800596655
|-> case 1 (all words): 0.128646918207218
|-> case 2 (some words): 0.15413770290430115
|-> case 3 (no words): 0.08481485894812896
nb_documents_with_kps: 57443
sum_ratio_present_kps: 36326.98306693177
sum_ratio_absent_kps: 21116.016933067363
sum_ratio_absent_kps_case_1: 7389.864922577222
sum_ratio_absent_kps_case_2: 8854.13206793177
sum_ratio_absent_kps_case_3: 4872.019942557372

# python3 src/analyse_abs.py data/docs/ntcir-2-t+a+k/ntc2-e1g.gz
present: 0.6390988530847473
absent: 0.36090114691527664
|-> case 1 (all words): 0.09130742069367455
|-> case 2 (some words): 0.1609295909431814
|-> case 3 (no words): 0.10866413527837987
nb_documents_with_kps: 75081
sum_ratio_present_kps: 47984.18098845591
sum_ratio_absent_kps: 27096.819011545886
sum_ratio_absent_kps_case_1: 6855.452453101779
sum_ratio_absent_kps_case_2: 12082.754617605004
sum_ratio_absent_kps_case_3: 8158.611940836039

# python3 src/analyse_abs.py data/docs/ntcir-2-t+a+k/ntc1-e1.gz
present: 0.6290909780987732
absent: 0.37090902190138064
|-> case 1 (all words): 0.09813755384356208
|-> case 2 (some words): 0.16533998469984915
|-> case 3 (no words): 0.10743148335809942
nb_documents_with_kps: 185060
sum_ratio_present_kps: 116419.57640695898
sum_ratio_absent_kps: 68640.4235930695
sum_ratio_absent_kps_case_1: 18161.3357142896
sum_ratio_absent_kps_case_2: 30597.81756855408
sum_ratio_absent_kps_case_3: 19881.270310249878

# stats for ALL
present:  63.2  200729 / 317584 
absent: 36.8 116852 / 317584
sum_ratio_absent_kps_case_1: 10.2 (all words)
sum_ratio_absent_kps_case_2: 16.3 (some words)
sum_ratio_absent_kps_case_3: 10.3 (no words)

# python3 src/analyse_abs.py data/docs/ntcir-2-t+a+s2s-copy-top5-all/ntc2-e1k.gz
present: 0.9945781562255838
absent: 0.005421843774437244
|-> case 1 (all words): 0.0036701711703883383
|-> case 2 (some words): 0.001167781736032677
|-> case 3 (no words): 0.000583890868016334
nb_documents_with_kps: 57545
sum_ratio_present_kps: 57233.000000001215
sum_ratio_absent_kps: 311.99999999999125
sum_ratio_absent_kps_case_1: 211.19999999999692
sum_ratio_absent_kps_case_2: 67.2000000000004
sum_ratio_absent_kps_case_3: 33.599999999999945

# python3 src/analyse_abs.py data/docs/ntcir-2-t+a+s2s-copy-top5-all/ntc1-e1.gz
present: 0.9831739532496944
absent: 0.016826046750300576
|-> case 1 (all words): 0.005014993665777932
|-> case 2 (some words): 0.007362664970414383
|-> case 3 (no words): 0.004448388114112468
nb_documents_with_kps: 187079
sum_ratio_present_kps: 183931.19999999958
sum_ratio_absent_kps: 3147.7999999994813
sum_ratio_absent_kps_case_1: 938.2000000000697
sum_ratio_absent_kps_case_2: 1377.4000000001524
sum_ratio_absent_kps_case_3: 832.2000000000463

# python3 src/analyse_abs.py data/docs/ntcir-2-t+a+s2s-copy-top5-all/ntc2-e1g.gz
present: 0.9924192527734113
absent: 0.007580747226634585
|-> case 1 (all words): 0.004150685108416191
|-> case 2 (some words): 0.0024537341960145917
|-> case 3 (no words): 0.0009763279222037176
nb_documents_with_kps: 77433
sum_ratio_present_kps: 76846.00000000355
sum_ratio_absent_kps: 586.9999999999958
sum_ratio_absent_kps_case_1: 321.39999999999094
sum_ratio_absent_kps_case_2: 189.99999999999787
sum_ratio_absent_kps_case_3: 75.60000000000046
```



