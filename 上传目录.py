import os
import requests
import base64

# 设置代理（如果需要）
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# GitHub 个人访问令牌
GITHUB_TOKEN = ''

# GitHub 用户名
GITHUB_USERNAME = 'lan2lang'

# 存储库名称
REPO_NAME = 'lsp_pic'

# 本地目录路径
DIRECTORY_PATH = r'G:\爬虫\code\Demo\cosersets\download\Kitaro_绮太郎_2410'

def upload_files_to_github(directory_path, upload_path):
    """
    遍历目录下的所有文件，并上传到 GitHub 存储库中
    :param directory_path: 本地目录路径
    :param upload_path: 上传到 GitHub 存储库中的路径
    """
    # 获取目录下的所有文件
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            upload_file_to_github(file_path, upload_path)

def upload_file_to_github(file_path, upload_path):
    """
    上传单个文件到 GitHub 存储库中
    :param file_path: 本地文件路径
    :param upload_path: 上传到 GitHub 存储库中的路径
    """
    # 读取文件内容并进行 base64 编码
    with open(file_path, 'rb') as file:
        content = file.read()
        encoded_content = base64.b64encode(content).decode('utf-8')

    # 构建 GitHub API URL
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{upload_path}/{os.path.basename(file_path[:-5])}'

    # API 请求头
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Content-Type': 'application/json'
    }

    # 请求数据
    data = {
        'message': f'Add {os.path.basename(file_path)} via API',
        'content': encoded_content,
    }

    # 发起 PUT 请求上传文件
    response = requests.put(url, json=data, headers=headers)

    # 检查请求结果
    if response.status_code == 201:
        print(f'Successfully uploaded {file_path} to GitHub.')
    else:
        print(f'Failed to upload {file_path} to GitHub.')
        print('Response:', response.json())

if __name__ == "__main__":
    upload_files_to_github(DIRECTORY_PATH, 'lsp-db2')
