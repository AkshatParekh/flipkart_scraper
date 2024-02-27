# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from openpyxl.workbook import Workbook


class FlipkartScrapPipeline:

    def __init__(self):
        self.items = []

        self.workbook = Workbook()
        self.worksheet = self.workbook.active
        self.worksheet.append(['Name', 'Brand', 'Price', 'URL'])

        self.file = open('scraped_data.json', 'w')

    def process_item(self, item, spider):
        self.items.append(dict(item))
        self.worksheet.append([item['name'], item['brand'], item['price'], item['url']])
        return item

    def close_spider(self, spider):
        json_data = json.dumps(self.items, indent=4)
        self.file.write(json_data)
        self.file.close()

        self.workbook.save('scraped_data.xlsx')
