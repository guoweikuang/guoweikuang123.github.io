import requests
import urllib

r = requests.get('http://music.163.com/api/playlist/detail?id=3779629')

arr = r.json['result']['tracks']

for i in range(10):
    name = arr[i]['name'] + '.mp3'
    link = arr[i]['mp3Url']
    urllib.urlretrieve(link, '/home/guoweikuang/python爬虫/' + name)
    print name + '下载完成'

    
