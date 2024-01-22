# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TokyorentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HouseItems(scrapy.Item):
    detail = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    deposit = scrapy.Field()
    key_money = scrapy.Field()
    floor = scrapy.Field()
    year_built = scrapy.Field()
    nearest_station = scrapy.Field()
