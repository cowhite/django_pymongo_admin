from django.shortcuts import render
from django.views.generic import TemplateView

from django.conf import settings

db = settings.MONGO_DB


class HomeView(TemplateView):
    template_name = "django_pymongo_admin/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['collections'] = db.collection_names()
        return context


class CollectionView(TemplateView):
    template_name = "django_pymongo_admin/collection.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionView, self).get_context_data(*args, **kwargs)
        collection = db.get_collection(kwargs['collection'])
        q_main = collection.find()
        page = self.request.GET.get('page')
        page_size = 3
        pages = q_main.count()/page_size

        try:
            page = int(page)
            if page > pages:
                q = q_main.skip((pages-1)*page_size).limit(page_size)
            else:
                q = q_main.skip((page-1)*page_size).limit(page_size)
        except TypeError:
            # If page is not an integer, deliver first page.
            page = 1
            q = q_main.limit(page_size)
        # except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            # q = q_main.skip((pages-1)*page_size).limit(page_size)
        context['page_size'] = page_size
        context['page'] = page
        context['total_count'] = pages
        fields = []
        for x in q:
            keys = x.keys()
            for k in keys:
                if k not in fields:
                    fields.append(k)

        q.rewind()
        context['rows'] = q
        context['fields'] = fields

        return context
