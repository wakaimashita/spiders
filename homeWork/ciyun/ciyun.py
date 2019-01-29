#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :        hayden_huang
   Date：          2018/12/17 15:04
-------------------------------------------------
"""
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from PIL import Image
from os import path
import numpy as np
import requests
from lxml.etree import HTML

# url = 'http://jtt.xizang.gov.cn/xwzx/xzxw/index_1.html'
# headers = {
#     'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     'Accept-Encoding': "gzip, deflate",
#     'Accept-Language': "zh-CN,zh;q=0.9",
#     'Cache-Control': "no-cache",
#     'Connection': "keep-alive",
#     'Host': "jtt.xizang.gov.cn",
#     'Pragma': "no-cache",
#     'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
#     'cache-control': "no-cache",
# }
# response = requests.get(url,headers=headers)
# response.encoding = 'utf8'
# html = HTML(response.text)
# urls = html.xpath('//div[@class="gl-main-itm"]//ul[@class="list"]/li/a/@href')
# for url in urls[:10]:
#     link = 'http://jtt.xizang.gov.cn/xwzx/xzxw'+url[1:]
#     print(link)
#     detail = requests.get(link)
#     detail.encoding = 'utf8'
#     detail_html = HTML(detail.text)
#     conten = detail_html.xpath('//div[@class="dfz-xl-sp"]/p//text()')
#     conten = ''.join(conten).replace('\n','').replace('\t','')
#     with open('news.txt','a',encoding='utf8',errors='ignore') as f:
#         f.write(conten)


text = open("mytxt.txt", "rb").read()
# 结巴分词
wordlist = jieba.cut(text, cut_all=True)
wl = " ".join(wordlist)

d = path.dirname(__file__)

alice_mask = np.array(Image.open(path.join(d, "china.jpg")))
# 设置词云
wc = WordCloud(background_color="white",  # 设置背景颜色
               mask = alice_mask,  #设置背景图片
               max_words=2000,  # 设置最大显示的字数
               # stopwords = "", #设置停用词
               # font_path="C:\Windows\Fonts\SimHei.ttf",
               font_path="/System/Library/Fonts/PingFang.ttc",
               max_font_size=50,  # 设置字体最大值
               random_state=30,
               )
myword = wc.generate(wl)  # 生成词云

# 展示词云图
plt.imshow(myword)
plt.axis("off")
plt.show()