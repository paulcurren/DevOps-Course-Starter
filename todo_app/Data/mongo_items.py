from tokenize import String
from typing import Iterator

from bson import ObjectId
from todo_app.Data.item import Item
import logging

import pymongo
import os

log = logging.getLogger(__name__)

class MongoItems:

    def get_db(self):
        client = pymongo.MongoClient(os.environ['MONGODB_CONNECTION_STRING'])
        db = client['my_db']
        return db

    def change_status(self, id, status):
        self.get_db().collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {'$set':
                {'status': status}
            })

        log.info('change_status: id[%s] status[%s]', id, status)

        return


    def get_statuses(self) -> list[str]:
        return ['To Do', 'Doing', 'Done']


    def get_items(self) -> list[Item]:

        result = []

        cursor = self.get_db().collection.find({})

        for document in cursor:
            result.append(Item(document['_id'], document['status'], document['name']))

        return result

    def add_item(self, title):

        self.get_db().collection.insert_one({'status': 'To Do', 'name': title})

        log.info('add_item: title[%s]', title)

        return


