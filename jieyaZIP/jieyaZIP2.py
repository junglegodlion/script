# coding = utf-8

"""
@author: sy
@file: zip_hack.py
@time: 2018/11/23 22:13
@desc: 读取txt文档，进行多线程跑字典方式进行爆破
"""
import optparse
import zipfile
from threading import Thread
from tqdm import tqdm


def extract_file(zip_file, password):
    """ 提取压缩文件，通过密码不断尝试 """
    try:
        zip_file.extractall(pwd=bytes(password, 'utf-8'))
        print('\n  发现密码，正确密码为：{}'.format(password))
    except:
        pass


def main():
    """ 通过optparse模块进行py命令行形式脚本操作，获取字典和zip路径 """
    # 第一行通过调用optparse的函数创建一个parser的实例化对象
    parser = optparse.OptionParser('\n  %prog -z <zipfile> -d <dictionary>')
    # 第二行添加一个参数，在命令行上输入-z xxxx 可将命令行上的zip路径作为字符串传入到变量zname中
    parser.add_option('-z', dest='zname', type='string', help='specify zip file')
    # 第三行添加一个参数，在命令行上输入-d xxxx 可将命令行上的字典文件作为字符串传入到变量dname中
    parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')
    # 第四行进行解析，得到相关参数，得到options。
    options, args = parser.parse_args()
    # 第五行，通过zname和dname判断是否传入的参数为空
    if options.zname and options.dname:
        zip_name = options.zname
        dict_name = options.dname
    else:
        print(parser.usage)
        exit(0)

    """
    测试用的目录文件,为了用pycharm调试，可将上述代码注释掉
    zip_name = 'C:/Users/sy/Desktop/secret_file.zip'
    dict_name = 'C:/Users/sy/Desktop/secret_dict.txt'
    """
    try:
        # 调用zipfile模块的实例对象方法，将zip路径传入
        zip_file = zipfile.ZipFile(zip_name)
        # 打开字典文件，用python自带的with关键词来打开，可以交由python自主关闭文件的资源
        with open(dict_name, 'r', encoding='utf-8') as f:
            # 读取每一行，并且将密码后的\n 清空，也就是清空换行符
            for line in tqdm(f.readlines()):
                password = line.strip('\n')
                # 对每个密码开启线程去处理，调用extract_file函数，传入的参数为元组(zip_file, password)
                # 开启多线程
                thread = Thread(target=extract_file, args=(zip_file, password))
                # 调用线程开始的方法
                thread.start()
    except Exception as e:
        print('发生异常！请检查文件是否存在！异常信息为：{}'.format(e))


main()