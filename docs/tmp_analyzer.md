## Anatomy of an analyzer
공식 문서, https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer-anatomy.html

- character filters : 문자변환, 더하기 빼기 바꾸기 등을 통해
  + 예) Hindu-Arabic numerals (٠‎١٢٣٤٥٦٧٨‎٩‎) => Arabic-Latin equivalents (0123456789)
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


## Stemming (어간 추출)
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








<base target='_blank'>

[1]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-lang-analyzer.html "Elasticsearch Guide [8.1] » Text analysis » Built-in analyzer reference » Language analyzers"
