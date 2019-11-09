# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
(1)：思路抓取所有的代理id，做好区分http还是https的代理。
(2): 代理洗澡，过滤掉所有反应时间大于1秒的代理。
(3): 测试代理：。。。
"""
__author__ = 'jungle'
import requests
from lxml import etree
import time
import json


"""
启动函数，访问目标网站，获取其html文本信息
使用了生成器的功能
"""
def start(start_url, n):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    }
    for i in range(1, n+1):
        try:
            response = requests.get(start_url.format(i), headers=headers)
            if response.status_code == 200:
                # print(response.text)
                yield response.text
        except Exception as e:
            _ = e  # 占位，编写规范
            print('发生了未知错误')

"""
匹配函数，提取所需内容
"""
def match_data(content):
    # print("进入match_data")
    data_contains = []
    rsp = etree.HTML(content)
    for i in range(2, 102):
        # Xpath string()提取多个子节点中的文本
        # split()当没有参数的情况下，函数默认会以空格，回车符，空格符等作为分割条件。
        # ['114.239.0.10', '808', '江苏宿迁', '高匿', 'HTTPS', '859天', '19-11-09', '11:00']
        string_one_item = 'string(//table[@id="ip_list"]/tr['+str(i)+'])'
        one_item = rsp.xpath(string_one_item).split()
        # print(one_item)
        # one_item_speed则是速度，
        string_one_item_speed = '//table[@id="ip_list"]/tr['+str(i)+']/td[7]/div/@title'
        one_item_speed = rsp.xpath(string_one_item_speed)[0]
        # print(one_item_speed)
        # one_item_link_speed则是链接速度
        string_one_item_link_speed = '//table[@id="ip_list"]/tr['+str(i)+']/td[8]/div/@title'
        one_item_link_speed = rsp.xpath(string_one_item_link_speed)[0]
        # print(one_item_link_speed)
        proxy_data = {"proxy": ":".join([one_item[0], one_item[1]]),
                      "proxy_scheme": one_item[-4],
                      'speed': one_item_speed,
                      'link_speed': one_item_link_speed}
        proxy_data = clean_data(proxy_data)
        if proxy_data:  # 如果不为空，没被过滤掉则加入容器
            data_contains.append(proxy_data)
    return data_contains

"""
过滤出速度，连接速度大于1秒的IP数据
"""
def clean_data(data):
    import re
    # eval() 函数用来执行一个字符串表达式，并返回表达式的值。
    # Python字典(Dictionary)get()函数返回指定键的值，如果值不在字典中返回默认值。
    # 正则re.findall的简单用法（返回string中所有与pattern相匹配的全部字串，返回形式为数组）
    # findall(pattern, string, flags=0)
    # \d对于Unicode（str类型）模式：匹配任何一个数字，包括[0 - 9]和其他数字字符；
    data_speed = eval(re.findall('\d\.\d+', data.get('speed', ''))[0])
    data_link_speed = eval(re.findall('\d\.\d+', data.get('link_speed', ''))[0])
    # 过滤掉所有速度、连接时间 > 1秒的代理。
    if data_speed < 1 and data_link_speed < 1:
        cleaned_data = {'proxy': data.get('proxy', ''), 'proxy_scheme': data.get('proxy_scheme', '')}
        # return cleaned_data
        test_data = testIP(cleaned_data)
        return test_data
    else:
        return

"""
保存写入文件函数，写入数据
"""
def save_data(file_name, data):
    with open('{}.json'.format(file_name), 'a', encoding='utf-8') as f:
        file_line = json.dumps(data)
        f.write('{}'.format(file_line))

"""
验证IP是否可用
"""
def testIP(cleaned_data):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    }
    proxy = cleaned_data.get('proxy', '')
    proxy_scheme = cleaned_data.get('proxy_scheme', '').lower()
    proxies = ":".join([proxy_scheme,proxy])
    dict_proxies={proxy_scheme:proxies}
    print("~~~~~~~~~~~~")
    print(dict_proxies)
    try:
        requests.get('http://wenshu.court.gov.cn/',headers=headers, proxies=dict_proxies, timeout=3)
    except:
        print('connect failed')
        return
    else:
        print('success')
        return cleaned_data


if __name__ == '__main__':
    count = 1  # 计数
    # 启动链
    start_url = 'http://www.xicidaili.com/nn/{}'
    # 输入保存的文件名
    file_name = input('请输入保存的文件名:')
    climb_page = int(input('请输入你要摸多少页:'))
    all_data = []  # 用于存放所有的信息
    for i in start(start_url, climb_page):
        print('正在执行抓取第%d页' % count)
        data = match_data(i)
        # extend()函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）。
        all_data.extend(data)
        count += 1
        time.sleep(3)
    save_data(file_name, all_data)  # 定义文件名，接受所有的信息写入文件