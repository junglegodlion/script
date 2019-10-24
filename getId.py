import time

#生成出生当年所有日期
def dateRange(year):
    fmt = '%Y-%m-%d'
    bgn = int(time.mktime(time.strptime(year+'-01-01',fmt)))
    end = int(time.mktime(time.strptime(year+'-12-31',fmt)))
    list_date = [time.strftime(fmt,time.localtime(i)) for i in range(bgn,end+1,3600*24)]
    return [i.replace('-','') for i in list_date]

data_time  = dateRange('1995')
print(data_time)


# pip install id-validator
# 可以用来验证身份证号合法性、获取身份证号信息、生成可通过校验的假数据、身份证升级。
from id_validator import validator

#遍历所有日期，print通过校验的身份证号码

def vali_dator(id1,id2,id3):
    for i in dateRange(id2):
        theid = id1 + i + id3
        if validator.is_valid(theid):
            print(theid)

vali_dator('330221','1993','4914')