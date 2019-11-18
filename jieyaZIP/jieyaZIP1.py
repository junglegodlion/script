import zipfile

def extractFile(zipFile, password):
    try:
        zipFile.extractall(pwd= bytes(password, "utf8" ))
        print("李大伟的压缩包密码是" + password)  #破解成功
    except:
        pass  #失败，就跳过

"""
生成从000000到99999的密码表
"""
def getDictionary():
    f = open('passdict.txt', 'w')
    for id in range(1000000):
        #  zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。
        password = str(id).zfill(6) + '\n'
        f.write(password)
    f.close()

def main():
    zipFile = zipfile.ZipFile('ppt.zip')
    PwdLists = open('passdict.txt')   #读入所有密码
    for line in PwdLists.readlines():   #挨个挨个的写入密码
        Pwd = line.strip('\n')
        guess = extractFile(zipFile, Pwd)

if __name__ == '__main__':

    main()