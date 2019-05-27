import scrapy


class googelSpider(scrapy.Spider):

    name="google"

    proxy="45.77.131.215"

    start_urls=["https://www.google.ca/"]

    def parse(self, response):
        print("进到这个方法了")
        print(response.url)

    def start_requests(self):
        print("我现在的在这里哦")
        yield scrapy.Request(url=self.start_urls[0],callback=self.parse)