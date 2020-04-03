'''
站点地址
https://www.sanjieke.cn/free.html
课程列表json
https://class.sanjieke.cn/course/class_content_with_checkpoint?cid=3003359
加载第一个视频页面
https://class.sanjieke.cn/course/section_content?cid=3003359&section_id=1673672
https://class.sanjieke.cn/course/class_content_with_checkpoint?cid=17301420
加载第一个视频
https://service.sanjieke.cn/video/master/1673668.m3u8?class_id=3003359
从加载页中取出m3u8文件地址
https://service.sanjieke.cn/video/media/1673668/608p.m3u8?class_id=3003359
获取key地址
https://service.sanjieke.cn/video/key/1673668?class_id=3003359
'''

print('''
三节课m3u8下载器v2
1、需要先报名这个课程
2、输入课程的id就能下载
3、时间久了可能需要更新一下cookies
''')
import os
import re

import requests
from Crypto.Cipher import AES

headrer = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
    'Cookie':'acw_tc=276aedd715843843846276228e7237cfd3f2985ec8423b6b72e1f786d0f2f0; sajssdk_2015_cross_new_user=1; PHPSESSID=8c8i2ohp56ah69jr6i8jp07pa5; sjk_jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyIiwianRpIjoiNDE4ZDViOWRjOTQ3YjFmYzNjMGM5MzhmODgxMzU0NmMzZDgwMGQ5NWVkM2JlMjlhNjQ4MmFkODAyMTZlNGU0ZTdiMDY1OWMwNjA3ZDJlMDkiLCJpYXQiOjE1ODQzODQ0MTcsIm5iZiI6MTU4NDM4NDQxNywiZXhwIjoxNTg3MDYyODE3LCJzdWIiOiIyMDc5NTY2NiIsInNjb3BlcyI6W119.bykO1OWL9_mqZKhI6qEpwwrbTEpEk25Xc-bwFXG47lktpRfKLBPw22WOUqYRfl0qi-WkkItBgcEe9TVU8jfFcg; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2220795666%22%2C%22%24device_id%22%3A%22170e4ab2004b55-0f846e6d4f2e96-4313f6a-3686400-170e4ab2005aa9%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fs%22%2C%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E4%B8%89%E8%8A%82%E8%AF%BE%22%7D%2C%22first_id%22%3A%22170e4ab2004b55-0f846e6d4f2e96-4313f6a-3686400-170e4ab2005aa9%22%7D; Hm_lvt_85148c078fe4635816b80e5a36990313=1584384385,1584384418; Hm_lpvt_85148c078fe4635816b80e5a36990313=1584384436'
}
class_id =input('请输入课程编号:')
# 获取这个课程所有课时的ID
class_url = 'https://class.sanjieke.cn/course/class_content_with_checkpoint?cid='+class_id
class_contect = requests.get(class_url,headers=headrer).text.encode('utf-8').decode('unicode-escape')
course_title = re.compile('"course_title":"(.*?)"',re.S).findall(class_contect)

if len(course_title)==0:
    print('课程不在有效期内或未报名')
    raise IndexError
course_title = course_title[0]

course_id_name_list = re.compile('"node_id":(\d*),.*?"title":"(.*?)"',re.S).findall(class_contect) # 课时ID,名称
# 创建与课程同名文件夹
course_title = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", course_title)
if not os.path.exists(r'./' + r'./' + course_title):  # 判断文件夹是否存在
    os.makedirs(r'./' + r'./' + course_title)  # 如果不存在则创建文件夹
# 获取m3u8文件的ID以及对应的名称
i = 1
for course_id_name in course_id_name_list:
    course_url = 'https://class.sanjieke.cn/course/section_content?cid='+class_id+'&section_id='+course_id_name[0]
    course_contect = requests.get(course_url,headers=headrer)
    course_contect = course_contect.text.replace('\\/','/').encode('utf-8','ignore').decode('unicode-escape','ignore')
    course_m3u8_id = re.compile('"id":"(\d*)"', re.S).findall(course_contect)
    if  len(course_m3u8_id) == 0:
        course_m3u8_id = re.compile('"id":(\d*)', re.S).findall(course_contect)
    # 读取每个m3u8文件的内容
    if not len(course_m3u8_id) == 0:
        # 获取m3u8文件下载地址
        course_m3u8_url = 'https://service.sanjieke.cn/video/master/'+course_m3u8_id[0]+'.m3u8?class_id='+class_id[0]
        course_m3u8_contect = requests.get(course_m3u8_url,headers=headrer).text.replace('\\/','/')
        course_m3u8_contect = course_m3u8_contect.encode('utf-8','ignore').decode('unicode-escape','ignore')
        course_m3u8_down_url = re.compile('http.*?\.m3u8',re.S).findall(course_m3u8_contect)[0]
        # 读取m3u8文件原始内容
        m3u8_res = requests.get(course_m3u8_down_url,headers=headrer).text
        m3u8_res = m3u8_res.encode('utf-8','ignore').decode('unicode-escape','ignore')

        URI = 'https://service.sanjieke.cn/video/key/'+course_m3u8_id[0]
        key = requests.get(URI,headers=headrer).content
        iv = re.compile('IV=0x(.*)').findall(m3u8_res)

        ts_url = re.compile('(https://vcdn.*)').findall(m3u8_res)
        file_url = r'./' + course_title + r'./ ' + str(i).rjust(2, '0') + ' ' + course_id_name[1] + '.mp4'  #构造文件下载地址

        for k in range(len(iv)):
            # 获取ts文件的内容
            ts_contrect = requests.get(ts_url[k])
            # 解密ts文件
            cryptor = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv[k]))
            # 下载ts文件
            with open(file_url, 'ab') as f:
                f.write(cryptor.decrypt(ts_contrect.content))
            print(' 正在下载片段'+str(k).rjust(2, '0') + ' ' + course_id_name[1] + '.MP4')
        print(str(i).rjust(2, '0') + ' ' + course_id_name[1] + '.MP4' + ' 下载成功！')
        i = i + 1
print(course_title +'下载完成！')