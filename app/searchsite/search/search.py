from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from searchsite import models

connections.create_connection()

class SubIndex(DocType):
    smi_filename = Text()
    eng_sentence = Text()
    kor_sentence = Text()
    emotion = Text()
    crawled_date = Date()

    class Index:
        index = 'sub-index'
        name = 'sub-index'


def bulk_indexing():
    SubIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Sub.objects.all().iterator()))


def search(emotion):
    s = Search().filter('term', emotion=emotion)
    response = s.execute()
    return response