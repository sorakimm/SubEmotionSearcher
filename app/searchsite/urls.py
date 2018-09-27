from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    # url(r'^searchsite/(?P<emotion>\w+)$', views.search_list, name='search_list'),
    # url(r'^search/(?P<emotion>\w+)/$', views.emotion_search_list, name='search_list'),
    # url(r'^search/term/$', views.term_search_list, name='term_search'),

    url(r'^search/emotion/(?P<emotion>\w+)/$', views.emotion_search_list, name='emotion_search_list'),
    url(r'^search/term/$', views.term_search_list, name='search_list'),
]