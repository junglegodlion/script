#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import time
import requests
import pymysql

"""
组合得出省市名称
"""
def get_address(x):
    address = []
    s = list(x.keys())  # 省列表
    for i in s:
        sheng = i
        for j in x[sheng]:
            city = j
            name = str(sheng) + str(city)
            address.append(name)
    return address

"""
生成经纬度
"""
# 方法一，这个不是很好用
# geolocator = Nominatim()
# def get_latitude_longitude(name,num):
#     latitude_longitude = None
#     for i in range(10):
#         try:
#             location = geolocator.geocode(name, timeout=200)
#             latitude_longitude = str(location.latitude) + "," + str(location.longitude)
#             print(name + '第' + str(i) +'次' + ' 砍杀')
#             return latitude_longitude.split(",")[num]
#         except Exception as e:
#             print(e)
#             time.sleep(1)
#             print(name+ ' 本次超时，等1秒继续')
#
#     if latitude_longitude == None:
#         return 0

# 方法二：应用高德api
def get_latitude_longitude(address):
    par = {'address': address, 'key': 'b95db2c663cf3e34ee731f70e1469bf1'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, par)
    answer = response.json()
    # print(answer)
    GPS = answer['geocodes'][0]['location'].split(",")
    return GPS[0], GPS[1]


"""
随机生成0-1之间的小数
"""
def generate_random(num):
    list=[]
    for i in range(0,num):
        m=('%.3f' % random.random())
        list.append(m)
    return list


"""
生成日期列表
转成字符串
"""
def generate_date(date,num):
    date_list=[]
    date = pd.date_range(date, periods=num)
    ts_list = [str(ele) for ele in date]
    print(ts_list)
    for i in ts_list:
        # print(i)
        # 转换成时间数组
        timeArray = time.strptime(i, "%Y-%m-%d %H:%M:%S")
        # print(timeArray)
        # 转换成时间戳
        timestamp = time.mktime(timeArray)
        timestamp2=str(timestamp).split(".")[0]+"000"
        date_list.append(timestamp2)
    return date_list

"""
将数据整理成可存入MySQL的样式
"""
def mysql_data(x,date,num):
    list=[]
    address=get_address(x)
    for i in address:
        latitude,longitude=get_latitude_longitude(i)
        timestamp=generate_date(date,num)
        for j in timestamp:
            data=[]
            data.append("0")
            num_random=generate_random(3)
            data.append(i)
            data.append(j)
            data.append(latitude)
            data.append(longitude)


            for m in num_random:
                data.append(m)
            print(data)
            list.append(data)
    return list



"""
保存列表至文件
"""
def save_txt(file_name,list):
    with open(file_name, 'w') as f:
        f.write(list)



"""
将数据存入数据库
"""

def save_mysql(list):
    print("进来了")
    try:
        # 1.链接 数据库  链接对象 connection()
        conn = pymysql.Connect(
            host="192.168.1.18",
            port=9906,
            db='soil',
            user='root',
            passwd="123456",
            charset='utf8'
        )
        # 2. 创建 游标对象 cursor()
        cur = conn.cursor()
        for i in list:
            print(i)
            sql = "insert into pollution(name,times,latitude,longitude,mercury,plumbum,petroleum) values('" + i[1] + "','" + i[2] + "','" + i[3]+ "','" + i[4] +"','"+ i[5] + "','" + i[6]+ "','" + i[7] +"')"
            # sql = "insert into goods(title,link,comment) values('" + i[1] + "','" + i[2] + "','" + i[3] + "')"
            print(sql)
            result = cur.execute(sql)
        # 提交事务
        conn.commit()
        # 关闭游标
        cur.close()
        # 关闭链接
        conn.close()

    except Exception as e:
        print(e)



if __name__ == '__main__':
    x = {'河北省': ['石家庄', '唐山', '秦皇岛', '承德'],
         '山东省': ['济南', '青岛', '临沂', '淄博'],
         '湖南省': ['长沙', '衡阳', '湘潭', '邵阳', '岳阳', '株洲'],
         '江西省': ['南昌', '九江', '上饶', '景德镇'],
         '浙江省': ['金华', '舟山', '杭州', '宁波'],
         '安徽省': ['合肥', '黄山', '阜阳', '芜湖'],
         '江苏省': ['连云港','南通','南京', '徐州']}
    # address = get_address(x)
    # print(address)
    # date=generate_date("20181010",5)
    # print(date)
    # m=generate_random(4)
    # print(m)

    # 获取想要的数据格式
    list=mysql_data(x,"20191024",30)
    print(list)
    print("开始向MySQL保存数据")
    # 存入MySQL数据库
    save_mysql(list)
    # str_list=str(list)
    # save_txt("list.txt",str_list)
