from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
   
es = Elasticsearch( 
        'https://localhost:9200',
        # api_key=('-cN1kX8BAaFJSMrVR1f_','Ax84KJycSCG3fXU-VIs_BQ'), # Home Version
        api_key=('bJu3i38B0jTokFLxBNhe','i1uzK3elTVSpZhakFD8vnw'), # Office Version
        ca_certs=r'D:\ES\elasticsearch-8.1.0\config\certs\http_ca.crt',
)

index_name = 'fest-index2'
mapping = None

if es.indices.exists(index=index_name):
    print(index_name, "index exists.")
else:
    es.indices.create(
        index=index_name,
        mappings = json.load(open('mapping.json', 'r', encoding='utf-8')),
        settings = json.load(open('settings.json', 'r', encoding='utf-8')),
    )
    print(index_name, 'index is created.')


def ckdata(jd: dict, key: str) -> str:
    """해당 key 유무 체크하여 정보가 없는 경우 ''를 반환"""
    if key in jd.keys():
        return jd[key]
    else:
        return ''


def yield_data():
    global index_name

    jdat = json.load(open('전국문화축제표준데이터.json','r', encoding='utf-8'))['records']
    for j in jdat[0:10]:
        yield {
            "_index": index_name,
            "_source": {
                            "name":j["축제명"],
                            "place":j["개최장소"],
                            "bdate":j["축제시작일자"],
                            "edate":j["축제종료일자"],
                            "event":j["축제내용"],
                            "managing":j["주관기관"],
                            "tel":ckdata(j, "전화번호"),
                            "web":ckdata(j, "홈페이지주소"),
                            "info":ckdata(j, "관련정보"),
                            "addr_road":ckdata(j, "소재지도로명주소"),
                            "addr_land":ckdata(j, "소재지지번주소"),
                            "location": {
                                "lat":j["위도"],
                                "lon":j["경도"],
                            },
                            "ref_date":j["데이터기준일자"],
                       },
        }


helpers.bulk(es, yield_data())
