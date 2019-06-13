import scrapy
from requests import request
import re
from pxivi.Util.FileUtil import FileUtil
from pxivi.items import PxiviItem


class pxivi(scrapy.Spider):
    name="pxivi"
    filepath="E:/pxiviscrapy/pixiv/pxivi/password/password.txt"
    # filepath="../password/password.txt"
    allowed_domains=[]

    start_urls=["https://www.pixiv.net/"]

    login_url="https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"

    request_url="https://accounts.pixiv.net/api/login?lang=zh"

    # agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

    loginReferer = 'https://accounts.pxivi.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'


    header = {
        'Origin': 'https://accounts.pxivi.net',
        'User-Agent': agent,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': '',
        'X-Requested-With': 'XMLHttpRequest',
        'accept-language': 'zh-CN, zh;q = 0.9'
    }



    def parse(self, response):
        print("这里是pixiv")
        # self.parse_dayrankpic(response)
        for i in range(1,4):
            xpath='//*[@id="column-misc"]/section[2]/ol/li['+str(i)+']/div[1]/a/@href'
            urllist=response.xpath(xpath).extract()
            url=urllist[0]
            targeturl=self.start_urls[0]+url[1:]
            i=targeturl.rfind('&')
            targeturl=targeturl[:i]
            yield scrapy.Request(url=targeturl,callback=self.getpicture,headers=self.header)


    def parse_dayrankpic(self,response):

        pass

    def getpicture(self,response):
        # print(response.body.decode('utf-8'))
        script=response.xpath("/html/head/script[6]").extract()
        pattern=re.compile('"original":"(.+?)"')
        url=re.search(pattern,script[0])
        url=url.group(1)
        url=url.replace("\\","")
        print(url)
        item=PxiviItem()
        item['referer']=response.url
        item['image_urls']=[url]
        item['picname']=url.split("/")[-1]
        print(item['picname'])
        yield item

    def start_requests(self):
        self.header['Referer']=self.loginReferer
        yield scrapy.Request(self.login_url, callback=self.before_login, headers=self.header)

    def before_login(self,response):
        postkey=response.xpath('//*[@id="old-login"]/form/input[1]/@value').extract()
        fileu = FileUtil()
        pid, password = fileu.readidpass(self.filepath)
        fromdata = {
            "pixiv_id": pid,
            "password": password,
            "captcha": "",
            "g_recaptcha_response": "",
            "post_key": postkey[0],
            "source": "pc",
            "ref": "wwwtop_accounts_index",
            "return_to": "https://www.pxivi.net/",
        }
        print(fromdata)
        yield scrapy.FormRequest(url=self.request_url,formdata=fromdata,callback=self.login)

    def login(self,response):
        print("我正在申请登录呢稍等")
        yield  scrapy.Request(self.start_urls[0], callback=self.parse, headers=self.header)