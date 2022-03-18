from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json

es = Elasticsearch( 
        'https://localhost:9200',
        # api_key=('-cN1kX8BAaFJSMrVR1f_','Ax84KJycSCG3fXU-VIs_BQ'), # Home Version
        # api_key=('bJu3i38B0jTokFLxBNhe','i1uzK3elTVSpZhakFD8vnw'), # Office Version
        basic_auth=('pyagent','pyagentpw'),
        ca_certs=r'D:\ES\elasticsearch-8.1.0\config\certs\http_ca.crt',
)

index_name = 'fest-index'
mapping = None

# with open('mapping.json', 'r', encoding='utf-8') as fd:
#     mapping = json.load(fd)

if es.indices.exists(index=index_name):
    print(index_name, "index exists.")
else:
    es.indices.create(
        index=index_name,
        mappings = mapping,
    )
    print(index_name, 'index is created.')


def yield_data():
    global index_name
    
    with open('전국문화축제표준데이터.json','r', encoding='utf-8') as fd:
        jdat = json.load(fd)['records']
    
    for i in jdat:
        yield {
            "_index": index_name,
            "_source": i,
        }

# helpers.bulk(es, yield_data())