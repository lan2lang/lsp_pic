import os
from sys import argv
from requests import get
import base64
import random
from string import ascii_lowercase


def download(content, name):
    encoded_string = base64.b64encode(content)
    f_name = ''
    if 'http' in name:
        f_name = ''.join(random.choice(ascii_lowercase) for i in range(12))
    else:
        f_name = os.path.basename(name).split('.')[0]
    with open(f"../lsp-db/{f_name}.lsplol", "wb") as lsp_file:
        lsp_file.write(bytearray(encoded_string))


def before_down(name):
    if "http" in name:
        download(get(name).content, name)
    else:
        with open(f"{name}", "rb") as image_file:
            download(image_file.read(), name)


dir = "D:\迅雷下载\电报\Twitter高质量合集-萝莉类Part01(0-50) [8547P+22.3GB]\[Twitter][萝莉] [⁵⁵⁵小埋长不高ˡᵃ@Xiaomai522]"

# 遍历指定目录
g = os.walk(dir)

for path, dir_list, file_list in g:
    for file_name in file_list:
        before_down(os.path.join(path, file_name))
