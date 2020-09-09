import scrapy
from ..items import *


class Spider(scrapy.Spider):
    name = "galileo"

    def start_requests(self):
        urls = [
            'https://oer.galileo.usg.edu/all-textbooks/',
            'https://oer.galileo.usg.edu/all-textbooks/index.2.html',
            'https://oer.galileo.usg.edu/all-textbooks/index.3.html'
        ]
        for url in urls:
            print("New Url", url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        all_oers = response.xpath('//div[@class="content_block"]/a/@href').getall()
        for oer in all_oers:
            print("Url:\t", oer)
            yield scrapy.Request(oer, callback=self.parse_item)

    def parse_item(self, response):
        html = response.xpath('//div[@id="content"]').get()
        yield TripleItem(subject=self.name, predicate="hasRaw", object=str(html), source=response.url)
