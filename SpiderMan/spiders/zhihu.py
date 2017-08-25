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
        yield scrapy.Request("https://www.zhihu.com/#signin",headers=self.header,callback=self.login)

    # 登录
    def login(self,response):

        account = '952718180@qq.com'
        password = 'WXK1991327'

        import re
        # 解析出xsrf参数的值
        regex = re.compile(r'name="_xsrf" value="(.*?)"')
        res = regex.findall(response.text)
        if res[1]:
            # 构建表单参数
            post_data = {
                "_xrsf": res[1],
                "email": account,
                "captcha_type": 'cn',
                "password": password
            }
            # 开始识别验证码
            import time
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login&lang=cn".format(t)
            yield scrapy.Request(captcha_url,headers=self.header,meta={'post_data':post_data},callback=self.recognize_captcha)
        else:
            print("无法获取xsrf参数！")

    # 识别验证码
    def recognize_captcha(self,response):
        post_data = response.meta.get("post_data",{})
        # 将验证码保存
        with open("captcha.gif","wb") as f:
            f.write(response.body)
            f.close()

        from zheye import zheye
        z = zheye()
        pos = z.Recognize('captcha.gif')

        pos_type = ()
        pos_list = []
        for i in range(len(pos)):
            pos_type += (pos[i][1] / 2, pos[i][0] / 2)
            pos_list.append("[%.2f, %f]")
        pos_str = '{"img_size": [200,44],"input_points": [' + ','.join(pos_list) + ']}'
        captcha_data = pos_str % pos_type
        post_data['captcha'] = captcha_data

        return [scrapy.FormRequest(
            url="https://www.zhihu.com/login/email",
            formdata=post_data,
            headers=self.header,
            callback=self.check_login
        )]

    # 检测是否登录
    def check_login(self,response):
        import json
        # 验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request("https://www.zhihu.com/", dont_filter=True, headers=self.headers)

    def parse(self, response):
        pass