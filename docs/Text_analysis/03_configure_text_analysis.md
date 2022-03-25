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
| position_increment_gap | When indexing an array of text values, Elasticsearch inserts a fake "gap" between the last term of one value and the first term of the next value to ensure that a phrase query doesn't match two terms from different array elements. Defaults to 100. See [`position_increment_gap`][6] for more.  |

### Example configuration
Read [this][7].

#### Example 1
```
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": {
          "type": "custom", 
          "tokenizer": "standard",
          "char_filter": [
            "html_strip"
          ],
          "filter": [
            "lowercase",
            "asciifolding"
          ]
        }
      }
    }
  }
}

POST my-index-000001/_analyze
{
  "analyzer": "my_custom_analyzer",
  "text": "Is this <b>déjà vu</b>?"
}
```

#### Example 2
```
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": { 
          "char_filter": [
            "emoticons"
          ],
          "tokenizer": "punctuation",
          "filter": [
            "lowercase",
            "english_stop"
          ]
        }
      },
      "tokenizer": {
        "punctuation": { 
          "type": "pattern",
          "pattern": "[ .,!?]"
        }
      },
      "char_filter": {
        "emoticons": { 
          "type": "mapping",
          "mappings": [
            ":) => _happy_",
            ":( => _sad_"
          ]
        }
      },
      "filter": {
        "english_stop": { 
          "type": "stop",
          "stopwords": "_english_"
        }
      }
    }
  }
}

POST my-index-000001/_analyze
{
  "analyzer": "my_custom_analyzer",
  "text": "I'm a :) person, and you?"
}
```

## Specify an analyzer

### index analyzer 를 결정하는 방법

1. The `analyzer` mapping parameter for the field. See Specify the analyzer for a field.
2. The `analysis.analyzer.default` index setting. See Specify the default analyzer for an index.

#### 1. Specify the analyzer for a field

```
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "whitespace"
      }
    }
  }
}
```

#### 2. Specify the default analyzer for an index
my-index-000001 index의 대체 분석기로 'simple' 분석기 설정 

```
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "default": {
          "type": "simple"
        }
      }
    }
  }
}
```

### query에 대한 search analyzer 지정
[full-text query][8]를 작성할 때, `analyzer` 파라메터를 이용해서 search analyzer를 특정할 수 있다. 이 파라메터가 지정되면 다른 analyzer 보다 우선 적용된다.  

아래 search API 에서 `stop` analyzer 를 `match` query 를 위한 search analyzer 로 사용하고 있다.

```
GET my-index-000001/_search
{
  "query": {
    "match": {
      "message": {
        "query": "Quick foxes",
        "analyzer": "stop"
      }
    }
  }
}
```

### field에 대한 search analyzer 지정
index를 mapping할 때, `search_analyzer` mapping 파라메터를 이용해서 각각의 text field 에 대한 search analyzer 를 지정할 수 있다.

**search analyzer가 지정되면 index analyzer 도 `analyzer` 파라메터로 반드시 같이 작성되어야 한다.**  

다음의 create index API 는 `simple` analyzer 를 `title` field 에 대한 search analyzer 로 설정하고 있다.

```
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "whitespace",
        "search_analyzer": "simple"
      }
    }
  }
}
```

### index의 기본 search analyzer 지정
index 를 생성할 때, `analysis.analyzer.default_search` 설정을 이용해 기본 search analyzer 를 지정할 수 있다.  

search analyzer 가 설정되면 `analysis.analyzer.default` 설정을 이용해 기본 index analyzer 도 반드시 같이 설정되어야 한다.  


```
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "default": {
          "type": "simple"
        },
        "default_search": {
          "type": "whitespace"
        }
      }
    }
  }
}
```


[1]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-analyzer.html "Standard analyzer"
[2]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html "Built-in analyzer reference"
[3]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html "Tokenizer reference"
[4]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-charfilters.html "Character filters reference"
[5]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenfilters.html "Token filter reference"
[6]: https://www.elastic.co/guide/en/elasticsearch/reference/current/position-increment-gap.html "Mapping Parameters >> position_increment_gap"
[7]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html#_example_configuration
[8]: https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html "Full text queries"
