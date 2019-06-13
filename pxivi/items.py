# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PxiviItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    referer=scrapy.Field()
    picname=scrapy.Field();
    image_urls =scrapy.Field();
    pass
