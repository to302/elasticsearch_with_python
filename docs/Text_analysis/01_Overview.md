# Elasticsearch Text analysis
Read the [`README.md`](../README.md) first.

## 환경
- MS-Windows 10 
- CMD Console
- Elasticsearch 8.1.0
- Kibana 8.1.0

## 참고 
- Elasticsearch Guide [8.1]
  + Text analysis, https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html
- Elasticsearch Plugins and Integrations [8.1]
  + Analysis Plugins 
    * Korean (nori) Analysis Plugin, https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-nori.html

## 한글 분석기 Plug-in 설치
```cmd
cd d:\ES\elasticsearch-8.1.0
bin\elasticsearch-plugin install analysis-nori
```

### to read.
https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-overview.html