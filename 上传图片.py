import os

import requests
import base64

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# GitHub 个人访问令牌
GITHUB_TOKEN = ''

# GitHub 用户名
GITHUB_USERNAME = 'lan2lang'

# 存储库名称
REPO_NAME = 'lsp_pic'

# 文件路径
FILE_PATH = 'G:\lsp_pic\src\imgs\Kitaro_绮太郎_FGO 清少纳言__DSC9245.webp'

# 上传到 GitHub 存储库中的路径
UPLOAD_PATH = 'path/in/repository/Kitaro_绮太郎_FGO 清少纳言__DSC9245.webp'

# 读取文件内容并进行 base64 编码
with open(FILE_PATH, 'rb') as file:
    content = file.read()
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
