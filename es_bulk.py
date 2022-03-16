from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json

es = Elasticsearch( # home version
    'https://localhost:9200',
    api_key=('-cN1kX8BAaFJSMrVR1f_', 'Ax84KJycSCG3fXU-VIs_BQ'),
    ssl_assert_fingerprint=('42376fbf31e025706536cfc90b7f530f01b0d172b0d57622d050d0fb158677bc')
)

index_name = 'fest-index'
mapping = None
with open('mapping.json', 'r', encoding='utf-8') as fd:
    mapping = json.load(fd)

if not es.indices.exists(index=index_name):
    es.indices.create(
        index = index_name,
        mappings = mapping,
    )


with open('전국문화축제표준데이터.json','r', encoding='utf-8') as fd:
    jstr = json.load(fd)['records']
    print(jstr[1])