import json

import requests
import random
import base64
import os
import platform
from shutil import which
from datetime import datetime
from PIL import Image
from termcolor import colored
from sys import exit

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# 模拟用户请求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
}


# 初始函数 设置lsp_info.log | 下载 apt 包
def init():
    # linux环境下需要
    if which('imagemagick') and platform.system() == 'Linux':
        if input("Install imagemagick? [y/n]").lower() == 'y':
            os.system("sudo apt-get install imagemagick")

def check_login():
    """
    登录检查
    :return:
    """
    with open('../lsp_info.json', 'r', encoding='utf-8') as log_f:
        t = datetime.now()
        current_time = f"{str(t.day)}/{str(t.month)}/{str(t.year)}"

        try:
            last_log_time = log_f.readlines()[-1].strip('\n')
            if last_log_time == current_time:
                exit("一天只能抽一张图哦！注意身体 " + colored(":p", 'yellow'))

        except IndexError:
            print('error')


def choose_img():
    """
    随机抽取图片
    1、请求图库地址
    2、
    :return:
    """
    # Read directories under lsp-db
    re = requests.get(pic_repository, headers=headers)

    #加载为json对象
    temp = json.loads(re.text)

    # print(re.text)

    temp = temp['payload']['tree']['items']

    img_list = []  # all of the images names in the LSP database

    for link in temp:
        img_list.append(link['name'])

    # Randomly choose one image in the img_list
    name = random.choice(img_list)

    # Get the url of the chosen image
    url = f"https://raw.githubusercontent.com/lan2lang/lsp_pic/master/lsp-db2/{name}"
    # url = f"https://gitee.com/lang_zou/lsp_pic/raw/master/lsp-db/{name}"
    print("访问 " + colored(url, 'green'))

    # Download the image
    with open(f"{name}.jpg", 'wb') as img_f:
        lsp_content = requests.get(url).content
        img_f.write(lsp_content)

        return f"{name}.jpg"


def main():
    # 随机抽取图片
    img_name = choose_img()

    print(f"显示图片 [{colored(img_name, 'red')}]")

    # Show image
    with Image.open(img_name) as image:
        image.show()

    #删除图片
    os.remove(img_name)


if __name__ == "__main__":
    # init()
    # 图库地址（github）
    pic_repository='https://github.com/lan2lang/lsp_pic/tree/main/lsp-db2'
    # gitee
    # pic_repository='https://gitee.com/lang_zou/lsp_pic/tree/master/lsp-db'
    main()
