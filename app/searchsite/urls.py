from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    # url(r'^searchsite/(?P<emotion>\w+)$', views.search_list, name='search_list'),
    url(r'^search/(?P<emotion>\w+)/$', views.search_list, name='search_list'),
]