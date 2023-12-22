import json

import requests
import random
import base64
import os
import logging
import platform
from shutil import which
from datetime import datetime
from bs4 import BeautifulSoup
from PIL import Image
from termcolor import colored
from sys import exit

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
}


# 初始函数 设置lsp_info.log | 下载 apt 包
def init():
    # if os.path.exists("lsp_info.log"):
    #     check_login()
    # else:
    #     with open("lsp_info.log", "wb") as file:
    #         file.write(b"")
    #         print("完成初始设置")

    if which('imagemagick') and platform.system() == 'Linux':
        if input("Install imagemagick? [y/n]").lower() == 'y':
            os.system("sudo apt-get install imagemagick")


def check_login():
    with open('lsp_info.json', 'r', encoding='utf-8') as log_f:
        t = datetime.now()
        current_time = f"{str(t.day)}/{str(t.month)}/{str(t.year)}"

        try:
            last_log_time = log_f.readlines()[-1].strip('\n')
            if last_log_time == current_time:
                exit("一天只能抽一张图哦！注意身体 " + colored(":p", 'yellow'))

        except IndexError:
            print('error')


# app_logging()


# def app_logging():
#     t = datetime.now()
#     log = "lsp_info.log"
#     logging.basicConfig(filename=log, level=logging.DEBUG, format='%(asctime)s',
#                         datefmt=f"{str(t.day)}/{str(t.month)}/{str(t.year)}")


def choose_img():
    # Read directories under lsp-db
    re = requests.get("https://github.com/lan2lang/lsp_pic/tree/main/lsp-db", headers=headers)
    # with open("lsp_info.json", "w") as file:
    #     file.write(re.text)
    print()
    # soup = BeautifulSoup(re.text, 'html.parser')

    temp = json.loads(re.text)
    temp = temp['payload']['tree']['items']

    img_list = []  # all of the images names in the LSP database

    for link in temp:
        img_list.append(link['name'])


    #下载所有
    # for i in img_list:pyinstaller-F setup.py
    # 
    #     url = f"https://raw.githubusercontent.com/SatinWuker/lsp/MASTER/lsp-db/{i}"
    #     print("访问 " + colored(url, 'green'))
    # 
    #     with open(f"imgs/{i}.png", 'wb') as img_f:
    #         lsp_content = requests.get(url).content
    #         img_f.write(base64.b64decode(lsp_content))


    # Randomly choose one image in the img_list
    name = random.choice(img_list)
    # Get the url of the chosen image
    url = f"https://raw.githubusercontent.com/lan2lang/lsp_pic/master/lsp-db/{name}"
    print("访问 " + colored(url, 'green'))

    # Download the image
    with open(f"{name}.png", 'wb') as img_f:
        lsp_content = requests.get(url).content
        img_f.write(base64.b64decode(lsp_content))

        return f"{name}.png"


def main():
    # app_logging()  # update the log file

    img_name = choose_img()

    print(f"显示图片 [{colored(img_name, 'red')}]")

    # Show image
    with Image.open(img_name) as image:
        image.show()
    os.remove(img_name)


if __name__ == "__main__":
    init()
    main()
