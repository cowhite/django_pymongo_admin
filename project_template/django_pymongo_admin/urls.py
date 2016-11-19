from django.conf.urls import url

from .decorators import superuser_required
from .views import *


urlpatterns = [
    url(r'^$', superuser_required(HomeView.as_view()), name="home"),
    url(r'^collections/(?P<collection>[\w.]+)/$',
        superuser_required(CollectionView.as_view()),
        name="collection"),
]