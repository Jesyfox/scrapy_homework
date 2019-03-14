# https://www.mytheresa.com/en-us/boys.html?block=boys

import scrapy


class CatalogSpider(scrapy.Spider):
    name = "boys_catalog"
    start_urls = [
        'https://www.mytheresa.com/en-us/boys.html?block=boys'
    ]

    def parse(self, response):
        p_urls = response.xpath('//h2[@class="product-name"]/a/@href').extract()
