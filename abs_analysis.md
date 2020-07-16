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



