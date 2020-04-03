'''

'''

print('''
三节课m3u8下载器v2
1、需要先报名这个课程
2、输入课程的id就能下载
3、时间久了可能需要更新一下cookies
''')
import re

import requests
from Crypto.Cipher import AES

headrer = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

# 获取m3u8文件下载地址
m3u8_url = 'http://hls.videocc.net/ef4825bc7e/5/ef4825bc7e600d7a69ace4569cd67585_1.m3u8?pid=1585820852086X1469432&device=desktop'  # 填写m3u8文件的下载地址
m3u8_res = requests.get(m3u8_url).text
m3u8_res = m3u8_res.encode('utf-8', 'ignore').decode('unicode-escape', 'ignore')

URI = 'http://hls.videocc.net/ef4825bc7e/5/ef4825bc7e600d7a69ace4569cd67585_1.key'  # 填入m3u8文件中key的下载地址
key = requests.get(URI, headers=headrer).content  # 获取key值
iv = re.compile('IV=0x(.*)').findall(m3u8_res)  # 获取iv值

ts_url = re.compile('(http://ab-dts.video.*)').findall(m3u8_res)  # 输入ts文件的域名，如果m3u8中ts的路径不全，则需要先补全
file_url = r'./test.mp4'  # 构造文件下载地址

for k in range(len(iv)):
    # 获取ts文件的内容
    ts_contrect = requests.get(ts_url[k])
    # 解密ts文件
    cryptor = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv[k]))
    # 下载ts文件
    with open(file_url, 'ab') as f:
        f.write(cryptor.decrypt(ts_contrect.content))
    print(' 正在下载片段' + str(k).rjust(2, '0') + '.MP4')
print('下载完成！')
