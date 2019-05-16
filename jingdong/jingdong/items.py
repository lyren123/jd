# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongItem(scrapy.Item):
    # define the fields for your item here like:
    brand = scrapy.Field()
    price = scrapy.Field()
    href = scrapy.Field()
    desc = scrapy.Field()

