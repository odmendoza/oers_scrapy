from operator import concat
from scrapy.selector import Selector
import scrapy
import re

from ..items import *

class Merlot(scrapy.Spider):
    name = "merlot"
    def start_requests(self):
        urls = [
            #'https://www.merlot.org/merlot/materials.htm?sort.property=overallRating'
            'https://www.merlot.org/merlot/viewMaterial.htm?id=1166124'
        ]
        for url in urls:
            print("New Url", url)
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse(self, response):
        material = response.xpath('//div[@class="card-header"]/div/h4/a/@href').getall()
        material = ["%s%s" % ('https://www.merlot.org', s) for s in material]
        if material is not None:
            for next in material:
                print('Next subject : ', next)
                yield response.follow(next, self.parse_list)
        else:
            print('next_subject is None :( ')

    def parse_list(self, response):
        pre_obj = []
        dominio = 'https://www.merlot.org'

        html = response.xpath("//div[@class='container']").get()
        # I get the OER's information
        titulo = (Selector(text=html).xpath('//h2/text()').get()).strip()
        pre_obj.append(('Title', titulo))

        # Enlace del recurso
        enlace_rea = (Selector(text=html).xpath('//meta[@itemprop="url"]/@content').get())
        pre_obj.append(('Link Resource', enlace_rea))

        # Imagen del recurso
        imagen_url = Selector(text=html).xpath('//div[@class="col detail-image"]/img/@src').get()
        imagen_url = dominio + imagen_url
        pre_obj.append(('Image', imagen_url))

        # Descripcion de recurso
        descripcion = Selector(text=html).xpath('//*[@itemprop="description"]/p/text()').get()
        if descripcion is None:
            descripcion = Selector(text=html).xpath('//div[@class="col detail-title"]/div[1]/p').get()
        if descripcion is None:
            descripcion = Selector(text=html).xpath('//div[@id="material_description"]/text()').get()
        if descripcion is not None:
            descripcion = descripcion.strip()
            descripcion = re.sub('<[^>]+>', '', descripcion)
            descripcion = descripcion.replace('\xa0', '')
            descripcion = descripcion.replace('\x93', '')
            descripcion = descripcion.replace('\x94', '')
            pre_obj.append(('Description', descripcion))

        # Palabras clave
        palabras_clave = Selector(text=html).xpath('//dd[@itemprop="keywords"]/span/text()').getall()
        if len(palabras_clave) > 0:
            palabras_clave = [(s.replace(', ', '')) for s in palabras_clave]
            pc =  []
            new = {
                'Keywords' : ' '.join(palabras_clave)
            }
            pc.append(new)
            pre_obj.append(('Keywords', pc))

        # Disciplinas
        disciplines = Selector(text=html).xpath('//div[@class="modal-body"]/ul/li/a/text()').getall()
        if len(disciplines) > 0:
            ds = []
            new = {
                    'Disciplines' : ', '.join(disciplines)
            }
            ds.append(new)
            pre_obj.append(('Disciplines', ds))

        # Metadata adicional
        adicional_predicates = Selector(text=html).xpath('//div[@class="col detail-more-about"]/dl/dt/text()').getall()
        adicional_predicates = ["%s" % s.replace(':', '') for s in adicional_predicates]
        adicional_objects = Selector(text=html).xpath('//div[@class="col detail-more-about"]/dl/dd').getall()
        objects = []
        for ao in adicional_objects:
            op1 = Selector(text=ao).xpath('//dd/span/a/span/text()').get()
            if op1 is not None:
                objects.append(op1.strip())
            else:
                op2 = Selector(text=ao).xpath('//dd/span/span/text()').get()
                if op2 is not None:
                    objects.append(op2.strip())
                else:
                    op3 = Selector(text=ao).xpath('//dd/span/a/text()').get()
                    if op3 is not None:
                        objects.append(op3.strip())
                    else:
                        op4 = Selector(text=ao).xpath('//dd/span/text()').get()
                        if op4 is not None:
                            objects.append(op4.strip())
                        else:
                            op5 = Selector(text=ao).xpath('//dd/a[2]/text()').get()
                            if op5 is not None:
                                objects.append(op5.strip())
                            else:
                                op6 = Selector(text=ao).xpath('//dd/a/text()').get()
                                if op6 is not None:
                                    objects.append(op6.strip())
                                else:
                                    op7 = Selector(text=ao).xpath('//dd/text()').get()
                                    if op7 is not None:
                                        objects.append(op7.strip())
                                    else:
                                        objects.append(None)

        for pre, obj in zip(adicional_predicates, objects):
            obj = obj.replace('\n', '')
            obj = obj.replace('   ', '')
            if pre == 'Material Type':
                mt = []
                new = {
                    'nameMaterial': obj
                }
                mt.append(new)
                obj = mt
            if pre == 'Author':
                authors = []
                are_there = Selector(text=html).xpath('//*[@itemprop="author"]').getall()
                if len(are_there) == 0:
                    new = {
                        'author name': 'Unknown',
                        'author link': None
                    }
                    authors.append(new)
                else:
                    for author in are_there:
                        if author.startswith('<span'):
                            name = re.sub('<[^>]+>', '', author)
                            name = name.replace('\n', '')
                            name = name.replace('  ', '')
                            new = {
                                'author name': name.strip(),
                                'author link': None
                            }
                            authors.append(new)
                        if author.startswith('<a'):
                            name = Selector(text=author).xpath('//a/span').getall()
                            name = ''.join(name)
                            name = re.sub('<[^>]+>', '', name)
                            new = {
                                'author name': name.strip(),
                                'author link': dominio + Selector(text=author).xpath('//a/@href').get()
                            }
                            authors.append(new)
                obj = authors

            pre_obj.append((pre, obj))

        # Licencia
        imagen_licencia = Selector(text=html).xpath('//a[@rel="license"]/img/@src').get()
        tipo_licencia = Selector(text=html).xpath('//dd/a[2]/text()').get()
        if imagen_licencia is not None and tipo_licencia is not None:
            licencia = {
                'license name': tipo_licencia,
                'license image': imagen_licencia
            }
            pre_obj.append(('Creative Commons', licencia))

        pre_obj_dict = dict(pre_obj)
        print(pre_obj_dict)


