# -*- coding: utf-8 -*-
# !/usr/bin/env python

from lxml import etree
import requests
import pymysql
import matplotlib.pyplot as plt
from pylab import *
import numpy as np

# 连接mysql数据库
conn = pymysql.connect(host = 'localhost', user = 'root', passwd = '2014081029', db = 'mysql', charset = 'utf8')
cur = conn.cursor()
cur.execute('use douban')

def get_page(i):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(i)

    html = requests.get(url).content.decode('utf-8')

    selector = etree.HTML(html)

    content = selector.xpath('//div[@class="info"]/div[@class="bd"]/p/text()')
    print(content)

    for i in content[1::2]:
        print(str(i).strip().replace('\n\r', ''))
        # print(str(i).split('/'))
        i = str(i).split('/')
        i = i[len(i) - 1]
        # print('zhe' +ｉ)
        # print(i.strip())
        # print(i.strip().split(' '))
        key = i.strip().replace('\n', '').split(' ')
        print(key)
        for i in key:
            if i not in douban.keys():
                douban[i] = 1
            else:
                douban[i] += 1

def save_mysql():
    print(douban)
    for key in douban:
        print(key)
        print(douban[key])
        if key != '':
            try:
                sql = 'insert douban(类别, 数量) value(' + "\'" + key + "\'," + "\'" + str(douban[key]) + "\'" + ');'
                cur.execute(sql)
                conn.commit()
            except:
                print('插入失败')
                conn.rollback()


def pylot_show():
    sql = 'select * from douban;'
    cur.execute(sql)
    rows = cur.fetchall()
    count = []
    category = []

    for row in rows:
        count.append(int(row[2]))
        category.append(row[1])
    print(count)
    y_pos = np.arange(len(category))
    print(y_pos)
    print(category)
    colors = np.random.rand(len(count))
    # plt.barh()
    plt.barh(y_pos, count, align='center', alpha=0.4)
    plt.yticks(y_pos, category)
    for count, y_pos in zip(count, y_pos):
        plt.text(count, y_pos, count,  horizontalalignment='center', verticalalignment='center', weight='bold')
    plt.ylim(+28.0, -1.0)
    plt.title(u'豆瓣电影250')
    plt.ylabel(u'电影分类')
    plt.subplots_adjust(bottom = 0.15)
    plt.xlabel(u'分类出现次数')
    plt.savefig('douban.png')


if __name__ == '__main__':
    douban = {}
    for i in range(0, 250, 25):
        get_page(i)
    # save_mysql()
    pylot_show()
    cur.close()
    conn.close()