# -*- coding:utf8 -*-
# /usr/bin/env python
import requests
import subprocess
import sys
import os
from bs4 import BeautifulSoup
from lxml import etree
import re
import pymysql
import time
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def get_mysql():
    conn = pymysql.connect(host = 'localhost', user = 'root', passwd = 'gwk2014081029', db = 'mysql', charset = 'utf8')
    cur = conn.cursor()
    cur.execute('use book')
    return (cur, conn)
url = 'http://210.38.102.131:86/reader/login.php'
session = requests.session()

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36'
}
cookie = {
    'Cookie':'ASP.NET_SessionId=i5ffsxeo3ozgfo45wa0g4suc; Hm_lvt_ed06d5e5f94d85932b82e4aac94d0c68=1462255778,1463414456,1464310905,1464787283; Hm_lpvt_ed06d5e5f94d85932b82e4aac94d0c68=1464787283; PHPSESSID=asev0q0gr32glv35p3i1q41ua4'
}

def get_img(img_url):
    html = session.get(img_url).content
    with open('tp.jpg', 'wb') as f:
        f.write(html)
    if sys.platform.find('darwin') >= 0:
        subprocess.call(['open', 'tp.jpg'])
    elif sys.platform.find('linux') >= 0:
        subprocess.call(['xdg-open', 'tp.jpg'])
    else:
        os.startfile('tp.jpg')

def send_email(day, number):
    from_addr = '15602200534@163.com'
    password = 'gwk2014081029'
    to_addr = '673411814@qq.com'
    smtp_server = 'smtp.163.com'

    text = 'Hello ,郭伟匡, 告诉你一个不好的消息,赶紧带上你的书,去图书馆交钱吧！你已经超期了%d天了,总共有%d书超期了！！！' % (day, number)
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = format_addr('python爱好者<%s>' % from_addr)
    msg['To'] = format_addr('管理员<%s>' % to_addr)
    msg['Subject'] = Header('来着郭伟匡的问候......', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def send_message():
    day_num = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day_num1 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    sql = 'select * from book_list;'
    cur, conn = get_mysql()
    cur.execute(sql)
    rows = cur.fetchall()
    local_time = time.strftime("%Y-%m-%d", time.localtime())
    local_time = str(local_time)
    times = re.split(r'-', local_time)
    from_addr = '15602200534@163.com'
    password = 'gwk2014081029'
    to_addr = '673411814@qq.com'
    smtp_server = 'smtp.163.com'

    for i in rows:
        print(i[4])
        number = 0
        pattern = re.split(r'-', i[4])
        if times[1] == pattern[1]:
            day = int(times[2]) - int(pattern[2])
            if day > 0:
                print('已经超期了%d天' % day)
                number += 1
                send_email(day, number)
        elif times[1] > pattern[1]:
            extend_day = day_num[int(pattern[1]) - 1] - int(pattern[2]) + times[2]
            print('已经超期了%d天' % extend_day)
            number += 1
            send_email(day, number)
        else:
            print('还没有超期的书籍')

        print(pattern[2])
def get_book_name(book_url):
    html1 = session.get(book_url, cookies = cookie, headers = headers).content.decode('utf-8')
    soup = BeautifulSoup(html1, 'lxml')
    # print(html1)
    book_list = []
    cur, conn = get_mysql()
    for book_name in soup.find_all('a', class_="blue"):
        print(book_name.get_text())
        # print(type(book_name.get_text()))
        content = book_name.get_text()
        content = str(content)
        with open('book.txt', 'w+') as f:
            f.write(content)
    sql = 'select * from book_list;'
    cur, conn = get_mysql()
    cur.execute(sql)
    rows = cur.fetchall()
    book_title = []
    for row in rows:
        book_title.append(row[1])

    book_every = []
    for book_time in soup.find_all('td', class_="whitetext"):
        print(book_time.get_text().strip())
        pattern = re.compile(r'\s')
        content = re.sub(pattern, r'', book_time.get_text())
        # print(content)
        if content != '':
            book_every.append(content)
            if len(book_every) == 7:
                book_list.append(book_every)
                if book_every[0] not in book_title:
                    sql = 'insert book_list(条形码, 题名和作者, 借阅日期, 应还日期, 续借量, 馆藏地, 附件) value(' + "\'" \
                          + book_every[0] + "\'," + "\'" + book_every[1] + "\'," + "\'" + book_every[2] + "\'," + "\'" \
                          + book_every[3] + "\'," + "\'" + book_every[4] + "\'," + "\'" + book_every[5] + "\'," + "\'" \
                          + book_every[6] + "\'" + ');'
                try:

                    cur.execute(sql)
                    conn.commit()
                except:
                    conn.rollback()
                book_every = []

    # book_list.append(book_every)

    # book_list.append(book_every)
        # book_every = []
    print(book_list)



    # print(book_list)
        # book_list = []
if __name__ == '__main__':
    img_url = 'http://210.38.102.131:86/reader/captcha.php'
    # get_img(img_url)
    # input_number = input('输入验证码：')
    # post_data = {
    #     'number':'2014081029',
    #     'passwd':'gwk2014081029',
    #     'captcha': input_number
    # }
    start = 'http://210.38.102.131:86/reader/login.php'
    start_url = 'http://210.38.102.131:86/reader/redr_info.php'
    book_url = 'http://210.38.102.131:86/reader/book_lst.php'
    html = session.get(start_url, cookies = cookie, headers = headers).content.decode('utf-8')
    print(html)
    # html = session.post(start, data = post_data, headers = headers).content.decode('utf-8')
    # print(html)
    book_html = session.get(book_url, cookies = cookie, headers = headers).content.decode('utf-8')
    print('=' * 40)
    print(book_html)
    print('=' * 40)
    get_book_name(book_url)
    # html1 = session.get(start_url, headers = headers).content.decode('utf-8')
    # print(html1)
    send_message()