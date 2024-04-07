# -*- coding: utf-8 -*-
# @Time    : 2024/4/3 10:40
# @Author  : Wing
# @Site    : 
# @File    : wallpaper.py
# @Software: PyCharm
import os
import pathlib
import ctypes
import random
import requests

from bs4 import BeautifulSoup

# 设置存储图片的路径
lib_path = pathlib.Path(__file__).parent.absolute().joinpath("img_cache")
# 设置文件夹存储图片的最大数量
img_max_num = 2000


def load_paper_by_wallhaven():
    # https://unsplash.com/
    # https://wallhaven.cc/
    # https://stocksnap.com/
    # https://www.gamewallpapers.com/

    # 随机类别参数，风格设置
    qs = ["cat", "nature", "mountains", "women", "model", "snow", "sweater", "panorama"]
    q = random.choice(qs)
    # 类别参数随机选择
    sort_categories = ["Relevance", "Random", "Date Added", "Views", "Favorites", "Hot"]
    sorting = random.choice(sort_categories)

    # 模拟浏览器请求
    url = f"https://wallhaven.cc/search?q={q}&categories=111&purity=110&sorting={sorting}&order=desc&ai_art_filter=0"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)

    # 解析图片url
    bs_html = BeautifulSoup(response.text, 'lxml')
    soup_list = bs_html.find_all("a", class_="preview")
    sp = random.choice(soup_list)
    img_url = sp['href']
    img_name = img_url.split("/")[-1]
    exist_flag = is_exist_img(img_name)
    if exist_flag:
        return None, exist_flag
    else:
        # 下载图片数据
        req_html = requests.get(img_url)
        img_soup = BeautifulSoup(req_html.text, 'lxml')
        img_src = img_soup.find('img', id='wallpaper')['src']
        img_bytes = requests.get(img_src).content
        return img_bytes, img_src.split('/')[-1]


def is_exist_img(file_name):
    if not lib_path.exists():
        return False
    dirs = lib_path.glob('*')
    for file in dirs:
        if file_name in file.name:
            return file.name
    return False


def save_img(img_bytes, file_name):
    img_path = lib_path.joinpath(file_name)
    if img_bytes:
        # 保存图片
        if not lib_path.exists():
            lib_path.mkdir()
        dirs = sorted(lib_path.glob('*'), key=lambda file: os.path.getctime(file))
        if len(dirs) > img_max_num:
            pathlib.Path(dirs[0]).unlink()
        
        with open(img_path, 'wb') as f:
            f.write(img_bytes)
        return str(img_path.absolute())
    else:
        return str(img_path.absolute())

def set_paper():
    print("\n下载壁纸 ...")
    img_bytes, img_name = load_paper_by_wallhaven()
    print("\n保存壁纸 ...")
    abs_image_path = save_img(img_bytes, img_name)
    # 设置桌面壁纸
    print("\n设置壁纸 ...")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_image_path, 3)


if __name__ == '__main__':
    set_paper()
