from operator import concat
import scrapy

from ..items import *

class GenericSpider(scrapy.Spider):
    name = "oasis"
    def start_requests(self):
        urls = [
            'http://oasis.col.org/browse?type=region'
        ]
        for url in urls:
            print("New Url", url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):
        resp = response.xpath('//div[@id="aspect_artifactbrowser_ItemViewer_div_item-view"]').get()
        yield TripleItem(subject=self.name, predicate="hasRaw", object=str(resp), source=response.url)

    def parse_list(self, response):
        next_page = response.xpath('//h4[@class="artifact-title"]/a/@href').getall()
        next_page = ["%s%s" % (s, '?show=full') for s in next_page]
        if next_page is not None:
            for next in next_page:
                print("Next : ", next)
                yield response.follow(next, self.parse_item)
        else:
            print('next_page is None :(')
        page = response.xpath('//a[@class="next-page-link"]/@href').getall()
        if page is not None and len(page) == 2:
            print('Next page :', page, ': ', len(page))
            p = page[0]
            yield response.follow(p, self.parse_list)
        else:
            print('Is not a new page :)')

    def parse(self, response):
        next_subject = response.xpath('//td[@class="ds-table-cell odd"]/a/@href').getall()
        if next_subject is not None:
            for next in next_subject:
                print('Next subject : ', next)
                yield response.follow(next, self.parse_list)
        else:
            print('next_subject is None :( ')
