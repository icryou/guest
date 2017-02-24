# coding:utf-8

from django.conf.urls import url
from sign import views_if



urlpatterns = [
    url(r'^add_event/', views_if.add_event, name='add_event'),
    url(r'^get_event_list/', views_if.get_event_list, name='get_event_list'),
]
