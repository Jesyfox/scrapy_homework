# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MytheresaItem(scrapy.Item):
    article = scrapy.Field()  # <span class="h1">
    title = scrapy.Field()  # <a class="text-000000"
    image = scrapy.Field()  # <img id="image-(*)" class="gallery-image"
    price = scrapy.Field()  # <span class="price"
    size = scrapy.Field()  # <a href="javascript:void(0);" class="size-trigger"> ???
    description = scrapy.Field()  # <p class="pa1 product-description">
