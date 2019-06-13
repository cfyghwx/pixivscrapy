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

    header2 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': agent,
        'Host':'www.pixiv.net',
        'Cookie':'p_ab_id=9; login_ever=yes; p_ab_id_2=2; _ga=GA1.2.14473519.1479795408; a_type=0; b_type=1; first_visit_datetime_pc=2018-07-10+21%3A31%3A45; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^4=p_ab_id_2=2=1^5=gender=male=1^6=user_id=20796070=1^9=p_ab_id=9=1^10=p_ab_id_2=2=1^11=lang=zh=1^14=hide_upload_form=no=1^15=machine_translate_test=no=1; _td=8290c264-2b72-450d-f5ae-5082a7ca1638; privacy_policy_agreement=1; p_ab_d_id=55280553; yuid_b=NxRoAIc; c_type=23; module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; device_token=29f48a8b368f710578f99626d6c56873; ki_r=; __utmz=235335808.1558845555.38.30.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); ki_s=196049%3A0.0.0.0.0%3B197685%3A0.0.0.0.0; _gid=GA1.2.1720188537.1560330345; login_bc=1; is_sensei_service_user=1; PHPSESSID=20796070_557a81f137746da25855a996c9220390; __utmc=235335808; ki_t=1479795521154%3B1560386800518%3B1560386800518%3B11%3B51; __utma=235335808.14473519.1479795408.1560386796.1560391302.44; tag_view_ranking=RTJMXD26Ak~Lt-oEicbBr~jH0uD88V6F~uusOs0ipBx~BU9SQkS-zU~y8GNntYHsi~jhuUT0OJva~aNqTPYQ7NR~0HA6x-6rNd~qtVr8SCFs5~nQRrj5c6w_~t2ErccCFR9~svKogfYWcS~K8esoIs2eW~I5npEODuUW~xZ6jtQjaj9~gooMLQqB9a~SoxapNkN85~0YMUbkKItS~RybylJRnhJ~-sp-9oh8uv~_pwIgrV8TB~YRDwjaiLZn~Itu6dbmwxu~sOBG5_rfE2~b1s-xqez0Y~wKl4cqK7Gl~1gyS7Hj6p1~NXxDJr1D_u~pYlUxeIoeg~ClLaegOm3j~0im78x6u68~aTW6kYb0Ak~kMjNs0GHNN~hM1TCn1fqR~d2oWv_4U1L~Oa9b6mEc1T~LJo91uBPz4~EUwzYuPRbU~Tb7S5ldFeI~Qri62qoiFF~4-_9de7LBH~w6DOLSTOSN~PTyxATIsK0~V47VpO7PWh~2pZ4K1syEF~A0q8P8HaKf~8HRshblb4Q~cpt_Nk5mjc~Ow9mLSvmxK~PwDMGzD6xn~KML8PeiHmP~s60GJ0Ed-R~IfTHG7cZ8v~mFuvKdN_Mu~2-ZLcTJsOe~pzzjRSV6ZO~3SAZKPd9Ah~noyKIE4uzj~ZW-jh61Jnc~fg8EOt4owo~CMH7y9clRf~7eyUzBENF5~W29V3uy2lf~_fMf86iA_3~vti3o9ERHH~l015P5ziIS~azESOjmQSV~tgP8r-gOe_~--avxVm3dl~65aiw_5Y72~puqZDMoPUT~eVxus64GZU~c8y2glRxy1~z8HrAjAXzi~iyrFzpI6SA~bFcHQpe7ZU~qyDMQvMC7T~T91C10O3g2~vFXX3OXCCb~H7qKdacf1z~DpO7Lofslr~Doqtqks7uU~jPsOGzt9Dh~uW5495Nhg-~_pKwD8FJtS~s3i_irjAJg~lUM3Y7NGaw~jFBZFm1HHK~LF9kqwfMs-~8XX2eqWqNX~DZrrbq7Psc~5EaZJPu78X~yroC1pdUO-~zCb4tJZ68z~5gCuAOMc6Z~tlXeaI4KBb~LtW-gO6CmS~GLBT6m6Fig~pD0wVYlrjV; __utmb=235335808.5.10.1560391302',
        'Upgrade-Insecure-Requests': '1'
        # 'Referer': '',
        # 'x-user-id':'20796070'
    }


    def parse(self, response):
        print("这里是pixiv")
        # self.parse_dayrankpic(response)
        urllist=response.xpath('//*[@id="column-misc"]/section[2]/ol/li[2]/div[1]/a/@href').extract()
        url=urllist[0]
        targeturl=self.start_urls[0]+url[1:]
        i=targeturl.rfind('&')
        targeturl=targeturl[:i]
        # self.header2['Referer']=targeturl
        # imageurl='https://i.pximg.net/user-profile/img/2017/09/29/13/51/27/13283446_b908e62681a97cefa388c5e166144867_170.jpg'
        yield scrapy.Request(url=targeturl,callback=self.getpicture,headers=self.header2)


    def parse_dayrankpic(self,response):

        pass

    def getpicture(self,response):
        # print(response.body.decode('utf-8'))
        script=response.xpath("/html/head/script[6]").extract()
        pattern=re.compile('"imageBig":"(.+?)"')
        url=re.search(pattern,script[0])
        url=url.group(1)
        url=url.replace("\\","")
        print(url)
        item=PxiviItem()
        item['referer']=response.url
        item['image_urls']=["https://i.pximg.net/img-master/img/2019/06/10/00/00/03/75148706_p0_master1200.jpg"]
        item['picname']='test.jpg'
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