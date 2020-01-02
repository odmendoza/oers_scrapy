# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
from .model import *


class GenericPipeline(object):

    def process_item(self, item, spider):
        print("Saving item", item["subject"])
        session = load_session()
        session.add(Triple(subject=item["subject"], predicate=item["predicate"], object=item["object"],
                           source=item["source"]))
        session.commit()
        return 'New added'
