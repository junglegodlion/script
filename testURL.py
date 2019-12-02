# !/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'jungle'
import requests
from lxml import etree
import time
import json
import xlrd
import openpyxl

okurl = []

"""
验证url是否可以访问
"""
def testIP(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    }
    try:
        if url.startswith( 'http://' ):
            url = url
        else:
            url = "http://" + url
        response = requests.get(url,headers=headers,timeout=5)
        if response.status_code == 200:
            okurl.append("可以访问")
        else:
            okurl.append("不可以访问")
    except:
        print('connect failed')
        okurl.append("不可以访问")
        return
    else:
        print(response.status_code)



import pandas as pd

# r使'\'不转义
df = pd.read_excel(r'E:\\code\\python\\爬虫\\test\\123.xlsx')


allurl = df["域名"].values.tolist()

for url in allurl:
    # print(str(url).strip())
    # 去除前后空格
    testurl = str(url).strip()
    testIP(url)
df['是否可用']= okurl

# 另存为xlsx文件
df.to_excel('ok.xlsx')


