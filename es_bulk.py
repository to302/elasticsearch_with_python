from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json

es = Elasticsearch( 
        'https://localhost:9200',
        api_key=('-cN1kX8BAaFJSMrVR1f_','Ax84KJycSCG3fXU-VIs_BQ'), # Home Version
        # ssl_assert_fingerprint="42376fbf31e025706536cfc90b7f530f01b0d172b0d57622d050d0fb158677bc",
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
    with open('전국문화축제표준데이터.json','r', encoding='utf-8') as fd:
        jdat = json.load(fd)['records']
    
    for i in jdat[0:10]:
        yield {
            "_index": index_name,
            "_source": i,
        }

# helpers.bulk(es, yield_data())