from operator import concat
from scrapy.selector import Selector
import scrapy
import re

from bs4 import BeautifulSoup as BS #analizar documentos html
import requests

from ..items import *

class Oercommos(scrapy.Spider):
    name = "oercommons"
    def start_requests(self):
        urls = [
            'https://www.oercommons.org/courses/06-congress-the-people-s-branch'
        ]
        for url in urls:
            print("New Url", url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        html = response.xpath('//div[@id="content"]').get()

        # en SOUP esta TODA la pagina
        dominio = 'https://www.oercommons.org'
        soup = BS(html, 'html.parser')

        metaData = dict()
        valor_title = soup.find('h1', 'material-title').find('a').get_text()
        metaData['Title'] = valor_title
        metaData['Link Resource'] = soup.find('h1', 'material-title').find('a').get('href')

        link_imagen = soup.find('div', 'material-thumb').find('a').find('img').get('src')
        metaData['Link Imagen'] = link_imagen

        keywords = soup.find_all('li', {'class': 'tag-instance keyword'})
        keywords_list = []
        for kw in keywords:
            keywords_list.append(kw.find('a').get_text())
        metaData['Keywords'] = ', '.join(keywords_list)

        print(metaData)


