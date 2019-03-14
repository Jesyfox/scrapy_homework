# https://www.mytheresa.com/en-us/boys.html?block=boys

import scrapy
from ..items import MytheresaItem


class CatalogSpider(scrapy.Spider):
    name = "boys_catalog"
    start_urls = [
        'https://www.mytheresa.com/en-us/boys.html?block=boys'
    ]

    def parse_item(self, response):
        item = MytheresaItem()
        item['article'] = response.xpath('//span[@class="h1"]/text()').extract_first().split('\xa0')[-1]
        item['title'] = response.xpath('//a[@class="text-000000"]/text()').extract_first()
        item['image'] = response.xpath('//img[@class="gallery-image"]/@src').extract()
        item['price'] = response.xpath(
            '//div[@class="price-box"]/span[@class="regular-price"]/span[@class="price"]/text()').extract_first()
        item['size'] = None  # ???
        item['description'] = response.xpath('//p[@class="pa1 product-description"]/text()').extract_first()
        return item

    def parse(self, response):
        p_urls = response.xpath('//h2[@class="product-name"]/a/@href').extract()[:3]
        for url in p_urls:
            yield scrapy.Request(url=url, callback=self.parse_item)
