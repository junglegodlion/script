# -*- coding: utf-8 -*-
# @Time : 2019/2/13 8:17 PM
# @Author : cxa
# @File : mp4downloders.py
# @Software: PyCharm
import requests
from tqdm import tqdm
import os
import aiohttp
import asyncio

try:
    # uvloop —— 超级快的 Python 异步网络框架
    import uvloop
    # 下面的代码片段让 asyncio.get_event_loop() 返回一个 uvloop 的实例。
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


async def fetch(session, url, dst, pbar=None, headers=None):
    if headers:
        async with session.get(url, headers=headers) as req:
            with(open(dst, 'ab')) as f:
                while True:
                    chunk = await req.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    pbar.update(1024)
            pbar.close()
    else:
        async with session.get(url) as req:
            return req


async def async_download_from_url(url, dst):
    '''异步'''
    async with aiohttp.ClientSession() as session:
        req = await fetch(session, url, dst)

        file_size = int(req.headers['content-length'])
        print("获取视频总长度:{}".format(file_size))
        if os.path.exists(dst):
            first_byte = os.path.getsize(dst)
        else:
            first_byte = 0
        if first_byte >= file_size:
            return file_size
        # header = {"Range": f"bytes={first_byte}-{file_size}"}
        header = {"Range": "bytes={}".format(first_byte) + "-" + "{}".format(file_size)}
        # tqdm是一个可以显示进度条的包
        pbar = tqdm(
            total=file_size, initial=first_byte,
            unit='B', unit_scale=True, desc=dst)
        await fetch(session, url, dst, pbar=pbar, headers=header)


def download_from_url(url, dst):
    '''同步'''
    response = requests.get(url, stream=True)
    # 通过header的content-length属性可以获取文件的总容量
    file_size = int(response.headers['content-length'])
    if os.path.exists(dst):
        # 获取本地已经下载的部分文件的容量，方便继续下载，当然需要判断文件是否存在，如果不存在就从头开始下载。
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    # 本地已下载文件的总容量和网络文件的实际容量进行比较，如果大于或者等于则表示已经下载完成，否则继续。
    if first_byte >= file_size:
        return file_size
    # header = {"Range": f"bytes={first_byte}-{file_size}"}
    header = {"Range": "bytes={}".format(first_byte) + "-" + "{}".format(file_size)}
    # tqdm是一个可以显示进度条的包
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=dst)
    # 设置stream=True参数读取大文件。
    req = requests.get(url, headers=header, timeout=60, stream=True)
    with(open(dst, 'ab')) as f:
        # 循环读取每次读取一个1024个字节，当然你也可以设置512个字节
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


if __name__ == '__main__':
    # 异步方式下载
    # url = "http://okxzy.xzokzyzy.com/20191011/7990_69a21b71/%E5%9C%B0%E7%8B%B1%E4%B9%8B%E9%9F%B303.mp4"
    # task = [asyncio.ensure_future(async_download_from_url(url, "{}.mp4".format(i))) for i in range(1, 12)]
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.wait(task))
    # loop.close()
    # 注释部分是同步方式下载。
    url = "http://okxzy.xzokzyzy.com/20191011/7990_69a21b71/%E5%9C%B0%E7%8B%B1%E4%B9%8B%E9%9F%B303.mp4"

    download_from_url(url, "夏目友人帐第一集.mp4")