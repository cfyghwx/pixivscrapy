import scrapy
from requests import request

from pixiv.Util.FileUtil import FileUtil


class pxivi(scrapy.Spider):
    name="pixiv"
    filepath="E:/pxiviscrapy/pxivi/pxivi/password/password.txt"
    # filepath="../password/password.txt"
    allowed_domains=[]

    start_urls=["https://www.pixiv.net/"]

    login_url="https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"


    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'

    header = {
        'Origin': 'https://accounts.pixiv.net',
        'User-Agent': agent,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
        'X-Requested-With': 'XMLHttpRequest',
        'accept-language': 'zh-CN, zh;q = 0.9'
    }

    def parse(self, response):
        # print(response.url)
        print(response.body.decode('utf-8'))
        print("这里是pixiv")

    def start_requests(self):
        # yield scrapy.Request(self.start_url[0],callback=self.before_login,headers=self.header)
        # print("start request")
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
            "return_to": "https://www.pixiv.net/",
        }
        print(fromdata)
        yield scrapy.FormRequest(url="https://accounts.pixiv.net/api/login?lang=zh",formdata=fromdata,callback=self.login)

    def login(self,response):
        print("我正在申请登录呢稍等")
        yield  scrapy.Request(self.start_urls[0], callback=self.parse, headers=self.header)