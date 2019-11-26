# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field

class NairalandItem(scrapy.Item):
    topic = Field()
    url = Field()
    topic_id = Field()
    class_ = Field()
    view_count = Field()
    valid = Field()
    comments = Field()
    timestamp = Field()
    sex = Field()



