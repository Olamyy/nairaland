# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem

settings = get_project_settings()


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_URI']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db['topics']

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            exists = self.collection.find_one({"topic_id": item.get('topic_id')})
            if exists:
                raise DropItem("Topic with id {} already exists".format(item.get('topic_id')))
            else:
                self.collection.insert(dict(item))
                print("Stored data in MongoDB database")
                return item
