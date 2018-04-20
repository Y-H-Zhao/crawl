# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 19:38:04 2017
@author: ZYH
"""
'''
获取百度结果的爬虫
按关键字批量采集百度搜索结果前10名
'''
#-------------------------------加载必要的包-------------------------------
import requests
from bs4 import BeautifulSoup
import re
import time

#----------------------打开关键词文件,将关键词整理为列表---------------------
with open('key.txt','r') as f:
    result = f.read()
keys = result.split('\n')
key_words = list(enumerate(keys, start=1))

#----------------------逐条爬取----------------------------------------
for key in key_words:
    url = 'https://www.baidu.com/s?wd='+ key[1] #网址加关键词
    #添加头信息，防止反爬虫
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    #使用requests.Session()实例，免除设置Cookie
    s=requests.Session()
    web_db=s.get(url,headers=header)
    #解析内容
    time.sleep(2)
    soup = BeautifulSoup(web_db.text,'lxml')

    titles = soup.select('#content_left > div > h3 > a')
    ranks = [ i for i in range(1,11)]
    #根据响应结果提取真实链接
    for title,link,rank in zip(titles,titles,ranks):


        baidu_url = link.get('href')
        if str(baidu_url).find('link?url=') > 0 :
            web_db2 = requests.get(baidu_url, allow_redirects=False)
            if web_db2.status_code == 200:
                soup = BeautifulSoup(web_db2.text, 'lxml')
                urls = soup.select('head > noscript')
                url2 = urls[0]
                url_math = re.search(r'\'(.*?)\'', str(url2), re.S)
                web_url = url_math.group(1)
            elif web_db2.status_code == 302:
                web_url = web_db2.headers['location']
            else:
                web_url = 'error'
        else:
            web_url = baidu_url

#-------------保存结果----------------------------------
        data = {
            'key':key,
            'title':title.get_text(),
            'url':web_url.encode('utf-8'),
            'rank':rank,
        }
#-------------写入文件-------------------------------------
        with open('info.txt','a') as f:
            f.write(str(data)+'\n')
    print('已完成采集任务' + str(key[0]) + '==总采集任务==' + str(len(key_words)))

'''
如果想获取的更多
下面语句可以获取下一页链接
nextpage_url = re.findall(' href\=\"(\/s\?wd\=[\w\d\%\&\=\_\-]*?)\" class\=\"n\"', result.text)
'''
