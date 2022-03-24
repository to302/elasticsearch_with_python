# Configure text analysis
원본 문서, https://www.elastic.co/guide/en/elasticsearch/reference/current/configure-text-analysis.html

기본으로 Elasticsearch는 [`standard` analyzer][1] 를 사용한다.  
그 외에 많은 [built-in analyzer][2] 가 있고, 별도의 설정없이 사용할 수 있다.  
맘에 드는 built-in analyzer가 없다면 custom analyzer 를 만들어 사용할 수 있다.  

- [Test an analyzer](#test-an-analyzer)
- [Configuring built-in analyzers](#configuring-built-in-analyzers)
- [Create a custom analyzer](#create-a-custom-analyzer)
- [Specify an analyzer](#specify-an-analyzer)

## Test an analyzer

### built-in analyzer
```
POST _analyze
{
  "analyzer": "whitespace",
  "text":     "The quick brown fox."
}
```

### combination of component below:
- A tokenizer
- Zero or more token filters
- Zero or more character filters

```
POST _analyze
{
  "tokenizer": "standard",
  "filter":  [ "lowercase", "asciifolding" ],
  "text":      "Is this déja vu?"
}
```

### custom analyzer 
```
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "std_folded": { 
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "asciifolding"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "my_text": {
        "type": "text",
        "analyzer": "std_folded" 
      }
    }
  }
}

GET my-index-000001/_analyze 
{
  "analyzer": "std_folded", 
  "text":     "Is this déjà vu?"
}

GET my-index-000001/_analyze 
{
  "field": "my_text", 
  "text":  "Is this déjà vu?"
}
```

## Configuring built-in analyzers
built-in analyzer 는 바로 사용할 수 있지만, 몇 가지 옵션 구성을 통해 변화를 꾀할 수 있다.  
예를 들어 `standard` analyzer 에 stop words 목록을 지원하도록 구성할 수 있다.  

```
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "std_english": { 
          "type":      "standard",
          "stopwords": "_english_"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "my_text": {
        "type":     "text",
        "analyzer": "standard", 
        "fields": {
          "english": {
            "type":     "text",
            "analyzer": "std_english" 
          }
        }
      }
    }
  }
}

POST my-index-000001/_analyze
{
  "field": "my_text", 
  "text": "The old brown cow"
}

POST my-index-000001/_analyze
{
  "field": "my_text.english", 
  "text": "The old brown cow"
}
```

1. We define the `std_english` analyzer to be based on the `standard` analyzer, but configured to remove the pre-defined list of English stopwords.
2. The `my_text` field uses the `standard` analyzer directly, without any configuration. No stop words will be removed from this field. The resulting terms are: [ the, old, brown, cow ]
3. The `my_text.english` field uses the `std_english` analyzer, so English stop words will be removed. The resulting terms are: [ old, brown, cow ]


## Create a custom analyzer
아래의 적절한 조합을 통해서 custom analyzer 를 만들 수 있다:  

- zero or more character filters
- a tokenizer
- zero or more token filters.

### Configuration
custom analyzer 는 아래와 같은 parameters 를 취할 수 있다.

| parameter              | comment                                                           |
|------------------------|-------------------------------------------------------------------|
| type                   | Analyzer type. Accepts [built-in analyzer types][2]. For custom analyzers, use custom or omit this parameter.  |
| tokenizer              | A built-in or customised [tokenizer][3]. (Required)           |
| char_filter            | An optional array of built-in or customised [character filters][4].  |
| filter                 | An optional array of built-in or customised [token filters][5].  |
| position_increment_gap | When indexing an array of text values, Elasticsearch inserts a fake "gap" between the last term of one value and the first term of the next value to ensure that a phrase query doesnâ€™t match two terms from different array elements. Defaults to 100. See [`position_increment_gap`][6] for more.  |

### Example configuration
Read [this][7].

## Specify an analyzer




[1]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-analyzer.html "Standard analyzer"
[2]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html "Built-in analyzer reference"
[3]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html "Tokenizer reference"
[4]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-charfilters.html "Character filters reference"
[5]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenfilters.html "Token filter reference"
[6]: https://www.elastic.co/guide/en/elasticsearch/reference/current/position-increment-gap.html "Mapping Parameters >> position_increment_gap"
[7]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html#_example_configuration