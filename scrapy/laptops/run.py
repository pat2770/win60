import scrapy
from datetime import datetime
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from laptops.items import Laptop
from scrapy.utils.log import configure_logging

class LaptopsSpider(scrapy.Spider):
    name = "laptops"

    def start_requests(self):
        urls = [
            'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for selector in response.xpath("//div[@class='thumbnail']"):
            l = ItemLoader(item=Laptop(), selector=selector)
            l.add_xpath('title', './/a[@class="title"]/@title')
            l.add_xpath('link', './/a[@class="title"]/@href')
            l.add_xpath('id', './/a[@class="title"]/@href', re='.*/(\d+)')
            l.add_xpath('price', './/h4[@class="pull-right price"]/text()')
            l.add_xpath('description', './/p[@class="description"]/text()')
            l.add_xpath('stars', 'count(.//span[@class="glyphicon glyphicon-star"])')
            l.add_xpath('reviews', './/div[@class="ratings"]',re='(\d+) reviews')
            yield l.load_item()

if __name__ == "__main__":
    startTime = datetime.now()
    process = CrawlerProcess(settings={
    "FEEDS": {
        "items.csv": {"format": "csv"}},
    "LOG_LEVEL": "ERROR"
    })
    process.crawl(LaptopsSpider)
    process.start()
    print(datetime.now() - startTime)
