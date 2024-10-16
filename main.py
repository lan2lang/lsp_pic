import base64
import os
import random
import uuid

import requests
from PIL import Image


def upload_pic():
    """
    上传网络上的图片到GitHub仓库
    :return:
    """

    filename = str(uuid.uuid4())
    # 保存地址
    UPLOAD_PATH = 'lsp-db2/' + filename

    # 下载图片
    response = requests.get('https://th.wallhaven.cc/lg/yx/yxd8jk.jpg')
    if response.status_code != 200:
        print('Failed to download image.')
        return
    content = response.content

    upload(UPLOAD_PATH, content)


def upload_local_pic(local_image_path):
    """
    上传本地图片到GitHub仓库
    :param local_image_path: 本地图片的路径
    :return:
    """

    # 获取图片文件名
    filename = str(uuid.uuid4())  # 使用UUID生成唯一的文件名

    # 上传地址
    UPLOAD_PATH = f'lsp-db2/{filename}'

    # 读取本地图片
    with open(local_image_path, 'rb') as img_file:
        content = img_file.read()

    upload(UPLOAD_PATH, content)


def upload(UPLOAD_PATH, content):
    # 编码为base64
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
        print(f'File uploaded successfully: {response.json()["content"]["html_url"]}')
    else:
        print('Failed to upload file.')
        print('Response:', response.json())


def get_one_pic():
    """
    随机获取一张图片并展示
    :return:
    """
    try:
        files = get_pic_list()
        if not files:
            print('No files found.')
            return

        # 随机选择一张图片
        url = (random.choice(files)['html_url']).replace('blob', 'raw')
        local_filename = f"{url.split('/')[-1]}"

        headers = {
            'Authorization': f'token {GITHUB_TOKEN}'
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print('Failed to download image.')
            return

        # 保存图片到本地
        with open(local_filename, 'wb') as img_f:
            img_f.write(response.content)

        # 显示图片
        try:
            with Image.open(local_filename) as image:
                image.show()
        except IOError:
            print('Failed to open image.')

        # 删除本地图片
        os.remove(local_filename)
    except Exception as e:
        print(f"Error in retrieving or displaying the image: {e}")


def get_pic_list():
    """
    获取图片列表
    :return: 文件列表或空列表
    """
    try:
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
            return []
    except Exception as e:
        print(f"Error retrieving the file list: {e}")
        return []


if __name__ == "__main__":
    # 设置代理，如果不需要代理，可以注释掉这部分
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"

    with open('token.txt', 'r', encoding='utf-8') as f:
        GITHUB_TOKEN = f.readline().strip()

    # GitHub 用户名
    GITHUB_USERNAME = 'lan2lang'

    # GitHub 仓库名称
    REPO_NAME = 'lsp_pic'

    # 图库地址
    pic_repository = f'https://github.com/{GITHUB_USERNAME}/{REPO_NAME}/tree/main/lsp-db2'

    # 上传图片
    # upload_pic()

    upload_local_pic("C:\\Users\\Administrator\Pictures\其他\wallhaven-e7jj6r.jpg")
    # 获取随机图片并展示
    get_one_pic()
