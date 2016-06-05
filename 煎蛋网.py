# -*- coding: utf-8 -*-
import urllib
import re
import urllib2

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    'Host':'jandan.net',
    'Referer':'http://jandan.net/'
    }

url = 'http://jandan.net/ooxx/'

def get_img(url):
    input_url = input('输入你要下载的网页')
    input_end = input('输入你要下载的网页终止')
    temp = 500
    for i in range(input_end, input_url):
        start_url = url + 'page-%d#comments'%i
        print i
        request = urllib2.Request(start_url, headers = headers)
        response = urllib2.urlopen(request)
        content = response.read()
        #print content
        pattern = re.compile(r'<img src="(.*?)".*?')
        html = re.findall(pattern,content)
        
        for i in html:
            temp += 1
            urllib.urlretrieve(i, '%s.jpg' % temp)
            print '爬取成功'
    
get_img(url)    
