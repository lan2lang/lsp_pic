import base64
import os

import requests
import random

from PIL import Image


def upload_pic():
    """
    上传图片
    :return:
    """
    # 读取文件内容并进行 base64 编码
    # with open(FILE_PATH, 'rb') as file:
    #     content = file.read()
    #     encoded_content = base64.b64encode(content).decode('utf-8')

    filename = '4'
    # 保存地址
    UPLOAD_PATH = 'lsp-db2/' + filename

    content = requests.get(
        'https://www.cosersets.com/directlink/1/Money%E5%86%B7%E5%86%B7/%E9%BB%91%E5%91%86%E5%A5%B3%E4%BB%86/05.webp').content
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
        'content': content,
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
    url = (random.choice(files)['html_url']).replace('blob', 'raw')
    print(url)
    with open(f"{url.split('/')[-1]}.webp", 'wb') as img_f:
        lsp_content = requests.get(url).content
        img_f.write(lsp_content)

    with Image.open(f"{url.split('/')[-1]}.webp") as image:
        image.show()
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
        # for file in files:
        # print(f"Name: {file['name']}, Type: {file['type']}, URL: {file['html_url']}")
        return files
    else:
        print(f"Failed to retrieve files: {response.status_code}")


if __name__ == "__main__":
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"

    # GitHub 个人访问令牌
    GITHUB_TOKEN = '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'

    # GitHub 用户名
    GITHUB_USERNAME = 'lan2lang'

    # 存储库名称
    REPO_NAME = 'lsp_pic'

    # 图库地址（github）
    pic_repository = 'https://github.com/lan2lang/lsp_pic/tree/main/lsp-db2'

    # get_one_pic()
    # https://github.com/lan2lang/lsp_pic/raw/main/lsp-db2/1.webp
    upload_pic()
    get_pic_list()
    #
