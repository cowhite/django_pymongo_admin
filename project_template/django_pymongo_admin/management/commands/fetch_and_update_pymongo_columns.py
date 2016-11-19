from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'Fetches fields/column names and stores in a separate collection'

    def add_arguments(self, parser):
        parser.add_argument('--collection')

    def handle(self, *args, **options):
        self.db = settings.MONGO_DB
        if options['collection']:
            self.update_fields(options['collection'])
        else:
            collections = self.db.collection_names()
            for collection in collections:
                self.update_fields(collection)

    def update_fields(self, collection):
        rows = self.db.get_collection(collection).find()
        columns = []
        for x in rows:
            keys = x.keys()
            for k in keys:
                if k not in columns:
                    columns.append(k)

        record = self.db.collection_columns.find_one({"name": collection})
        if not record:
            self.db.collection_columns.insert_one({
                "name": collection,
                "fields": columns
            })
        else:
            self.db.collection_columns.update(
                record,
                {
                    "name": collection,
                    "fields": columns
                })
