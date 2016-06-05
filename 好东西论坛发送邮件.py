# -*- coding:utf8 -*-
import requests
from bs4 import BeautifulSoup
import re
import time
import pymysql

def mysql():
    conn = pymysql.connect(host = 'localhost', user = 'root', passwd = 'gwk2014081029', db = 'mysql', charset = 'utf8')
    cur = conn.cursor()
    cur.execute('use stu')
    return (cur, conn)
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36'
}
session = requests.session()

def get_page():
    url = 'http://forum.memect.com/'
    url1 = 'http://forum.memect.com/blog/thread-category/py/'
    html = session.get(url1, headers = headers).content.decode('utf-8')
    return html


def get_category(html):
    soup = BeautifulSoup(html, 'lxml')
    url_set = []
    for text in soup.find_all('h2', class_="title"):
        # print(text.get_text())
        pattern = re.compile(r'\s')
        match = re.sub(pattern, r'', text.get_text())
        print(match)

        print(text.find('a').get('href'))
        url_set.append(text.find('a').get('href'))
    return url_set

def get_every_page(url_set):
    cur, conn = mysql()
    for url in url_set:
        time.sleep(1)
        html = session.get(url, headers = headers).content
        soup = BeautifulSoup(html, 'lxml')
        for content in soup.find_all('div', class_="text"):
            pattern = re.compile(r'\s')
            match = re.sub(pattern, r'', content.get_text())
            print(type(match))
            re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
            replace_text = re.sub(re_pattern, r'', match)
            # print(content.get_text())
            print(replace_text)
            # print(type(match))

            if content.find('a') is not None:
                print(content.find('a').get('href'))
                print(type(content.find('a').get('href')))
                sql = 'insert python(标题, 内容链接) value(' + "\'" + replace_text + "\'," + "\'" \
                      + str(content.find('a').get('href')) + "\'" + ');'
                cur.execute(sql)
                conn.commit()
    conn.close()
    cur.close()

if __name__ == '__main__':
    html = get_page()
    url_set = []
    url_set = get_category(html)
    print('=' * 50)
    get_every_page(url_set)
