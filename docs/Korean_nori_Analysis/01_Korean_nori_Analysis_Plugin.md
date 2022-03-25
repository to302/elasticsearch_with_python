# Korean (nori) Analysis Plugin
공식 문서 : https://www.elastic.co/guide/en/elasticsearch/plugins/8.1/analysis-nori.html

It uses the [mecab-ko-dic dictionary](https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/) . 

## Installation
```
bin/elasticsearch-plugin install analysis-nori
```

## Removal
```
bin/elasticsearch-plugin remove analysis-nori
```

## `nori` analyzer
아래와 같이 tokenizer 와 token filters 를 가지고 있다:

- [`nori_tokenizer`][1]
- [`nori_part_of_speech`][2] token filter
- [`nori_readingform`][3] token filter
- [`nori_number`][4] token filter

[`nori_tokenizer`][1] 는 `decompound_mode` 와 `user_dictionary` 설정을 가지고 있고,  
[`nori_part_of_speech`][2] 는 `stoptags` 설정을 가지고 있다.


## `nori_tokenizer
공식 문서, https://www.elastic.co/guide/en/elasticsearch/plugins/8.1/analysis-nori-tokenizer.html  

### 가용한 설정

#### `decompound_mode`  
The decompound mode determines how the tokenizer handles compound tokens. It can be set to:

+ `none`  
  No decomposition for compounds. Example output:  
  
  가거도항  
  가곡역  

+ `discard`  
  Decomposes compounds and discards the original form (default). Example output:  
  
  가곡역 => 가곡, 역

+ `mixed`  
  Decomposes compounds and keeps the original form. Example output:
  
  가곡역 => 가곡역, 가곡, 역

#### `discard_punctuation`
Whether punctuation should be discarded from the output. Defaults to `true`.  

#### `user_dictionary`  
The Nori tokenizer uses the mecab-ko-dic dictionary by default. A `user_dictionary` with custom nouns (`NNG`) may be appended to the default dictionary. The dictionary should have the following format:

```
<token> [<token 1> ... <token n>]
```

The first token is mandatory and represents the custom noun that should be added in the dictionary. For compound nouns the custom segmentation can be provided after the first token (`[<token 1> ... <token n>]`). The segmentation of the custom compound nouns is controlled by the decompound_mode setting.

As a demonstration of how the user dictionary can be used, save the following dictionary to `$ES_HOME/config/userdict_ko.txt`:  

```
c++
C샤프
세종
세종시 세종 시
```

Then create an analyzer as follows:  

```
PUT nori_sample
{
  "settings": {
    "index": {
      "analysis": {
        "tokenizer": {
          "nori_user_dict": {
            "type": "nori_tokenizer",
            "decompound_mode": "mixed",
            "discard_punctuation": "false",
            "user_dictionary": "userdict_ko.txt"
          }
        },
        "analyzer": {
          "my_analyzer": {
            "type": "custom",
            "tokenizer": "nori_user_dict"
          }
        }
      }
    }
  }
}

GET nori_sample/_analyze
{
  "analyzer": "my_analyzer",
  "text": "세종시"  
}
```

다음과 같은 결과가 나온다.   

```
{
  "tokens" : [ {
    "token" : "세종시",
    "start_offset" : 0,
    "end_offset" : 3,
    "type" : "word",
    "position" : 0,
    "positionLength" : 2    
  }, {
    "token" : "세종",
    "start_offset" : 0,
    "end_offset" : 2,
    "type" : "word",
    "position" : 0
  }, {
    "token" : "시",
    "start_offset" : 2,
    "end_offset" : 3,
    "type" : "word",
    "position" : 1
   }]
}
```

#### `user_dictionary_rules`
You can also inline the rules directly in the tokenizer definition using the `user_dictionary_rules` option:

```
PUT nori_sample
{
  "settings": {
    "index": {
      "analysis": {
        "tokenizer": {
          "nori_user_dict": {
            "type": "nori_tokenizer",
            "decompound_mode": "mixed",
            "user_dictionary_rules": ["c++", "C샤프", "세종", "세종시 세종 시"]
          }
        },
        "analyzer": {
          "my_analyzer": {
            "type": "custom",
            "tokenizer": "nori_user_dict"
          }
        }
      }
    }
  }
}
```

### 부가적인 속성
The nori_tokenizer sets a number of additional attributes per token that are used by token filters to modify the stream. You can view all these additional attributes with the following request:

```
GET _analyze
{
  "tokenizer": "nori_tokenizer",
  "text": "뿌리가 깊은 나무는",   
  "attributes" : ["posType", "leftPOS", "rightPOS", "morphemes", "reading"],
  "explain": true
}
```

```
{
  "detail": {
    "custom_analyzer": true,
    "charfilters": [],
    "tokenizer": {
      "name": "nori_tokenizer",
      "tokens": [
        {
          "token": "뿌리",
          "start_offset": 0,
          "end_offset": 2,
          "type": "word",
          "position": 0,
          "leftPOS": "NNG(General Noun)",
          "morphemes": null,
          "posType": "MORPHEME",
          "reading": null,
          "rightPOS": "NNG(General Noun)"
        },
        {
          "token": "가",
          "start_offset": 2,
          "end_offset": 3,
          "type": "word",
          "position": 1,
          "leftPOS": "J(Ending Particle)",
          "morphemes": null,
          "posType": "MORPHEME",
          "reading": null,
          "rightPOS": "J(Ending Particle)"
        },
        {
          "token": "깊",
          "start_offset": 4,
          "end_offset": 5,
          "type": "word",
          "position": 2,
          "leftPOS": "VA(Adjective)",
          "morphemes": null,
          "posType": "MORPHEME",
          "reading": null,
          "rightPOS": "VA(Adjective)"
        },
        {
          "token": "은",
          "start_offset": 5,
          "end_offset": 6,
          "type": "word",
          "position": 3,
          "leftPOS": "E(Verbal endings)",
          "morphemes": null,
          "posType": "MORPHEME",
          "reading": null,
          "rightPOS": "E(Verbal endings)"
        },
        {
          "token": "나무",
          "start_offset": 7,
          "end_offset": 9,
          "type": "word",
          "position": 4,
          "leftPOS": "NNG(General Noun)",
          "morphemes": null,
          "posType": "MORPHEME",
          "reading": null,
          "rightPOS": "NNG(General Noun)"
        },
        {
          "token": "는",
          "start_offset": 9,
          "end_offset": 10,
          "type": "word",
          "position": 5,
          "leftPOS": "J(Ending Particle)",
          "morphemes": null,
          "posType": "MORPHEME",
          "reading": null,
          "rightPOS": "J(Ending Particle)"
        }
      ]
    },
    "tokenfilters": []
  }
}
```

## `nori_part_of_speech` token filter
`nori_part_of_speech` token filter 는 품사 태그(POS Tags: part-of-speech tags) 세트와 일치하는 토큰을 제거한다.  
지원되는 태그 목록과 그 의미는 여기에서 확인할 수 있다: [Part of speech tags][5]  

### '품사 태그' 참고 사이트
- [mecab-ko, 세종 품사 태그][8]
- [한국어 형태소 품사(Part Of Speech, POS) 태그표][6]  
- [세종 품사 태그 설명][7]

### 가용 설정

#### `stoptags`  
An array of part-of-speech tags that should be removed.  

##### 기본값
```
"stoptags": [
    "E",
    "IC",
    "J",
    "MAG", "MAJ", "MM",
    "SP", "SSC", "SSO", "SC", "SE",
    "XPN", "XSA", "XSN", "XSV",
    "UNA", "NA", "VSV"
]
```

| 태그 | Description        | 설명                 |
|------|--------------------|----------------------|
| E    | Verbal endings     | 어미                 |
| IC   | Interjection       | 감탄사               |
| J    | Ending Particle    | 조사                 |
| MAG  | General Adverb     | 일반 부사            |
| MAJ  | Conjunctive adverb | 접속 부사            |
| MM   | Determiner         | 관형사               |
| SP   | Space              |                      |
| SSC  | Closing brackets   | 닫힘 괄호            |
| SSO  | Opening brackets   | 열림 괄호            |
| SC   | Separator (· / :)  | 가운데점, 빗금, 콜론 |
| SE   | Ellipsis           | 줄임표               |
| XPN  | Prefix             | 체언 접두사          |
| XSA  | Adjective Suffix   | 형용사 파생 접미사   |
| XSN  | Noun Suffix        | 명사 파생 접미사     |
| XSV  | Verb Suffix        | 동사 파생 접미사     |
| UNA  | Unknown            |                      |
| NA   | Unknown            | 분석불능범주         |
| VSV  | Unknown            |                      |


##### 예제

```
PUT nori_sample
{
  "settings": {
    "index": {
      "analysis": {
        "analyzer": {
          "my_analyzer": {
            "tokenizer": "nori_tokenizer",
            "filter": [
              "my_posfilter"
            ]
          }
        },
        "filter": {
          "my_posfilter": {
            "type": "nori_part_of_speech",
            "stoptags": [
              "NR"   
            ]
          }
        }
      }
    }
  }
}

GET nori_sample/_analyze
{
  "analyzer": "my_analyzer",
  "text": "여섯 용이"  
}
```

Korean numerals should be removed (NR)  

```
{
  "tokens" : [ {
    "token" : "용",
    "start_offset" : 3,
    "end_offset" : 4,
    "type" : "word",
    "position" : 1
  }, {
    "token" : "이",
    "start_offset" : 4,
    "end_offset" : 5,
    "type" : "word",
    "position" : 2
  } ]
}
```


## `nori_readingform` token filter
한자를 한글로 변환한다.  

```
PUT nori_sample
{
  "settings": {
    "index": {
      "analysis": {
        "analyzer": {
          "my_analyzer": {
            "tokenizer": "nori_tokenizer",
            "filter": [ "nori_readingform" ]
          }
        }
      }
    }
  }
}

GET nori_sample/_analyze
{
  "analyzer": "my_analyzer",
  "text": "鄕歌"      
}
```

```
{
  "tokens" : [ {
    "token" : "향가",     
    "start_offset" : 0,
    "end_offset" : 2,
    "type" : "word",
    "position" : 0
  }]
}
```

## `nori_number token` filter
The `nori_number` token filter normalizes Korean numbers to regular Arabic decimal numbers in half-width characters.

- 영영칠 → 7
- 일영영영 → 1000
- 삼천2백2십삼 → 3223
- 조육백만오천일 → 1000006005001
- ３.２천 → 3200
- １.２만３４５.６７ → 12345.67
- 4,647.100 → 4647.1
- 15,7 → 157 (be aware of this weakness)

[1]: https://www.elastic.co/guide/en/elasticsearch/plugins/8.1/analysis-nori-tokenizer.html "nori_tokenizer"
[2]: https://www.elastic.co/guide/en/elasticsearch/plugins/8.1/analysis-nori-speech.html "'nori_part_of_speech' token filter"
[3]: https://www.elastic.co/guide/en/elasticsearch/plugins/8.1/analysis-nori-readingform.html "'nori_readingform' token filter"
[4]: https://www.elastic.co/guide/en/elasticsearch/plugins/8.1/analysis-nori-number.html "'nori_number' token filter"
[5]: https://lucene.apache.org/core/9_0_0/analysis/nori/org/apache/lucene/analysis/ko/POS.Tag.html "Lucene 9.0.0 POS.Tag Enum Constant - Part of speech tag for Korean based on Sejong corpus classification."
[6]: http://kkma.snu.ac.kr/documents/?doc=postag "꼬꼬마 한국어 형태소 분석기, POS 태그표"
[7]: https://m.blog.naver.com/aramjo/221404487481 "세종 품사 태그 설명"
[8]: https://to302.tistory.com/19 "mecab-ko-dic, 세종 품사 태그 v2.0"

