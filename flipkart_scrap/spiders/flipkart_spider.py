import scrapy

from flipkart_scrap.items import FlipkartScrapItem


class FlipkartSpider(scrapy.Spider):
    name = 'flipkart_spider'

    def start_requests(self):
        urls = [
            "https://www.flipkart.com/search?q=tshirt+for+men",
            "https://www.flipkart.com/search?q=tshirt+for+men&page=2",
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.91'
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):

        product_path = "div._1xHGtK._373qXS"
        products = response.css(product_path)

        for product in products:
            product_name = "a.IRpwTa::text"
            product_brand = "div._2WkVRV::text"
            product_price = "a._3bPFwb div._30jeq3::text"
            product_url = "a.IRpwTa::attr(href)"

            name = product.css(product_name).get()
            brand = product.css(product_brand).get()
            price = product.css(product_price).get()
            url = response.urljoin(product.css(product_url).get())

            item = FlipkartScrapItem()
            item['name'] = name
            item['brand'] = brand
            item['price'] = price
            item['url'] = url

            yield item
