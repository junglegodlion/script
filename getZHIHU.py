from urllib import request
from bs4 import BeautifulSoup
import requests
import re
import json
import math


def getVideo():
    m = 0  # 计数字串个数
    num = 0  # 回答者个数
    path = u'E:/data/video'
    # path = u'/home/zhihuimage'
    kv = {'user-agent': 'Mozillar/5.0'}
    # ceil() 函数返回数字的上入整数。
    for i in range(math.ceil(900 / 20)):
        try:
            url = "https://www.zhihu.com/api/v4/questions/312311412/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=20&offset=" + str(
                i * 20) + "&platform=desktop&sort_by=default"
            r = requests.get(url, headers=kv)
            # 用requests.get函数获得json文件，再使用json.loads函数转换成Python对象
            dicurl = json.loads(r.text)
            # print(dicurl)
            for k in range(20):  # 每条dicurl里可以解析出20条content数据
                name = dicurl["data"][k]["author"]["name"]
                ID = dicurl["data"][k]["id"]
                question = dicurl["data"][k]["question"]["title"]
                content = dicurl["data"][k]["content"]
                data_lens = re.findall(r'data-lens-id="(.*?)"', content)
                print("正在处理第" + str(num + 1) + "个回答--回答者昵称:" + name + "--回答者ID:" + str(ID) + "--" + "问题:" + question)
                num = num + 1  # 每次碰到一个content就增加1，代表回答者人数
                for j in range(len(data_lens)):
                    try:
                        videoUrl = "https://lens.zhihu.com/api/v4/videos/" + str(data_lens[j])
                        R = requests.get(videoUrl, headers=kv)
                        # 用requests.get函数获得json文件，再使用json.loads函数转换成Python对象
                        Dicurl = json.loads(R.text)
                        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                        print(Dicurl)
                        playurl = Dicurl["playlist"]["LD"]["play_url"]
                        # print(playurl)#跳转后的视频url
                        videoread = request.urlopen(playurl).read()

                        fileName = path + "/" + str(m + 1) + '.mp4'
                        print('===============================================')
                        print(">>>>>>>>>>>>>>>>>第---" + str(m + 1) + "---个视频下载完成<<<<<<<<<<<<<<<<<")
                        videoname = open(fileName, 'wb')

                        videoname.write(videoread)
                        m = m + 1
                    except:
                        print("此URL为外站视频,不符合爬取规则")
        except:
            print("构造第" + str(i + 1) + "条json数据失败")


if __name__ == "__main__":
    getVideo()