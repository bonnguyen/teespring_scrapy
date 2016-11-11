# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from teespring_scrapy.items import ShopItem


class ShopSpider(Spider):
    # We stored already crawled links in this list
    crawledLinks = []
    name = "shop"
    allowed_domains = ["teespring.com"]
    start_urls = ['https://teespring.com/shop/']

    def parse(self, response):
        categories = response.xpath('//div[@class="feature_block feature_block--category"]/a')
        for category in categories:
            item = ShopItem()
            item["category_url"] = category.xpath('@href').extract_first()
            item["category_name"] = category.xpath('@title').extract_first()
            # print item["category_name"]
            # print item["category_url"]
            category_url = item["category_url"]
            if category_url and not category_url in ShopSpider.crawledLinks:
                ShopSpider.crawledLinks.append(category_url)
                yield Request(url=category_url, callback=ShopSpider.parse_product, meta={'item': item})

    @staticmethod
    def parse_sub_category(response):
        sub_categories = response.xpath('//a[@class="category__list_item_link"]')
        print sub_categories
        for sub_category in sub_categories:
            item = response.meta["item"].copy()
            item["sub_category_url"] = sub_category.xpath('@href').extract_first()
            item["sub_category_name"] = sub_category.xpath('@title').extract_first()
            # print item["sub_category_name"]
            # print item["sub_category_url"]
            sub_category_url = item["sub_category_url"]
            if sub_category_url and not sub_category_url in ShopSpider.crawledLinks:
                ShopSpider.crawledLinks.append(sub_category_url)
                yield Request(url=sub_category_url, callback=ShopSpider.parse_product, meta={'item': item})

    @staticmethod
    def parse_product(response):
        products = response.xpath('//article[@class="product_card js-product-card"]')
        for product in products:
            image_link = product.xpath('.//div[@class="product_card__image_container"]/img/@src').extract_first()
            product_url = product.xpath('.//div[@class="product_card__title"]/a/@href').extract_first()
            product_name = product.xpath('.//div[@class="product_card__title"]/a/text()').extract_first()
            product_price = product.xpath(
                './/div[@class="js-product-card-price product_card__price"]/@data-usd-price').extract_first()

            item = response.meta["item"].copy()
            item["product_image_url"] = "https:" + image_link
            item["product_url"] = product_url
            item["product_name"] = product_name
            item["product_price"] = product_price

            # print item["product_image_url"]
            # print item["product_url"]
            # print item["product_name"]
            # print item["product_price"]
            yield item

        next_links = response.xpath('//ul[@class="pagination"]/li')
        for next_link in next_links:
            next_text = next_link.xpath('./a/@rel').extract_first()
            next_page = "http://teespring.com" + next_link.xpath('./a/@href').extract_first()
            if next_text and next_text == 'next' and next_page and not next_page in ShopSpider.crawledLinks:
                ShopSpider.crawledLinks.append(next_page)
                yield Request(url=next_page, callback=ShopSpider.parse_product, meta={'item': item})