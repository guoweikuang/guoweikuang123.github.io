# -*- coding: utf-8 -*-
import urllib2
import urllib
import re
start_url = 'http://pp.163.com/square?projectnameforlofter=pp'
get_page = urllib2.urlopen(start_url)
get_content = get_page.read()
#print get_content
def getimg(aaa):
    reg = re.compile(r'<img.*?src=".*?" data-lazyload-src="(.*?)".*?>')
    l = re.findall(reg, aaa)
    temp = 101
    for i in l:
        temp += 1
        urllib.urlretrieve(i, '/home/guoweikuang/图片/%s.jpg' %temp)
def get_href(aaa):
    print '开始下载'
    req = re.compile(r'<img.*[\s]+<a href="(.*?)".*')
    get_url = re.findall(req, aaa)
    for i in get_url:
        print i
        
 
        
        
        

get_href(get_content)
