# Elasticsearch with Django

## 환경
MS-Windows 10 Home

## 프로그램 설치
- Elasticsearch 8.1.0
- Kibana 8.1.0
- Python 패키지 Elasticsearch Client 8.1.0


## Elastic Stack 개요
> - https://www.elastic.co/kr/start
> - http://kimjmin.net/2022/02/2022-02-elastic-8-install/  

1. Download 'Elasticsearch'
2. Download 'Kibana'
3. Start Elasticsearch
   ```cmd
   bin\elasticsearch.bat
   ```
4. Start Kibana
   ```cmd
   bin\kibana.bat
   ```
5. Open Kibana  
   http://localhost:5601

  
### Elasticsearch 설치 경로 
> D:\bin\elasticsearch-8.1.0\  

환경변수 %ES_HOME% 로 설치 경로 등록   

### Kibana 설치 경로
> D:\bin\kibana-8.1.0\

### 참고 문서
- [Install Elasticsearch with `.zip` on Windows][1]  
- [Elastic 가이드 북][2]


## Elasticsearch 실행 메세지 
- 아래 실행 메세지 중에서 Kibana 에 대한 부분 확인 (enrollment token)
  + Kibana 초기 설정에 필요
- Kibana 에서 로그인 시 elastic 계정과 패스워드 사용 (아래 실행 메세지 참고)

```cmd
--------------------------------------------------------------------------------
-> Elasticsearch security features have been automatically configured!
-> Authentication is enabled and cluster connections are encrypted.

->  Password for the elastic user (reset with `bin/elasticsearch-reset-password -u elastic`):
  m*Ds1PqIVhugabHu1egF

->  HTTP CA certificate SHA-256 fingerprint:
  0370f93afacfbd830363261daad3f688cf8bae489841666d352743cab480aeea

->  Configure Kibana to use this cluster:
* Run Kibana and click the configuration link in the terminal when Kibana starts.
* Copy the following enrollment token and paste it into Kibana in your browser (valid for the next 30 minutes):
  eyJ2ZXIiOiI4LjEuMCIsImFkciI6WyIxOTIuMTY4LjIwLjU6OTIwMCJdLCJmZ3IiOiIwMzcwZjkzYWZhY2ZiZDgzMDM2MzI2MWRhYWQzZjY4OGNmOGJhZTQ4OTg0MTY2NmQzNTI3NDNjYWI0ODBhZWVhIiwia2V5IjoicEU3ZmJYOEIycGY2a0tZN2dFZkE6blNOcTJmbW1UMy1XbFAwWTB5Q1hsdyJ9

->  Configure other nodes to join this cluster:
* On this node:
  - Create an enrollment token with `bin/elasticsearch-create-enrollment-token -s node`.
  - Uncomment the transport.host setting at the end of config/elasticsearch.yml.
  - Restart Elasticsearch.
* On other nodes:
  - Start Elasticsearch with `bin/elasticsearch --enrollment-token <token>`, using the enrollment token that you generated.
```

### 실행 확인
```sh
curl --cacert %ES_HOME%\config\certs\http_ca.crt -u elastic https://localhost:9200 
```

- windows 10 의 cmd 콘솔창에서 curl 이용하니 오류발생. (7.79.1.0 version)  
  ```
  curl: (60) schannel: CertGetCertificateChain trust error CERT_TRUST_REVOCATION_STATUS_UNKNOWN
  More details here: https://curl.se/docs/sslcerts.html

  curl failed to verify the legitimacy of the server and therefore could not
  establish a secure connection to it. To learn more about this situation and
  how to fix it, please visit the web page mentioned above.
  ```


- Git Bash 창에서 실행하니 정상 (7.78.0 version)  
  ```
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100   536  100   536    0     0  14122      0 --:--:-- --:--:-- --:--:-- 14888{
    "name" : "KWAK-DELL7567",
    "cluster_name" : "elasticsearch",
    "cluster_uuid" : "iLtXFDzZTu-RQvSciYsftQ",
    "version" : {
      "number" : "8.1.0",
      "build_flavor" : "default",
      "build_type" : "zip",
      "build_hash" : "3700f7679f7d95e36da0b43762189bab189bc53a",
      "build_date" : "2022-03-03T14:20:00.690422633Z",
      "build_snapshot" : false,
      "lucene_version" : "9.0.0",
      "minimum_wire_compatibility_version" : "7.17.0",
      "minimum_index_compatibility_version" : "7.0.0"
    },
    "tagline" : "You Know, for Search"
  }
  ```

- windows 용으로 별도로 받아서 해도 정상적으로 보임
  + https://curl.se/
## Kibana 설정
> config/kibana.yml  

```yaml
# This section was automatically generated during setup.
elasticsearch.hosts: ['https://192.168.20.5:9200']
elasticsearch.serviceAccountToken: AAEAAWVsYXN0aWMva2liYW5hL2Vucm9sbC1wcm9jZXNzLXRva2VuLTE2NDY4MTYzNjA4NzE6cUphekdUeVlTcU9yRWVFUnp2RkhjUQ
elasticsearch.ssl.certificateAuthorities: ['D:\bin\kibana-8.1.0\data\ca_1646816361508.crt']
xpack.fleet.outputs: [{id: fleet-default-output, name: default, is_default: true, is_default_monitoring: true, type: elasticsearch, hosts: ['https://192.168.20.5:9200'], ca_trusted_fingerprint: 0370f93afacfbd830363261daad3f688cf8bae489841666d352743cab480aeea}]
```

## Kibana Dev Tools

### Data 입력
#### input 1
```
PUT /twitter/_doc/1
{
    "user": "kimchy",
    "post_date": "2018-11-15T13:12:00",
    "message": "김치가 맛있나요?"
}
```

#### output 1
```
{
  "_index" : "twitter",
  "_id" : "1",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 0,
  "_primary_term" : 1
}
```

#### input 2 / output 2 
**생략**

#### input 3
```
PUT /twitter/_doc/3
{
    "user": "elastic",
    "post_date": "2019-01-15T01:46:38",
    "message": "김치가 미국에서 인기인가요?"
}
```

#### output 3
```
{
  "_index" : "twitter",
  "_id" : "3",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 2,
  "_primary_term" : 1
}
```

### Data 조회
#### input 1
```
GET /twitter/_doc/3?pretty=true
```

#### output 1
```
{
  "_index" : "twitter",
  "_id" : "3",
  "_version" : 1,
  "_seq_no" : 2,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "user" : "elastic",
    "post_date" : "2019-01-15T01:46:38",
    "message" : "김치가 미국에서 인기인가요?"
  }
}
```

### Data 검색 - query 방식
#### input 1
```
GET /twitter/_search?q=user:kimchy&pretty=true
```

#### output 1
```
{
  "took" : 35,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 0.4700036,
    "hits" : [
      {
        "_index" : "twitter",
        "_id" : "1",
        "_score" : 0.4700036,
        "_source" : {
          "user" : "kimchy",
          "post_date" : "2018-11-15T13:12:00",
          "message" : "김치가 맛있나요?"
        }
      },
      {
        "_index" : "twitter",
        "_id" : "2",
        "_score" : 0.4700036,
        "_source" : {
          "user" : "kimchy",
          "post_date" : "2018-11-15T14:12:12",
          "message" : "김치는 건강에 좋은가요?"
        }
      }
    ]
  }
}
```

### Data 검색 - json 방식

#### input 1
```
GET /twitter/_search?pretty=true
{
    "query" : {
        "match" : { "user": "kimchy" }
    }
}
```

#### output 1
**위와 같은 결과**

### Data 검색 - wildcard 검색

#### input 1
```
GET /twitter/_search?pretty=true
{
    "query" : {
        "wildcard" : { "message": "*미국*" }
    }
}
```

#### output 1
```
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "twitter",
        "_id" : "3",
        "_score" : 1.0,
        "_source" : {
          "user" : "elastic",
          "post_date" : "2019-01-15T01:46:38",
          "message" : "김치가 미국에서 인기인가요?"
        }
      }
    ]
  }
}
```


## 실습
### 인덱스 설정 예
```
PUT drink
{
  "settings": {
    "index": {
        "number_of_shards": 3,
        "number_of_replicas": 1
    }
}
```

샤드의 개수를 3개로 정하고 복제본이 1개인 설정을 가진 drink 인덱스가 생성되었다.  
- 샤드 : 루씬의 단일 검색 인스턴스로 인덱스는 샤드 단위로 분리되어 각 노드에 분산 저장됨.  

현재는 노드당 하나의 샤드가 들어가도록 3개로 설정했다.  

### 분석기 설정
분석기가 있어야 우리가 원하는 형태의 색인이 가능하다. 정리, 색인할 때 특정한 규칙과 흐름에 의해 텍스트를 변경(토큰화)하는 과정을 분석(Analyze)이라고 하며, 해당 처리는 분석기(Analyzer)를 통해서 이루어진다. 프로젝트에선 한글명과 영문명 두 개의 필드를 비교하므로 각각 다른 분석기가 필요하다. 영어명 필드는 snowball 형태소 분석기를 사용하고 한글명 필드는 nori라는 토크나이저를 사용했다.

### 프로젝트 인덱스 세팅
```
PUT drink
{
  "settings": {
    "index": {
        "number_of_shards": 3,
        "number_of_replicas": 1
    }
    , 
    "analysis": {
      "analyzer": {
        "english_name_analyzer": {
          "type": "custom",
          "tokenizer": "whitespace",
          "filter": ["lowercase", "stop", "snowball"]
        }
        ,
        "nori_without_category_analyzer": {
          "type": "custom",
          "tokenizer": "nori_mixed",
          "filter": ["nori_filter", "category_stop_filter"]
        }
        ,
        "nori_with_category_analyzer": {
          "type": "custom",
          "tokenizer": "nori_mixed",
          "filter": ["nori_filter"]
        }
      }
      ,
      "tokenizer": {
        "nori_mixed": {
          "type": "nori_tokenizer",
          "decompound_mode": "mixed"
        }
      }
      ,
      "filter": {
          "nori_filter": {
            "type": "nori_part_of_speech",
            "stoptags": [
              "IC"
            ]
          }
          ,
          "category_stop_filter": {
            "type": "stop",
            "stopwords": [
              "소주", "맥주", "와인", "막걸리", "양주", "칵테일"
            ]
          }
        }
    }
  }
  ,
  "mappings": {
      "properties": {
        "id": {
          "type": "long"
        },
        "name": {
          "type": "text",
          "analyzer": "nori_without_category_analyzer"
        },
        "englishName": {
          "type": "text",
          "analyzer": "english_name_analyzer"
        },
        "category": {
          "type": "text",
          "analyzer": "nori_with_category_analyzer"
        }
    }
  }
}
```

### 검색쿼리
```
GET drink/_search
{
  "query": {
    "bool": {
      "should": [
        {
         "match_phrase": {
           "name": {
              "query": "금성맥주",
              "slop": 1,
              "boost": 2
            }
         } 
        }
        ,
        {
         "match_phrase": {
            "englishName": {
              "query": "금성맥주",
              "slop": 1,
              "boost": 2
            }
         } 
        }
        ,
        {
         "multi_match" : {
            "query": "금성맥주",
            "type": "best_fields",
            "fields": ["name", "englishName"],
            "tie_breaker": 0.3
          }
        }
        ,
        {
          "match": {
           "category": {
              "query": "금성맥주",
              "boost": 0.5
           }
          }  
        }
      ]
    }
  }
}
```

bool 복합 쿼리를 사용했다. 여러 조건들을 총합해서 검색하는 쿼리로 must, must_not, should, filter 가 있다. 자세한 설명은 아래 참고 자료 Elastic 가이드 북에 있다. 나는 원하는 조건을 맞추기 위해 위에서부터 조건에 맞으면 가중치를 주고 없으면 다음 조건으로 넘어가는 should를 사용했다. must일 시 조건에 해당하지 않으면 false를 반환해버려 A가 아니면 B라는 조건이 성립하지 않는다. 따로 or 조건을 걸어줄 수도 있지만 가중치 boost를 통해 score 조절을 해서 원하는 결과에 가까울수록 점수가 높아지도록 하고 싶었기 때문에 should를 사용했다.

> 출처 : [Elasticsearch - 1편][3]
## 참고 자료
- [AWS ElasticSearch 구축 및 기초 세팅](https://danidani-de.tistory.com/52), 2021. 4. 11.
- [Elasticsearch - 1편][3], 2021. 11. 2.
- [Elastic 가이드 북][2]



























## Python 패키지 설치
```cmd
pip install elasticsearch==8.1.0
```

### Elasticsearch Python Client
https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html

## Python 전체 패키지 업데이트
```
pip freeze > package.txt
pip install -r package.txt --upgrade
```

1. pip freeze > package.txt 로 패키지 전체 저장
2. package.txt 를 열어 == 부분을 >= 로 변경(Ctrl + h 후 변경)
3. pip install -r package.txt --upgrade 명령어 실행

---
[1]: https://www.elastic.co/guide/en/elasticsearch/reference/current/zip-windows.html "윈도우에서 Elasticsearch 설치"
[2]: https://esbook.kimjmin.net/ "Elastic 가이드 북 (한글)"
[3]: https://jujeol-jujeol.github.io/2021/11/02/Elasticsearch-1/ "Elasticsearch - 1편, 2021. 11. 2."
