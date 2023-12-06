import os
from sys import argv
from requests import get
import base64
import random
from string import ascii_lowercase

name = "D:\迅雷下载\电报\Twitter高质量合集-萝莉类Part01(0-50) [8547P+22.3GB]\[Twitter][萝莉] [Kit@kittyxkum]\P-Kit@kittyxkum (573).jpg"


def download(content):
    encoded_string = base64.b64encode(content)
    f_name = ''
    if 'http' in name:
        f_name = ''.join(random.choice(ascii_lowercase) for i in range(12))
    else:
        f_name = os.path.basename(name)
    with open(f"../lsp-db/{f_name}.lsplol", "wb") as lsp_file:
        lsp_file.write(bytearray(encoded_string))

if "http" in name:
    download(get(name).content)
else:
    with open(f"{name}", "rb") as image_file:
        download(image_file.read())
