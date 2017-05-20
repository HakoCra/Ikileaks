from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ikili/$', views.IkiliCreate.as_view(), name='ikili_create'),
    url(r'^login/$', views.twitter_login, name='login'),
    url(r'^callback/twitter$', views.twitter_callback, name='callback'),
]