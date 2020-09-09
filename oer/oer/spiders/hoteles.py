from operator import concat
from scrapy.selector import Selector

import scrapy
import re

class GenericSpider(scrapy.Spider):
    name = "hotels"

    def start_requests(self):
        # Urls for scrape
        urls = [
            'https://www.tripadvisor.co/Hotels-g644406-Loja_Loja_Province-Hotels.html' # Page one
            'https://www.tripadvisor.co/Hotels-g644406-oa30-Loja_Loja_Province-Hotels.html', # Page otwo
            'https://www.tripadvisor.co/Hotels-g644406-oa60-Loja_Loja_Province-Hotels.html' # Page three
        ]
        for url in urls:
            print("New Url for scrape ", url)
            yield scrapy.Request(url=url, callback=self.parse_hotels_list)

    # This method gets urls of all hotels in a page
    def parse_hotels_list(self, response):
        # Get urls of all hotels in the page
        hotels_links = response.xpath('//a[@class="property_title prominent "]/@href').getall()
        # Add domain to all hotels links to navigate to each hotel page
        hotels_list = ["%s%s" % ('https://www.tripadvisor.co', s) for s in hotels_links]
        for hotel in hotels_list:
            print('Go to hotel ', hotel)
            yield response.follow(hotel, self.parse_hotel)

    def parse_hotel(self, response):
        # All HTML
        html = response.xpath('//div[@class="page "]').get()
        # Hotel name
        name = Selector(text=html).xpath('//h1[@id="HEADING"]/text()').get()
        # Hotel address
        address = Selector(text=html).xpath('//span[@class="_3ErVArsu jke2_wbp"]/text()').get()
        # Hotel guests
        room = response.xpath('//span[@class="room-info"]/text()').get()
        adult = response.xpath('//span[@class="adult-info"]/text()').get()
        child = response.xpath('//span[@class="child-info"]/text()').get()
        guests = response.xpath('//*[@id="component_46"]/div/div/div[2]/button/div/span[2]/span[2]/span').get()

        # Hotel price
        price = Selector(text=html).xpath('//div[@class="CEf5oHnZ"]/text()').get()

        print(name)
        print(address)
        print(room, adult, child)
        print(guests)
        print(price)
