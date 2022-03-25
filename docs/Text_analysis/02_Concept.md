# Text analysis Concepts
- [Anatomy of an analyzer](#anatomy-of-an-analyzer)
- [Index and search analysis](#index-ans-search-analysis)
- [Stemming](#stemming)
- [Token graphs](#token-graphs)

## Anatomy of an analyzer
공식 문서, https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer-anatomy.html

- character filters : 문자변환, 더하기 빼기 바꾸기 등을 통해
  + 예) Hindu-Arabic numerals (٠١٢٣٤٥٦٧٨٩) => Arabic-Latin equivalents (0123456789)
  + 예) strip HTML elements like `<b>` from the stream
  + Analyzer에 적용하지 않거나, 하나 이상을 적용할 순서대로 등록할 수 있다.

- tokenizers : 문자 쪼개기aa
  + 쪼개는 방식에 대한 방법들 
  + 예) `whitespace` tokenizer : "Quick brown fox!" => [Quick, brown, fox!]
  + Analyzer에 단 하나의 tokenizer 를 반드시 등록해야 한다.

- token filters
  + tokenizer 에서 입력된 token 을 추가, 제거, 변환한다.
  + 예) `lowercase` : 모든 문자 소문자로 변환
  + 예) `stop` : remove common words (stop words) like 'the' 
  + 예) `synonym` : 동의어 처리  
  + Analyzer에 적용하지 않거나, 하나 이상을 적용할 순서대로 등록할 수 있다.

## Index ans search analysis
공식 문서, https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-index-search-time.html

Index에 사용되는 analyzer 와 query(search)에 사용되는 analyzer 가 같을 경우, 다를 경우에 대한 내용


## Stemming
**어간 추출**

> 어간 : 활용어가 활용할 때에 변하지 않는 부분

공식 문서, https://www.elastic.co/guide/en/elasticsearch/reference/current/stemming.html  
참고: https://wikidocs.net/21707 

Stemming 은 단어를 어근 형태로 줄이는 과정입니다. 이렇게 하면 검색 중에 단어의 변형이 일치하는지 확인할 수 있습니다.  

예) walking, walked => walk  

### Stemmer token filters
In Elasticsearch, stemming is handled by stemmer token filters.

- Algorithmic stemmers, which stem words based on a set of rules
- Dictionary stemmers, which stem words by looking them up in a dictionary

stemming 은 token 을 변경하기 때문에, index와 search 에 동일한 stemmer token filter 를 사용하길 추천한다.

### Algorithmic stemmers
- `stemmer`, which provides algorithmic stemming for several languages, some with additional variants.
- `kstem`, a stemmer for English that combines algorithmic stemming with a built-in dictionary.
- `porter_stem`, our recommended algorithmic stemmer for English.
- `snowball`, which uses Snowball-based stemming rules for several languages.

> 대부분 라틴어 계열만 지원

### Dictionary stemmers
이론적으로, dictionary stemmers 는 다음과 같은 경우에 적합하다:

- 불규칙한 단어의 어간
- 철자가 비슷하지만 개념적으로 관련이 없는 단어를 식별, 예를 들면:  
  + `organ` and `organization`  
  + `broker` and `broken`

You can use the `hunspell` token filter to perform dictionary stemming.

> If available, we recommend trying an algorithmic stemmer for your language before using the `hunspell` token filter.

### Control stemming
때때로, stemming 은 철자가 비슷하지만 개념적으로 관련없는 공유 root words 를 생성할 수 있다.  
예를 들면, `skies`(하늘) 과 `skiing`(스키) 은 모두 같은 root word 인 `ski`로  줄일 수 있다.

이를 방지하고 stemming을 더 잘 제어하기 위해 다음 토큰 필터를 사용할 수 있습니다.

- `stemmer_override`, which lets you define rules for stemming specific tokens.
- `keyword_marker`, which marks specified tokens as keywords. Keyword tokens are not stemmed by subsequent stemmer token filters.
- `conditional`, which can be used to mark tokens as keywords, similar to the keyword_marker filter.

For built-in [language analyzers][1], you also can use the `stem_exclusion` parameter to specify a list of words that won’t be stemmed.


## Token graphs
공식 문서, https://www.elastic.co/guide/en/elasticsearch/reference/current/token-graphs.html

Tokenizer는 텍스트를 토큰 스트림으로 변환할 때 다음도 기록한다:

- The **position** of each token in the stream
- The **positionLength**, the number of positions that a token spans

이를 이용해서 *토큰 그래프*라고 하는 [방향성 비순환 그래프][2]를 생성할 수 있습니다.  

![](https://www.elastic.co/guide/en/elasticsearch/reference/current/images/analysis/token-graph-qbf-ex.svg)

### Synonyms
몇몇 token filter 는 기존의 token stream 에 새로운 토큰을 추가할 수 도 있다.  

![](https://www.elastic.co/guide/en/elasticsearch/reference/current/images/analysis/token-graph-qbf-synonym-ex.svg)

### Multi-position tokens
일부 토큰 필터는 여러 위치에 걸쳐 있는 토큰을 추가할 수 있습니다. These can include tokens for multi-word synonyms, such as using "atm" as a synonym for "automatic teller machine."

However, only some token filters, known as graph token filters, accurately record the positionLength for multi-position tokens. This filters include:

- [synonym_graph][3]
- [word_delimiter_graph][4]

[nori_tokenizer][5]와 같은 일부 토크나이저는 복합 토큰을 다중 위치 토큰으로 정확하게 분해합니다.

In the following graph, 'domain name system' and its synonym, 'dns', both have a position of 0.  
However, 'dns' has a 'positionLength' of **3**. Other tokens in the graph have a default 'positionLength' of **1**.

![](https://www.elastic.co/guide/en/elasticsearch/reference/current/images/analysis/token-graph-dns-synonym-ex.svg)

### Using token graphs for search
Indexing은 positionLength 속성을 무시하고 다중 위치 토큰이 포함된 토큰 그래프를 지원하지 않습니다.  

그러나 `match` 또는 `match_phrase` 쿼리와 같은 쿼리는 이러한 그래프를 사용하여 단일 쿼리 문자열에서 여러 하위 쿼리를 생성할 수 있습니다.  

#### 예제
A user runs a search for the following phrase using the `match_phrase` query: 

`domain name system is fragile`  

During search analysis, 'dns', a synonym for 'domain name system', is added to the query string’s token stream. The dns token has a positionLength of 3.  

![](https://www.elastic.co/guide/en/elasticsearch/reference/current/images/analysis/token-graph-dns-synonym-ex.svg)  

The match_phrase query uses this graph to generate sub-queries for the following phrases:

```
dns is fragile
domain name system is fragile
```

This means the query matches documents containing either dns is fragile or domain name system is fragile.


### Invalid token graphs
he following token filters can add tokens that span multiple positions but only record a default positionLength of 1:  

- synonym
- word_delimiter

This means these filters will produce invalid token graphs for streams containing such tokens.

In the following graph, dns is a multi-position synonym for domain name  
system. However, dns has the default positionLength value of 1, resulting in an invalid graph.  
![](https://www.elastic.co/guide/en/elasticsearch/reference/current/images/analysis/token-graph-dns-invalid-ex.svg)







[1]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-lang-analyzer.html "Elasticsearch Guide [8.1] » Text analysis » Built-in analyzer reference » Language analyzers"
[2]: https://en.wikipedia.org/wiki/Directed_acyclic_graph "Directed acyclic graph"
[3]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-graph-tokenfilter.html "Synonym graph token filter"
[4]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-word-delimiter-graph-tokenfilter.html "Word delimiter graph token filter"
[5]: https://www.elastic.co/guide/en/elasticsearch/plugins/8.1/analysis-nori-tokenizer.html "nori_tokenizer"