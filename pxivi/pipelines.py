from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import requests
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PxiviPipeline(object):
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    header2 = {
        'User-Agent': agent,
        'Referer': '',
    }
    path = "E:\\pixiv\\dayrank\\"
    def process_item(self, item, spider):
        print("prr")
        urls=item['image_urls']
        url=urls[0]
        self.header2['Referer']=item['referer']
        imgcontent=requests.get(url,headers=self.header2)
        filename=item['picname']
        file=self.path+filename
        with open(file,'wb') as f:
            f.write(imgcontent.content)
        print("已保存图片")
        return item

# class PxiviImagePipeline(ImagesPipeline):
#
#     agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
#     header2 = {
#         'User-Agent': agent,
#         'Referer': '',
#     }
#
#     def get_media_requests(self, item, info):
#         for image_url in item['image_urls']:
#             self.header2['Referer']=item['referer']
#             print("我已经到了pipeline")
#             yield Request(image_url, headers=self.header2)
#
#     # def item_completed(self, results, item, info):
#     #     image_paths = [x['path'] for ok, x in results if ok]
#     #     if not image_paths:
#     #         raise DropItem("Item contains no images")
#     #     item['image_paths'] = image_paths
#     #     return item
