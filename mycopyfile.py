import re
import os
import shutil

# 读取文件内容
def readData(path):
    with open(path, 'r',encoding='utf-8') as f:
        data = f.read()
    return data

# 替换md中的内容
def subMD(data,path):
    num = re.compile('(C..Users.jungle.AppData.Roaming.Typora.typora-user-images.)').sub("picture/", data)
    with open(path, 'w', encoding='utf-8') as d:
        d.write(num)


# 找到图片编号
def findPictNum(data):
    num = re.compile('C..Users.jungle.AppData.Roaming.Typora.typora-user-images.(.*?).png').findall(data)
    return num


# 构造图片地址
def findPictrue(data):
    num = findPictNum(data)
    pict = []
    for i in num:
        j = ('C://Users//jungle//AppData//Roaming//Typora//typora-user-images//') + i + '.png'
        pict.append(j)
    return pict


# 复制图片到指定文件夹
def mycopyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))

    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstfile))


if __name__ == '__main__':
    path = 'README.md'
    data=readData(path)
    subMD(data,'123.md')
    num = findPictNum(data)
    addr = findPictrue(data)
    for i in range(0, len(addr)):
        srcfile = addr[i]
        dstfile = 'C://Users//jungle//AppData//Roaming//Typora//typora-user-images//picture//' + num[i] + '.png'
        mycopyfile(srcfile, dstfile)


