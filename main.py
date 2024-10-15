import base64
import os
import random
import uuid

import requests
from PIL import Image


def upload_pic():
    """
    上传图片
    :return:
    """

    filename = str(uuid.uuid4())

    # 保存地址
    UPLOAD_PATH = 'lsp-db2/' + filename

    content = requests.get(
        'https://th.wallhaven.cc/lg/yx/yxd8jk.jpg').content
    encoded_content = base64.b64encode(content).decode('utf-8')

    # GitHub API URL
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{UPLOAD_PATH}'

    # API 请求头
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Content-Type': 'application/json'
    }

    # 请求数据
    data = {
        'message': 'Add new file via API',
        'content': encoded_content,
    }

    # 发起 PUT 请求上传文件
    response = requests.put(url, json=data, headers=headers)

    # 检查请求结果
    if response.status_code == 201:
        print('File uploaded successfully.')
    else:
        print('Failed to upload file.')
        print('Response:', response.json())


def get_one_pic():
    """
    随机获取一张图片
    :return:
    """
    files = get_pic_list()
    if not files:
        print('No files found.')
        return

    url = (random.choice(files)['html_url']).replace('blob', 'raw')
    print(url)
    local_filename = f"{url.split('/')[-1]}"

    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print('Failed to download image.')
        return

    with open(local_filename, 'wb') as img_f:
        img_f.write(response.content)

    try:
        with Image.open(local_filename) as image:
            image.show()
    except IOError:
        print('Failed to open image.')

    os.remove(local_filename)


def get_pic_list():
    """
    获取图片列表
    :return:
    """
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/lsp-db2'

    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        files = response.json()
        return files
    else:
        print(f"Failed to retrieve files: {response.status_code}")


if __name__ == "__main__":
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"

    # GitHub 个人访问令牌
    GITHUB_TOKEN = ''

    with open('token.txt', 'r', encoding='utf-8') as f:
        GITHUB_TOKEN = f.readline().strip()

    # GitHub 用户名
    GITHUB_USERNAME = 'lan2lang'

    # 存储库名称
    REPO_NAME = 'lsp_pic'

    # 图库地址（github）
    pic_repository = 'https://github.com/lan2lang/lsp_pic/tree/main/lsp-db2'

    upload_pic()
    get_one_pic()
