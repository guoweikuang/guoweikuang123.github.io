# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 18:06:02 2016

@author: guoweikuang
"""

import re
import requests
import os
import time
import urllib.request

header = {
    'User-Agent': ' Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'
}

response = requests.session()

def get_xsrf():
    start_url = 'http://www.zhihu.com'
    start_page = response.get(start_url, headers = header)
    start_html = start_page.text
    req = re.compile('name="_xsrf" value="(.*?)"/>')
    content = re.findall(req, start_html)
    print(content[0])
    return content[0]

def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r' + t
    r = response.get(captcha_url, headers = header)
    with open('captcha.gif', 'wb') as fp:
        fp.write(r.content)
        fp.close()
    captcha = input('请输入验证码：')
    return captcha

def login_zhihu(email, password):
    login_url = 'http://www.zhihu.com/login/email'
    post_data = {
        'email': email,
        'password': password,
        '_xsrf': get_xsrf(),
        'remeber_me': 'true',
    }
    post_data['captcha'] = get_captcha()
    get_content = response.post(login_url, data = post_data, headers = header)
    login_code = eval(get_content.text)
    print(login_code["msg"])
    index = response.get('http://zhihu.com')
    with open('zhihu.html', 'wb') as fp:
        fp.write(index.content)
    print(index.text)
            
try:
    input = raw_input
except:
    pass

def get_question(url):
    start_url = url
    content = response.get(start_url)
    
    pattern = re.compile(r'<div class="zm-list-content-medium">\s+<h2.*title=".*?">(.*?)</a></h2>\s+<div.*?>(.*?)</div>\s+<div.*>\s+<a.*?>(.*?)</a>\s+.\s+<a.*?>(.*?)</a>\s+.\s+<a.*?>(.*?)</a>\s+.\s+<a.*?>(.*?)</a>')
    
    get_content = re.findall(pattern, content.text)
    item = []
    for item in get_content:
        print(item[0],item[1],item[2], item[3], item[4], item[5])
        print('\n')



    
if __name__ == '__main__':
    email = input('请输入你的邮箱账号：')
    password = input("请输入你的密码:")
    login_zhihu(email, password)
    set_url = input('输入你要抓取的url的名字:')
    url = 'https://www.zhihu.com/people/' + set_url + '/followees'
    print(url)
    get_question(url)
    
    
    
