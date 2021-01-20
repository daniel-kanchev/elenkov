import scrapy


class ElenSpider(scrapy.Spider):
    name = 'elen'
    allowed_domains = ['elenkov.net']
    start_urls = ['http://elenkov.net/блог-2/']

    def parse(self, response):
        pass
