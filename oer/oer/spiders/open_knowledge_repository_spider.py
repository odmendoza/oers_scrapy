import scrapy
from operator import concat
from scrapy import Selector
from ..items import *

class GenericSpider(scrapy.Spider):

    name = "okr"

    def start_requests(self):
        urls = [
            'https://openknowledge.worldbank.org/browse?type=topic&value=Accommodation+and+Tourism+Industry'
        ]
        for url in urls:
            print("New Url", url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next = response.xpath('//*[@id="aspect_artifactbrowser_ConfigurableBrowse_div_browse-by-topic-results"]/ul/li/div/div/div/div/div/h4/a/@href').getall()
        if next is not None:
            for n in next:
                print('Next resource : ', n)
                yield response.follow(n, self.parse_item)
        else:
            print('next is None :( ')

    def parse_item(self, response):
        # Get html of resource
        html = response.xpath('//*[@id="main"]/div/div/div[2]/div').get()
        titulo = Selector(text=html).xpath("//h2/text()").get()
        print(titulo)




