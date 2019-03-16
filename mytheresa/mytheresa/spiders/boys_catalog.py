# https://www.mytheresa.com/en-us/boys.html?block=boys

import scrapy
from ..items import MytheresaItem
from scrapy_redis.spiders import RedisSpider


class CatalogSpider(RedisSpider):
    name = "boys_catalog"
    # start_urls = [
    #         'https://www.mytheresa.com/en-us/boys.html',
    #     ]

    def get_page_count(self, response):
        return int(response.xpath('//li[@class="last"]/a/@href').extract_first().split('?p=')[-1])

    def make_requests_from_url(self, url):
        return scrapy.Request(url=url)

    def get_article(self, response):
        try:
            return response.xpath('//span[@class="h1"]/text()').extract_first()
        except IndexError:
            return None

    def get_title(self, response):
        return response.xpath('//a[@class="text-000000"]/text()').extract_first()

    def get_image(self, response):
        img_list = response.xpath('//img[@class="gallery-image"]/@src').extract()
        return [img.lstrip('//') for img in img_list]

    def get_price(self, response):
        return response.xpath(
            '//div[@class="price-box"]/span[@class="regular-price"]/span[@class="price"]/text()').extract_first()

    def get_size(self, response):
        res = []
        params_list = response.xpath(
            '//div[@class="product-options"]/dl/dd/div/div[@class="size-chooser"]/ul[@class="sizes"]/li/a')
        if params_list:
            for item in params_list:
                if item.xpath('span/text()'):
                    size = item.xpath('span/text()').extract_first()
                else:
                    size = item.xpath('text()').extract_first()
                res.append(size)
        return res

    def get_description(self, response):
        return response.xpath('//p[@class="pa1 product-description"]/text()').extract_first()

    def parse_item(self, response):
        item = MytheresaItem()
        item['article'] = self.get_article(response)
        item['title'] = self.get_title(response)
        item['image'] = self.get_image(response)
        item['price'] = self.get_price(response)
        item['size'] = self.get_size(response)
        item['description'] = self.get_description(response)
        return item

    def parse_page(self, response):
        p_urls = response.xpath('//h2[@class="product-name"]/a/@href').extract()[:1]  # !!!
        for url in p_urls:
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse(self, response):
        for page in range(1, self.get_page_count(response) + 1):
            page_url = 'https://www.mytheresa.com/en-us/boys.html?p={page}'.format(page=page)
            yield scrapy.Request(url=page_url, callback=self.parse_page)
