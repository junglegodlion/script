import requests
from lxml import etree
import yagmail
import zmail

"""
爬取天气信息
"""
def parse(url='https://www.tianqi.com/shanghai'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    html = requests.get(url, headers=headers)
    bs = etree.HTML(html.text)

    # 今天天气相关数据：日期，星期几，天气，最低气温，最高气温
    today_date = bs.xpath('//ul[@class = "week"]/li[1]/b/text()')[0]
    today_week = bs.xpath('//ul[@class = "week"]/li[1]/span/text()')[0]
    today_weather = bs.xpath('//ul[@class = "txt txt2"]/li[1]/text()')[0]
    today_low = bs.xpath('//div[@class = "zxt_shuju"]/ul/li[1]/b/text()')[0]
    today_high = bs.xpath('//div[@class = "zxt_shuju"]/ul/li[1]/span/text()')[0]

    # 明天天气相关数据，维度和上述一致
    tomorrow_date = bs.xpath('//ul[@class = "week"]/li[2]/b/text()')[0]
    tomorrow_week = bs.xpath('//ul[@class = "week"]/li[2]/span/text()')[0]
    tomorrow_weather = bs.xpath('//ul[@class = "txt txt2"]/li[2]/text()')[0]
    tomorrow_low = bs.xpath('//div[@class = "zxt_shuju"]/ul/li[2]/b/text()')[0]
    tomorrow_high = bs.xpath('//div[@class = "zxt_shuju"]/ul/li[2]/span/text()')[0]

    tomorrow = ('明天是%s，%s,%s，%s-%s度，温差%d度') % \
               (tomorrow_date, tomorrow_week, tomorrow_weather, tomorrow_low, tomorrow_high,
                int(int(tomorrow_high) - int(tomorrow_low)))

    print(('明天是%s，%s,%s，%s-%s度，温差%d度') % \
          (tomorrow_date, tomorrow_week, tomorrow_weather, tomorrow_low, tomorrow_high,
           int(int(tomorrow_high) - int(tomorrow_low))))

    # 计算今明两天温度差异，这里用的是最高温度
    temperature_distance = int(tomorrow_high) - int(today_high)

    if temperature_distance > 0:
        a = '明日升温%d' % temperature_distance
        print('明日升温%d' % temperature_distance)
    if temperature_distance < 0:
        a = '明日降温%d' % temperature_distance
        print('明日降温%d' % temperature_distance)
    else:
        a = '最高气温不变'
        print('最高气温不变')
    content = tomorrow, a
    return content

"""
发送邮件方式二，使用yagmail
"""
def send_email(contents, send_to='receiver_email@xx.com'):
    """

    :param contents: 要发送的内容
    :param send_to: 收件人邮箱
    :return:
    """
    # 登录邮箱，设置登录的账号，密码和port等信息
    yag = yagmail.SMTP(user='junglegodlion@163.com', password='这里填写授权码',
                       host='smtp.163.com', port='465')

    # 登录完即可一件发送，设置发送给谁，和邮件主题，邮件内容
    yag.send(to=send_to,
             subject='这里填写主题',
             contents=contents)
    print('发送成功！~')

"""
发送邮件方式一，使用zmail
"""
def sendEmail(content):
    """
    发送邮件
    :param content: 要发送的内容
    :return:
    """
    # 发件人邮箱
    server = zmail.server('junglegodlion@163.com', '这里填写授权码')
    mail = {
        'subject': '这里填写主题 ',
        'content_text': content,
    }
    # 收件人邮箱
    server.send_mail('1037044430@qq.com', mail)

if __name__ == '__main__':
    # 默认爬取上海，可以找到自己城市所对应的地址
    weather = parse()
    send_email(weather,send_to = '1037044430@qq.com')

