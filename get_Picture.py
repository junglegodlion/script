#！/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import requests
import time
import random
import re
import urllib.parse
import string
import requests
from lxml import etree

keyWord = input('Please input the Keywords that you want to download:')
class Spider():
    #初始化函数
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
        }
        self.filePath = ('E:\\keyWord\\photo\\')#这是我保存图片的路径名


    def creat_File(self,path):   #用os修改目标保存路径
        filePath = path
        if not os.path.exists(filePath): #判断路径是否存在，没有则创建
            os.makedirs(filePath)

    def get_pageNum(self):  #获取总页数
        # total=""
        # url = ("https://wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc").format(keyWord)
        # print(url)
        # html = requests.get(url).text
        # selector = etree.HTML(html)
        # pageInfo = selector.xpath('//header[@class="listing-header"]/h1[1]/text()')
        # print(pageInfo)
        # next_total = str(pageInfo[0])
        # for item in next_total:
        #     # Python isdigit()方法检测字符串是否只由数字组成。
        #     if item.isdigit():
        #         total = total + item
        # totalPagenum = int(total)
        url = ("https://wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc").format(keyWord)
        data = requests.get(url, headers=self.headers, verify=False).content.decode()
        # 用正则表达式获取页数
        pattern = re.compile('data-pagination=.{&quot;total&quot;:(.*?),&quot;')
        totalPagenum = pattern.findall(data)[0]
        return totalPagenum

    def getLinks(self,number):
        pic_downlist = []
        url = ("https://wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc&page={}").format(keyWord,number)
        print(url)
        encode_new_url = urllib.parse.quote(url, safe=string.printable)
        print(encode_new_url)
        html = requests.get(encode_new_url, headers=self.headers, verify=False).text
        selector = etree.HTML(html)
        print(selector)
        pic_Linklist = selector.xpath('//*[@id="thumbs"]/section[@class="thumb-listing-page"]/ul//li/figure/a[@class="preview"]/@href')
        for item in pic_Linklist:
            html_in = requests.get(item, headers=self.headers, verify=False).text
            selector_in = etree.HTML(html_in)
            pic_willdownlist = selector_in.xpath('//*[@id="wallpaper"]/@src')[0]
            pic_downlist.append(pic_willdownlist)
        return pic_downlist

    def download(self,url,count):
        """
        https://alpha.wallhaven.cc/网站上据我抽样点取，发现基本都是JPG,PNG格式的图片,

        demo："https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-635067.jpg"
              "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-626126.png "
        要保存图片，必须就要在文件名上加上该格式得后缀，实在想不出办法只能出此愚见
        (
         在传入每一个该图片的url后做一个判断，判断该后缀后取出保存作为路径名
         )
        :param url: 在getLinks()上取得每一张图片响应链接后的真实url
        :param count: 第*张图片
        :return: None
        """
        path = self.filePath + keyWord
        self.creat_File(path)
        if url.endswith('.jpg'):
            pic_path = (self.filePath + keyWord +"\\" + str(count)+'.jpg')
        elif url.endswith('.png'):
            pic_path = (self.filePath + keyWord + "\\" +  str(count)+'.png')
        try:
            pic = requests.get(url, headers=self.headers,verify=False)
            print(pic_path)
            f = open(pic_path, 'wb')
            f.write(pic.content)
            f.close()
            print("Image:{} has been downloaded!".format(count))
            # random.uniform(x, y)方法将随机生成一个实数，它在[x, y]范围内。
            time.sleep(random.uniform(0, 2))
        except Exception as e:
            print(repr(e))

    def main_fuction(self):
         #count是图片总数，times是总页面数
        # self.creat_File()    #创建该工程保存目录
        count = self.get_pageNum()   #获得页数count
        print("We have found:{} 页!".format(count)) #打印出来有多少页图片
        times = int(count)
        j = 1
        for i in range(times):   #每一页开始遍历
            pic_Urls = self.getLinks(i + 1)  #获取第一页
            for item in pic_Urls:    #在第一页获取的响应连接逐个开始遍历
                self.download(item, j)  #调用下载函数传入item作为url，j用来计数
                j += 1
spider = Spider()
spider.main_fuction()