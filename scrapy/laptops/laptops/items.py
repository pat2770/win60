# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Laptop(scrapy.Item):
    title = scrapy.Field()
    id = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    stars = scrapy.Field()
    reviews = scrapy.Field()
