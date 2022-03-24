# Configure text analysis
원본 문서, https://www.elastic.co/guide/en/elasticsearch/reference/current/configure-text-analysis.html

기본으로 Elasticsearch는 [`standard` analyzer][1] 를 사용한다.  
그 외에 많은 [built-in analyzer][2] 가 있고, 별도의 설정없이 사용할 수 있다.  
맘에 드는 built-in analyzer가 없다면 custom analyzer 를 만들어 사용할 수 있다.  

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


## Create a custom analyzer

## Specify an analyzer




[1]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-analyzer.html "Standard analyzer"
[2]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html "Built-in analyzer reference"