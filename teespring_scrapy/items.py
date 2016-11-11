# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopItem(scrapy.Item):
    category_name = scrapy.Field()
    category_url = scrapy.Field()
    sub_category_name = scrapy.Field()
    sub_category_url = scrapy.Field()
    product_image_url = scrapy.Field()
    product_url = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()