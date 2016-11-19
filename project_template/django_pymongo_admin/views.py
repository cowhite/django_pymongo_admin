from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings
from django.core.urlresolvers import reverse

from bson.objectid import ObjectId

db = settings.MONGO_DB


class HomeView(TemplateView):
    '''
    Admin home - shows list of collections
    '''
    template_name = "django_pymongo_admin/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['collections'] = db.collection_names()
        return context


class CollectionView(TemplateView):
    '''
    Show records/rows in a collection
    '''
    template_name = "django_pymongo_admin/collection.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionView, self).get_context_data(*args, **kwargs)
        collection = db.get_collection(kwargs['collection'])
        collection_columns_record = db.collection_columns.find_one(
            {"name": kwargs['collection']})
        collection_columns = []
        if collection_columns_record:
            collection_columns = collection_columns_record['fields']

        search_dict = {}
        for column in collection_columns:
            if column in self.request.GET:
                val = self.request.GET.get(column, None)
                if val:
                    search_dict[column] = {
                        "$regex": val}

        q_main = collection.find(search_dict)
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


def object_view(request, collection, object_id):
    '''
    View Mongo record in JSON format
    '''
    collection = db.get_collection(collection)
    obj = collection.find_one({"_id": ObjectId(object_id)})
    obj["_id"] = object_id
    return JsonResponse(obj, safe=False)


def object_delete_view(request, collection, object_id):
    '''
    Delete Mongo Record
    Whether to actually delete or to set status as Deleted need to provided in
    settings
    '''
    if request.method == "POST":
        collection = db.get_collection(collection)
        obj = collection.delete_one({"_id": ObjectId(object_id)})
        return JsonResponse({"message": "Deleted successfully"})


def object_edit_view(request, collection, object_id):
    '''
    Edit Mongo Record
    '''
    collection_obj = db.get_collection(collection)
    obj = collection_obj.find_one({"_id": ObjectId(object_id)})
    if request.method == "GET":
        return render(
            request, "django_pymongo_admin/object_edit.html", {"obj": obj})
    if request.method == "POST":
        data_to_update = {}
        edited = False
        for key in obj:
            if key in request.POST and key != "_id":
                data_to_update[key] = request.POST[key]
                edited = True
        if edited:
            collection_obj.update(obj, data_to_update)
        return redirect(reverse(
            "django-pymongo-admin:object-view", args=[
                collection, object_id
            ]))

