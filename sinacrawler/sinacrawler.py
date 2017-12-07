
# coding: utf-8

# In[5]:

import requests
res=requests.get('http://news.sina.com.cn/china/')
res.encoding='utf-8'
# print(res.text)


# In[9]:

from bs4 import BeautifulSoup
html_sample='<html>  <body>  <h1 id="title">Hello World</h1>  <a href="#" class="link">This is link1</a>  <a href="# link2" class="link">This is link2</a>  </body>  </html>'

soup = BeautifulSoup(html_sample,"lxml")
print(soup.text)


# In[12]:

soup = BeautifulSoup(html_sample,"lxml")
header = soup.select('h1')
print(header)
print(header[0])
print(header[0].text)


# In[16]:

soup = BeautifulSoup(html_sample,"lxml")
alink = soup.select('a')
print(alink)
for link in alink:
#     print(link)
    print(link.text)


# In[17]:

alink = soup.select('#title')
print(alink)


# In[18]:

for link in soup.select('.link'):
    print(link)


# In[19]:

alinks = soup.select('a')
for link in alinks:
    print(link['href'])


# In[27]:

import requests
from bs4 import BeautifulSoup
res = requests.get('http://news.sina.com.cn/china/')
res.encoding='utf-8'
soup = BeautifulSoup(res.text,'lxml')

for news in soup.select('.news-item'):
    if len(news.select('h2'))>0:
        h2 = news.select('h2')[0].text
        a = news.select('a')[0]['href']
        print(h2,a)


# In[30]:

# 取得新闻内文页面
import requests
from bs4 import BeautifulSoup
res = requests.get('http://news.sina.com.cn/o/2017-12-06/doc-ifypnyqi1126795.shtml')
res.encoding='utf-8'
print(res.text)
soup = BeautifulSoup(res.text,'lxml')


# In[33]:

# 取得新闻内文标题
soup.select('#artibodyTitle')[0].text


# In[44]:

# 取得新闻内文时间
timesource=soup.select('.time-source')[0].contents[0].strip()
type(timesource)
timesource


# In[46]:

from datetime import datetime
dt=datetime.strptime(timesource,'%Y年%m月%d日%H:%M')


# In[48]:

dt.strftime('%Y-%m-%d')


# In[50]:

# 取得新闻来源
soup.select('.time-source span a')[0].text


# In[59]:

# 整理新闻内文
article = []
for p in soup.select('#artibody p')[:-1]:
    article.append(p.text.strip())
print(article)
'@'.join(article)


# In[62]:

' '.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])


# In[65]:

# 取得编辑名称
editor = soup.select('.article-editor')[0].text.strip('责任编辑：')
editor


# In[67]:

# 取得评论数
soup.select('#commentCount1')


# In[70]:

import requests
res = requests.get('http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-fypnyqi1126795&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20')
print(res.text)


# In[74]:

# 取得评论数与评论内容
import requests
comments = requests.get('http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-fypnyqi1126795&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20')

import json
jd = json.loads(comments.text.strip('var data='))


# In[77]:

# 取得评论数
jd['result']['count']['total']


# In[80]:

# 取得新闻编号
newsurl = 'http://news.sina.com.cn/o/2017-12-06/doc-ifypnyqi1126795.shtml'
newsid = newsurl.split('/')[-1].rstrip('.shtml').lstrip('doc-i')
newsid


# In[86]:

import re
m = re.search('doc-i(.*).shtml', newsurl)
newsid = m.group(1)
newsid


# In[96]:

# 建立评论数抽取函数
commentURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-fypnyqi1126795&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'
commentURL.format(newsid)


# In[94]:

import re
import json

def getCommentCounts(newsurl):
    m = re.search('doc-i(.*).shtml', newsurl)
    newsid = m.group(1)
    comments = requests.get(commentURL.format(newsid))
    jd = json.loads(comments.text.strip('var data='))
    return jd['result']['count']['total']


# In[98]:

news = 'http://news.sina.com.cn/o/2017-12-06/doc-ifypnyqi1126795.shtml'
getCommentCounts(news)


# In[102]:

import requests
from bs4 import BeautifulSoup

def getNewsDetail(newsurl):
    result = {}
    res = requests.get(newsurl)
    res.encoding='utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    result['title']=soup.select('#artibodyTitle')[0].text
    result['newssource']=soup.select('.time-source span a')[0].text
    timesource=soup.select('.time-source')[0].contents[0].strip()
    result['dt']=datetime.strptime(timesource,'%Y年%m月%d日%H:%M')
    result['article']=''.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])
    result['editor']=soup.select('.article-editor')[0].text.strip('责任编辑：')
    result['comments']=getCommentCounts(newsurl)
    return result


# In[104]:

getNewsDetail('http://news.sina.com.cn/o/2017-12-06/doc-ifypnyqi1126795.shtml')


# In[110]:

# 抓取分页链接
import requests
import json
res = requests.get('http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=4&callback=newsloadercallback&_=1512560122546')
jd=json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
# jd


# In[113]:

for ent in jd['result']['data']:
    print(ent['url'])


# In[118]:

# 建立剖析清单链接函数
def parseListLinks(url):
    newsdetails = []
    res = requests.get(url)
    jd=json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
    for ent in jd['result']['data']:
        newsdetails.append(getNewsDetail(ent['url']))
    return newsdetails


# In[119]:

url='http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=4&callback=newsloadercallback&_=1512560122546'
parseListLinks(url)


# In[120]:

url='http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1512560122546'
for i in range(1,10):
    newsurl = url.format(i)
    print(newsurl)


# In[135]:

# 批次抓取每页新闻内文
url='http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1512560122546'
news_total = []
for i in range(1,3):
    newsurl = url.format(i)
    newsary = parseListLinks(newsurl)
    news_total.extend(newsary)


# In[138]:

len(news_total)


# In[142]:

import pandas
df = pandas.DataFrame(news_total)
df.head()


# In[143]:

# 保存数据到数据库
df.to_excel('news.xlsx')


# In[144]:

import sqlite3
with sqlite3.connect('news.sqlite') as db:
    df.to_sql('news', con = db)


# In[146]:

import sqlite3
with sqlite3.connect('news.sqlite') as db:
   df2 = pandas.read_sql_query('SELECT * FROM news', con = db)
df2

