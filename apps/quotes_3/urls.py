from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^quotes$', views.quotes),
    url(r'^add_quote$', views.add_quote),
    url(r'^add_fave/(?P<quoteid>\d+)$', views.add_fave),
    url(r'^delete_fave/(?P<quoteid>\d+)$', views.delete_fave),
]
