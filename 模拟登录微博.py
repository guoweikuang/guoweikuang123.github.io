
"""
Created on Sun Mar 13 10:51:59 2016

@author: guoweikuang
"""
import urllib.request
import re
import subprocess
import sys
import urllib
import requests
from bs4 import BeautifulSoup
import pymysql
import time

conn = pymysql.connect(host = 'localhost', user = 'root', passwd = 'gwk2014081029', db = 'mysql', charset = 'utf8')
cur = conn.cursor()
cur.execute('use weibo1')
start_url = 'https://login.weibo.cn/login/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
    'Host': 'login.weibo.cn',
    'Origin': 'https://login.weibo.cn',
    'Referer': 'https://login.weibo.cn/login/'
}

response = requests.session()

'''
获取一些post形式登录时所需的密码的标志和
验证码图片的链接
'''
def get_page(start_url):
    html = response.get(start_url, headers = headers)
    pattern = re.compile(r'action="(.*?)".*?type="password" name="(.*?)".*?name="vk" value="(.*?)".*?name="capId" value="(.*?)"', re.S)
    content = re.findall(pattern, html.text)
    return content
    
def get_captcha(capId):
    capt_url = 'http://weibo.cn/interface/f/ttt/captcha/show.php?cpt='
    captcha_url = capt_url + capId
    content1 = response.get(captcha_url, headers = headers)
    with open('captcha1.jpg', 'wb') as fp:
        fp.write(content1.content)
        fp.close()
    if sys.platform.find('darwin') >= 0:
        subprocess.call(['open', 'captcha1.jpg'])
    elif sys.platform.find('linux') >= 0:
        subprocess.call(['xdg-open', 'captcha1.jpg'])
    else:
        os.startfile('captcha1.jpg')
    capt_cha = input('请输入验证码:')
    return capt_cha
    
res = get_page(start_url)
if  res == []:
    print('可能你的网络有问题，请检查后重试')
else:
    post_url, password, vk, capId = res[0]

def get_img():
   # for page in range(1, 45):
        start_url = 'http://m.weibo.cn'
        
        content2 = response.get(start_url)
        pattern = re.compile(r'<img.*src="(.*?)".*?>')
        html = re.findall(pattern, content2.text)
        temp = 500
        for i in html:
            temp += 1
           
            urllib.request.urlretrieve(i, '%s.jpg' %temp)
            print('下载成功')
def get_page(html):
    soup = BeautifulSoup(html, 'lxml')
    for content, time in zip(soup.find_all('span', class_="ctt"), soup.find_all('span', class_="ct")):
        print(content.get_text(), time.get_text())
        query = 'insert content(微博内容, 发布时间) value(' + "\'" + content.get_text() + "\'," + "\'" + time.get_text() + "\'" + ');'
        cur.execute(query)
    conn.commit()

    # for content in soup.find_all('span', class_="ctt"):
    #     print(content.get_text())
    #     query = 'insert content(微博内容) value(' + "\'" + content.get_text() + "\'" + ');'
    #     cur.execute(query)
    # for time in soup.find_all('span', class_="ct"):
    #     print(time.get_text())
    #     query = 'insert content(发布时间) value(' + "\'" + time.get_text() + "\'" + ');'
    #     cur.execute(query)
    # conn.commit()
    # conn.close()
    # cur.close()
if __name__ == '__main__':
    capt_cha = get_captcha(capId)
    conn = pymysql.connect(host = 'localhost', user = 'root', passwd = 'gwk2014081029', db = 'mysql', charset = 'utf8')
    cur = conn.cursor()
    cur.execute('use weibo1')
    password_input = 'gwk2014081029'
    #email = input('请输入你的邮箱账号或手机号码:')
    #password_input = input('请输入你的密码')
    postdata = {
            'mobile': '15602200534',
            'code': capt_cha,
            'remember': 'on',
            'backURL' : 'http%3A%2F%2Fweibo.cn',
            'backTitle': '手机新浪网',
            'tryCount': '',
            'vk': vk,
            'capId': capId,
            'submit': '登录'
            
    }
    postdata[password] = password_input
    post_url = start_url + post_url
    page = response.post(post_url, data = postdata, headers = headers)
    input_num = input('输入要获取的页数：')
    for i in range(1, int(input_num)):
        url = 'http://weibo.cn/gzyhl?page=%d&vt=4' % i
        index = response.get(url)
        time.sleep(20)

    #index.encoding = 'gbk'
        print(index.text)
        get_page(index.text)
    conn.close()
    cur.close()
    with open('weibo.html', 'w') as f:
        f.write(index.text)
    # pattern = re.compile(r'<img src="(.*?)" alt="图片" class="ib"')
    # content = re.findall(pattern, index.text)
    # print(content)
    # temp = 1
    # for item in content:
    #     print(item[-10:-4])
    #     print(item)
    #     soup = BeautifulSoup(index.content, 'lxml')
    #     temp = 1
    #     for i in soup.find_all('img'):
    #         if i.get('src')[-4:] == '.jpg':
    #             print(i.get('src'))
    #             urllib.request.urlretrieve(i.get('src'), '%s.jpg'%temp)
    #
    #     #with open('%s.jpg'%temp, 'wb') as f:
    #         #f.write(item)
    #     #urllib.request.urlretrieve(item, '%s.jpg'%temp)
    #     temp += 1
    #     print('成功')
  #  start_url = 'http://weibo.cn/u/1270344441?filter=1&page=1'
        
   # content2 = response.get(start_url,headers = headers, allow_redirects=True)
   # pattern = re.compile(r'<img src="(.*?)".*?>')
   # html = re.findall(pattern, content2.text)
    #temp = 500
    #for i in html:
   #     temp += 1
    #    urllib.request.urlretrieve(i, '%s.jpg' %temp)
    #    print('下载成功')

