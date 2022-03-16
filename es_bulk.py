from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json

es = Elasticsearch( 
    'https://localhost:9200',
    api_key=('-cN1kX8BAaFJSMrVR1f_','Ax84KJycSCG3fXU-VIs_BQ'),
    ca_certs=r'D:\ES\elasticsearch-8.1.0\config\certs\http_ca.crt',
)

index_name = 'fest-index'
mapping = None

with open('mapping.json', 'r', encoding='utf-8') as fd:
    mapping = json.load(fd)

if not es.indices.exists(index=index_name):
    es.indices.create(
        index=index_name,
        mappings = mapping,
    )
    print('index is created.')
else:
    print("index exists.")


def yield_data():
    with open('전국문화축제표준데이터.json','r', encoding='utf-8') as fd:
        jdat = json.load(fd)['records']
    
    for i in jdat[0:10]:
        yield {
            "_index": index_name,
            "_source": i,
        }

helpers.bulk(es, yield_data())