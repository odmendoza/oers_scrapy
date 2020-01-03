from operator import concat
import scrapy

from ..items import *

class GenericSpider(scrapy.Spider):
    name = "okr"
    def start_requests(self):
        urls = [
            'https://openknowledge.worldbank.org/htmlmap'
        ]
        for url in urls:
            print("New Url", url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):
        resp = response.xpath('//div[@id="aspect_artifactbrowser_ItemViewer_div_item-view"]').get()
        yield TripleItem(subject=self.name, predicate="hasRaw", object=str(resp), source=response.url)

    def parse_list(self, response):
        next_page = response.xpath('//a/@href').getall()
        next_page = ["%s%s" % (s, '?show=full') for s in next_page]
        if next_page is not None:
            for next in next_page:
                print("Next : ", next)
                yield response.follow(next, self.parse_item)
        else:
            print('next_page is None :(')

    def parse(self, response):
        next = response.xpath('//a/@href').getall()
        if next is not None:
            for n in next:
                print('Next topic : ', n)
                yield response.follow(n, self.parse_list)
        else:
            print('next is None :( ')
