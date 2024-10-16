import os


def download(content, name):
    f_name = ''

    # 使用 os.path.basename() 获取文件名
    file_name = os.path.basename(name)

    # 使用 os.path.splitext() 获取文件名和后缀
    file_name=file_name[:-4]


    os.makedirs(f'../lsp-db2/{dir_name}', exist_ok=True)

    with open(f"../lsp-db2/{dir_name}/{file_name}", "wb") as lsp_file:
        lsp_file.write(content)


def before_down(name):
    '''
    去除文件后缀保存
    :param name:
    :return:
    '''

    with open(f"{name}", "rb") as image_file:
        download(image_file.read(), name)


dir_name = 'cosersets'

dir = ''

# 遍历指定目录
g = os.walk(dir)

for path, dir_list, file_list in g:
    for file_name in file_list:
        before_down(os.path.join(path, file_name))
