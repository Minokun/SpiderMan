# -*- coding: utf-8 -*-
import scrapy


class ZhiguSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    header = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "Origin": "https://www.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
    }

    # 首先重写入口方法
    def start_requests(self):
        return [scrapy.FormRequest(
            "https://www.zhihu.com/#signin",
            headers=self.header,
            callback=self.login
        )]

    # 登录
    def login(self,response):
        pass

    # 识别验证码
    def recognize_captcha(self,response):
        pass

    # 检测是否登录
    def check_login(self,response):
        # 验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)

    def parse(self, response):
        pass