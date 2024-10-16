import base64
import os
import random
import threading
import uuid
from tkinter import Tk, Button, Label, filedialog, messagebox, simpledialog

import requests
from PIL import Image, ImageTk


def upload_pic():
    """
    上传网络上的图片到GitHub仓库
    :return:
    """
    # 弹出对话框让用户输入图片URL
    image_url = simpledialog.askstring("Input", "请输入URL:")
    if not image_url:
        messagebox.showerror('Error', '未输入URL')
        return

    filename = str(uuid.uuid4())

    # 保存地址
    UPLOAD_PATH = 'lsp-db2/' + filename

    # 下载图片
    response = requests.get(image_url)

    if response.status_code != 200:
        print('Failed to download image.')
        return
    content = response.content

    show_loading()

    # 下载和上传图片的过程可以使用线程来避免界面冻结
    thread = threading.Thread(target=upload, args=(UPLOAD_PATH, content))
    thread.start()


def show_loading():
    """
    显示加载中提示
    """
    loading_label.config(text="加载中...请稍候")
    root.update_idletasks()  # 刷新界面，确保“加载中”即时显示


def hide_loading():
    """
    隐藏加载中提示
    """
    loading_label.config(text="")
    root.update_idletasks()  # 刷新界面，移除“加载中”提示


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

    # 显示“加载中”提示
    show_loading()

    # 下载和上传图片的过程可以使用线程来避免界面冻结
    thread = threading.Thread(target=upload, args=(UPLOAD_PATH, content))
    thread.start()


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
        hide_loading()
        print(f'File uploaded successfully: {response.json()["content"]["html_url"]}')
        messagebox.showinfo('Success', f'File uploaded successfully')

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

        # # 显示图片
        # try:
        #     with Image.open(local_filename) as image:
        #         image.show()
        # except IOError:
        #     print('Failed to open image.')

        show_image(local_filename)

        # 删除本地图片
        # os.remove(local_filename)
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


def show_image(image_path):
    """
    在 GUI 界面上展示图片
    """
    try:
        # print(image_path)
        img = Image.open(image_path)
        img.thumbnail((300, 300))  # 调整图片大小
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # 保存引用避免被垃圾回收
        image_label.bind("<Double-1>", lambda event: open_image_with_default_app(image_path))  # 绑定双击事件
    except Exception as e:
        messagebox.showerror('Error', f'Failed to open image: {e}')


def open_image_with_default_app(image_path):
    """
    将图片数据保存为临时文件，并使用系统默认的图片查看器打开
    """
    # temp_image_path = "temp_image.jpg"
    # with open(temp_image_path, 'wb') as temp_file:
    #     temp_file.write(image_data)

    image_path = os.path.abspath(image_path)
    # 使用系统默认的图片查看器打开
    try:
        with Image.open(image_path) as image:
            image.show()
    except IOError:
        print('Failed to open image.')
    os.remove(image_path)


def select_and_upload():
    """
    打开文件对话框，选择本地图片并上传
    """
    local_image_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
    )
    if local_image_path:
        upload_local_pic(local_image_path)


# 创建图形界面
root = Tk()
root.title("GitHub 图片上传工具")
root.geometry("400x400")

# 标签和按钮
Label(root, text="选择图片或上传网络图片").pack(pady=10)

Button(root, text="上传本地图片", command=select_and_upload).pack(pady=10)
Button(root, text="上传网络图片", command=upload_pic).pack(pady=10)
Button(root, text="展示随机图片", command=get_one_pic).pack(pady=10)

# 加载中的提示标签
loading_label = Label(root, text="", fg="red")
loading_label.pack(pady=10)

# 展示图片的标签
image_label = Label(root)
image_label.pack(pady=10)

# 运行主循环
if __name__ == "__main__":
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"
    # 从文件中读取GitHub token
    with open('token.txt', 'r', encoding='utf-8') as f:
        GITHUB_TOKEN = f.readline().strip()

    GITHUB_USERNAME = 'lan2lang'
    REPO_NAME = 'lsp_pic'

    # 启动GUI
    root.mainloop()
