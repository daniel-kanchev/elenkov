import scrapy
from elenkov.items import Article
from datetime import datetime
from scrapy.loader import ItemLoader


class ElenSpider(scrapy.Spider):
    name = 'elen'
    allowed_domains = ['elenkov.net']
    start_urls = ['http://elenkov.net/блог-2/']

    def parse(self, response):
        categories = response.xpath("//section[@id='categories-2']/ul/li/a")
        for category in categories:
            category_name = category.xpath(".//text()").get()
            yield response.follow(category, self.parse_category, cb_kwargs=dict(category=category_name))

    def parse_category(self, response, category):
        articles = response.xpath("//div[@class='slide-content']")
        for article in articles:
            date = article.xpath(".//div[@class='slide-meta']//time/text()").get() or "Not available"
            link = article.xpath(".//header/h3/a/@href").get()
            yield response.follow(link, self.parse_article, cb_kwargs=dict(category=category, date=date))

        next_page = response.xpath("//a[text()='›']/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse_category, cb_kwargs=dict(category=category))

    def parse_article(self, response, category, date):
        item = ItemLoader(item=Article(), response=response)

        title = response.xpath("//h1/a/text()").get() or "Not available"
        author = response.xpath("//a[@rel='author']/text()").get() or "Not available"
        content = response.xpath("//div[@class='entry-content']/descendant-or-self::*/text()").getall()
        content = [text for text in content if text.strip()]
        content = " ".join(content)

        if date != "Not available":
            date_time_obj = datetime.strptime(date, '%d.%m.%Y')
            date = date_time_obj.strftime("%Y/%m/%d")

        item.add_value('title', title)
        item.add_value('author', author)
        item.add_value('date', date)
        item.add_value('category', category)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
