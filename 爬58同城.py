#-*-coding:utf8-*-
from bs4 import BeautifulSoup
import requests
from lxml import etree
url = 'http://bj.58.com/pbdn/0/'
import re
import pymysql

conn = pymysql.connect(host = 'localhost', user = 'root', passwd = 'gwk2014081029', db = 'mysql', charset = 'utf8')
cur = conn.cursor()
cur.execute('use tongcheng')
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36'
}
response = requests.get(url, headers = headers)
#print response.text
soup = BeautifulSoup(response.text, 'lxml')
text = re.compile(r'<a.*?target="_blank" class="t">(.*?)</a>')
content1 = re.findall(text, response.text)
for n in content1:
   # print n
    query = 'insert item(content) value(' + "\'" + n + "\'" + ');'
    cur.execute(query)
conn.commit()
cur.close()
conn.close()


content = soup.select('td.t > a.t')
# for item in content:
#     print item.get_text()
#  如果只想得到tag中包含的文本内容,那么可以嗲用 get_text() 方法
#  这个方法获取到tag中包含的所有文版内容包括子孙tag中的内容,并将结果作为Unicode字符串返回
#  用strip来去除空白

for title in soup.find_all('a', class_="t"):

     print title.get_text(strip = True)
# for href in soup.find_all('td')
selector = etree.HTML(response.text)
# for title in soup.find_all('img'):
#     print title.get('alt')
html = selector.xpath('//div[@id="infolist"]/table[@class="tbimg"]/tr/td[@class="t"]/a[@class="t" and @target="_blank"]/text()')
# for i in html:
#
#     print unicode(i)

# for i in html:
#     text = i.xpath('string(.)')
#     print unicode(text)

'''
//*[@id="infolist"]/table[2]/tbody/tr/td/a
//*[@id="infolist"]/table[1]/tbody/tr/td[2]/a[1]
#infolist > table:nth-child(4) > tbody > tr > td.t > a.t
#infolist > table:nth-child(4) > tbody > tr > td.t > a.t
#infolist > table:nth-child(4) > tbody > tr > td.t > a.t
#infolist > table:nth-child(4) > tbody > tr > td.t > a.t
'''

