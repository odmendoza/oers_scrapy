# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TripleItem(scrapy.Item):
    subject = scrapy.Field()
    predicate = scrapy.Field()
    object = scrapy.Field()
    source = scrapy.Field()
