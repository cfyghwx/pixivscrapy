from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PxiviPipeline(object):
    def process_item(self, item, spider):
        return item

class PxiviImagePipeline(ImagesPipeline):

    agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    header2 = {
        'User-Agent': agent,
        'Referer': '',
    }

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            self.header2['Referer']=item['referer']
            print("我已经到了pipeline")
            yield Request(image_url, headers=self.header2)

    # def item_completed(self, results, item, info):
    #     image_paths = [x['path'] for ok, x in results if ok]
    #     if not image_paths:
    #         raise DropItem("Item contains no images")
    #     item['image_paths'] = image_paths
    #     return item
