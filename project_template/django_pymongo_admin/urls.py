from django.conf.urls import url

from .decorators import superuser_required
from .views import *


urlpatterns = [
    url(r'^$', superuser_required(HomeView.as_view()), name="home"),
    url(r'^collections/(?P<collection>[\w.]+)/$',
        superuser_required(CollectionView.as_view()),
        name="collection"),
    url(r'^collections/(?P<collection>[\w.]+)/objects/(?P<object_id>[\w]+)/$',
        superuser_required(object_view),
        name="object-view"),
    url(r'^collections/(?P<collection>[\w.]+)/objects/(?P<object_id>[\w]+)/edit/$',
        superuser_required(object_edit_view),
        name="object-edit"),
    url(r'^collections/(?P<collection>[\w.]+)/objects/(?P<object_id>[\w]+)/delete/$',
        superuser_required(object_delete_view),
        name="object-delete"),

]