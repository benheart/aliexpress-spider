# -*- coding: utf-8 -*-
import scrapy
from aliexpress.items import AliexpressItem

protocol_prefix = 'https:'


class AliExpressSpider(scrapy.Spider):
    name = 'aliexpress'
    start_urls = ['https://www.aliexpress.com/store/all-wholesale-products/2824066.html']

    def parse(self, response):
        for product in response.css('.items-list .item'):
            item = AliexpressItem()
            item['product_name'] = product.css('.detail h3 a::text').extract_first()
            item['product_url'] = protocol_prefix + product.css('.detail h3 a::attr(href)').extract_first()
            yield item

        next_page = response.xpath('//a[@class="ui-pagination-next"]/@href')
        if next_page:
            url = protocol_prefix + next_page.extract_first()
            yield scrapy.Request(url, self.parse)
