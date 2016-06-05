# -*- coding: utf-8 -*-
import time
from datetime import datetime
import subprocess
import sys
import requests
from bs4 import BeautifulSoup
import json
import pymysql

conn = pymysql.connect(host = 'localhost', user = 'root', passwd = 'gwk2014081029', db = 'mysql', charset = 'utf8')
cur = conn.cursor()
cur.execute('use score')
session = requests.session()
url = 'http://jw.gzucm.edu.cn/'
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36',
    'Referer':'http://jw.gzucm.edu.cn/login!welcome.action'

}
cookie = {
    'Cookie':'JSESSIONID=45FDD39CDE25C925AC4959EE13F34688'
}
def get_img(session):
    d = int(time.mktime(datetime.now().timetuple()))
    img_url = '{}yzm?d={}'.format(url, d)
    pic = session.get(img_url).content
    with open('验证码.jpg', 'wb') as f:
        f.write(pic)

    if sys.platform.find('darwin') >= 0:
        subprocess.call(['open', '验证码.jpg'])
    elif sys.platform.find('linux') >= 0:
        subprocess.call(['xdg-open', '验证码.jpg'])
    else:
        os.startfile('验证码.jpg')
if __name__ == '__main__':
    get_img(session)
    input_url = input('输入验证码:')
    postdata = {
        'account':'2014081029',
        'pwd' :'gwk2014081029',
        'verifycode': str(input_url)
    }
    # session = requests.session()

    # html = 'http://jw.gzucm.edu.cn/default!getMenu.action'
    html = 'http://jw.gzucm.edu.cn/login!doLogin.action'
    html1 = 'http://jw.gzucm.edu.cn/login!welcome.action'
    html2 = 'http://jw.gzucm.edu.cn/xskccjxx!getDataList.action'
    html3 = 'http://jw.gzucm.edu.cn/xskccjxx!getDataList.action'
    text = session.post(html, data = postdata).content.decode('utf-8')
    print(text)
    text1 = session.get(html1, cookies = cookie, headers = headers).content.decode('utf-8')
    print(text1)
    text2 = session.get(html2, headers = headers).content.decode('utf-8')
    text3 = session.get(html3, headers = headers).content.decode('utf-8')
    data_string1 = json.loads(str(text3))
    print(data_string1)
    data_string = json.loads(str(text2))
    print(data_string)
    print(data_string.get('rows'))
    sql1 = 'select * from score;'
    cur.execute(sql1)
    content = cur.fetchall()
    contents = []
    for s in content:
        contents.append(s[1])
    for data in data_string.get('rows'):
        print(data)
        print("课程：" + data['kcmc'])
        print("分数：" + data['zcj'])
        print('修读方式：' + data['xdfsmc'])
        print('学年学期：' + data['xnxqmc'])
        print('绩点：' + data['cjjd'])
        print('学时：' + data['zxs'])
        print('学分:' + data['xf'])
        if data['kcmc'] not in contents:
            sql = 'insert score(课程名称, 成绩, 修读方式, 学年学期, 绩点, 学时, 学分) value(' + "\'" + data['kcmc'] + "\'," \
                                + "\'" + data['zcj'] + "\'," + "\'" + data['xdfsmc'] + "\'," + "\'" + data['xnxqmc'] \
                                + "\'," + "\'" + data['cjjd'] + "\'," + "\'" + data['zxs'] + "\'," + "\'" + data['xf']\
                                + "\'" + ');'
            cur.execute(sql)
        else:
            sql = "update score set 绩点='%s' where 课程名称='%s' "% (data['cjjd'],data['kcmc'])
            sql2 = "update score set 学分='%s' where 课程名称='%s'" % (data['xf'], data['kcmc'])
            cur.execute(sql)
            cur.execute(sql2)
    conn.commit()
    conn.close()
    cur.close()