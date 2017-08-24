# -*- coding: utf-8 -*-
import requests
import http.cookiejar as cookiejar
import re

session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未能加载")

header = {
    "HOST":"www.zhihu.com",
    "Referer":"https://www.zhihu.com",
    "Origin":"https://www.zhihu.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
}

# 判断是否登陆
def is_login():
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True

# 获取xsrf
def get_xsrf():
    response = session.get("https://www.zhihu.com",headers=header)
    regex = re.compile(r'name="_xsrf" value="(.*?)"')
    res = regex.findall(response.text)
    if res:
        return (res[1])
    else:
        return ""

# 获取验证码
def get_captcha():
    import time
    t = str(int(time.time()*1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login&lang=cn".format(t)
    t = session.get(captcha_url,headers=header)
    with open("captcha.gif","wb") as f:
        f.write(t.content)
        f.close()

    # from PIL import Image
    # try:
    #     im = Image.open("captcha.jpg")
    #     im.show()
    #     im.close()
    # except:
    #     pass
    #
    # return input("请输入验证吗：")

# 获取验证码坐标
def get_captcha_position():
    from zheye import zheye
    z = zheye()
    positions = z.Recognize('captcha.gif')
    print(positions)
    return positions

# 获取知乎首页
def get_index():
    response = session.get("https://www.zhihu.com",headers=header)
    with open("index_page.html","wb") as f:
        f.write(response.text.encode("utf-8"))
    print("ok")

# 登陆知乎
def zhihu_login(account, password):
    if re.match("^1\d{10}",account):
        print("手机号登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        captcha = get_captcha()
        pos = get_captcha_position()

        pos_type = ()
        pos_list = []
        for i in range(len(pos)):
            pos_type += (pos[i][1] / 2, pos[i][0] / 2)
            pos_list.append("[%.2f, %f]")
        pos_str = '{"img_size": [200,44],"input_points": [' + ','.join(pos_list) + ']}'
        captcha_data = pos_str % pos_type

        post_data = {
            "_xrsf": get_xsrf(),
            "phone_num": account,
            "captcha": captcha_data,
            "captcha_type": 'cn',
            "password": password
        }
    else:
        if "@" in account:
            print("邮箱方式登陆")
            post_url = "https://www.zhihu.com/login/email"
            captcha = get_captcha()
            pos = get_captcha_position()

            pos_type = ()
            pos_list = []
            for i in range(len(pos)):
                pos_type += (pos[i][1] / 2, pos[i][0] / 2)
                pos_list.append("[%.2f, %f]")
            pos_str = '{"img_size": [200,44],"input_points": [' + ','.join(pos_list) + ']}'
            captcha_data = pos_str % pos_type

            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "captcha": captcha_data,
                "captcha_type": 'cn',
                "password": password
            }
    response_text = session.post(post_url,data=post_data,headers=header)
    print(response_text.json())
    session.cookies.save()

zhihu_login("Username","Password")
get_index()
res = is_login()
print (res)