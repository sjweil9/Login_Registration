from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/add', views.addquote),
    url(r'^/favorite/(?P<quoteid>\d+)', views.favorite),
    url(r'^/unfavorite/(?P<quoteid>\d+)', views.unfavorite),
    url(r'^', views.index)
]