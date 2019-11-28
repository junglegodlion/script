import pymysql
# 参数设置 DictCursor使输出为字典模式 连接到本地用户root 密码为123456
conn = pymysql.connect(host="192.168.1.18", port=8806, user="root", passwd="123456")
conn.autocommit(True)
cursor = conn.cursor()

import pandas as pd
# pandas读取文件 这里随便找了一个爬取的股票文件改的名字
# usecols 就是说我只用这些列其他列不需要
# parse_dates 由于csv只储存str、int、float格式无法储存日期格式，所以读取是设定吧日期列读作时间格式
# df = pd.read_csv('stock.csv', encoding='gbk', usecols=[0, 3, 4, 5, 6, 11], parse_dates=['日期'] )
df = pd.read_csv('tags.csv', encoding='gbk')
print(df.head())

# 一个根据pandas自动识别type来设定table的type
def make_table_sql(df):
    columns = df.columns.tolist()
    types = df.ftypes
    # 添加id 制动递增主键模式
    make_table = []
    for item in columns:
        if 'int' in types[item]:
            char = item + ' INT'
        elif 'float' in types[item]:
            char = item + ' FLOAT'
        elif 'object' in types[item]:
            char = item + ' VARCHAR(255)'
        elif 'datetime' in types[item]:
            char = item + ' DATETIME'
        make_table.append(char)
    return ','.join(make_table)


# csv 格式输入 mysql 中
def csv2mysql(db_name, table_name, df):
    # 创建database
    cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
    # 选择连接database
    conn.select_db(db_name)
    # 创建table
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    cursor.execute('CREATE TABLE {}({})'.format(table_name, make_table_sql(df)))
    values = df.values.tolist()
    # 根据columns个数
    s = ','.join(['%s' for _ in range(len(df.columns))])
    # executemany批量操作 插入数据 批量操作比逐个操作速度快很多
    cursor.executemany('INSERT INTO {} VALUES ({})'.format(table_name, s), values)

# csv2mysql(数据库名,表,df)
csv2mysql("wt","tags",df)


# 光标关闭
cursor.close()
# 连接关闭
conn.close()
