from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from searchsite import models
import json
import requests


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


# def search(emotion):
#     s = Search().filter('term', emotion=emotion)
#     response = s.execute()
#     return response

def search(mode, term):
    query = json.dumps({
        "query":{
            "match":{
                mode:term
            }
        }
    })
    es = Elasticsearch()
    results = es.search(index='sub-index', body=query, size=1000)
    return results

def format_results(results):
    data = [doc for doc in results['hits']['hits']]
    result_list = []
    # doc_dic = {'smi_filename': '', 'emotion': '', 'eng_sentence': '', 'kor_sentence': ''}
    for doc in data:
        doc_dic={}
        doc_dic['smi_filename'] = doc['_source']['smi_filename']
        doc_dic['emotion'] = doc['_source']['emotion']
        doc_dic['eng_sentence'] = doc['_source']['eng_sentence']
        doc_dic['kor_sentence'] = doc['_source']['kor_sentence']
        result_list.append(doc_dic)
        # print("%s" % (doc['_source']['smi_filename']))
        # print("%s" % (doc['_source']['eng_sentence']))
        # print("%s" % (doc['_source']['kor_sentence']))

    return result_list


# def format_results(results):
#     data = [doc for doc in results['hits']['hits']]
#     for doc in data:
#         print("%s) %s" % (doc['_id'], doc['_source']['eng_sentence']))
