# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImagebotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ImageItem(scrapy.Item):
    # define the fields for your item here like:
    image_urls = scrapy.Field()
    len=scrapy.Field()
    images=scrapy.Field()