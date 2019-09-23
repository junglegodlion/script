# coding=utf-8
import os

for i in range(1,9):
    path = 'F://010-教程//013-微服务//spring2//' + str(i)
    for file in os.listdir(path):
        pre = file.split(".")[0]
        file1 = file.replace(pre, "")
        os.rename(os.path.join(path, file), os.path.join(path, file1))