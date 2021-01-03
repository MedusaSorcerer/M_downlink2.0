#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import os
import shutil
import sys
import time

import pyautogui
import pyperclip
import yaml.scanner
from bs4 import BeautifulSoup
from pynput.keyboard import Listener
from selenium import webdriver

try:
    cf = open('./config.yaml', 'r', encoding='UTF-8')
    cs = cf.read()
    cf.close()
    conf = yaml.safe_load(cs)
except FileNotFoundError:
    print('未发现配置文件 config.yaml')
    sys.exit()
except yaml.scanner.ScannerError:
    print('配置文件 config.yaml 格式错误，无法识别')
    sys.exit()
pyautogui.FAILSAFE = True
Driver = None
ScrollMove = None
ScrollMax = conf['SCROLL_MAX']
Download = conf['DOWNLOAD']
Number = conf['NUMBER']
Shroud = conf['SHROUD']
Shift = conf['SHIFT']
LinkFile = conf['LINK_FILE']
SleepSeconds = conf['SLEEP_SECONDS']
SleepMethod = conf['SLEEP_METHOD']


def format_h5(path):
    if os.path.isfile(path):
        index_path = os.path.join(os.path.dirname(path), 'm_index.html')
        if Shroud == 1 or not os.path.isfile(index_path):
            hf = open(path, 'r', encoding='UTF-8')
            html = BeautifulSoup(hf.read(), 'html.parser')
            hf.close()
            for img in html.find_all('img'):
                if img.get('crossOrigin'): del img['crossOrigin']
                if img.get('crossorigin'): del img['crossorigin']
            for js in html.find_all('link') + html.find_all('script'):
                if js.get('href', '').endswith('.js.下载') or js.get('src', '').endswith('.js.下载'):
                    js.extract()
            for head in html.find_all('head'):
                new_tag = html.new_tag("style")
                new_tag.append("* {visibility: inherit !important;}")
                head.insert_after(new_tag)
            index = open(index_path, 'w', encoding='UTF-8')
            index.write(str(html))
            index.close()


def _get_path():
    paths = []
    for root, dirs, files in os.walk(Download):
        for i in dirs:
            for _root, _dirs, _files in os.walk(os.path.join(root, i)):
                if _files:
                    try:
                        _files.remove('m_index.html')
                    except ValueError:
                        ...
                    paths.append([i, os.path.join(root, i, _files[0])])
                break
        break
    return paths


def write():
    paths = _get_path()
    a = ''
    for i in paths:
        format_h5(i[1])
        title = i[1][:-5]
        a += fr"""<div class="link"><a href="{i[0]}/m_index.html" target="_blank" onmousemove="goin(this)" onmouseout="gout()">{i[0]} {title}</a></div>"""
        a += '\n'
    with open(os.path.join(Download, 'links.html'), 'w', encoding='UTF-8') as f:
        f.write(_header() + a + _finish())
        f.close()


def _press(key):
    try:
        if key.char == '1':
            listener.stop()
    except AttributeError:
        ...


def download():
    global Driver, Number, ScrollMove, listener
    Driver = webdriver.Chrome('chromedriver.exe', options=ops)
    Driver.maximize_window()
    for i in links:
        i = i.replace('\n', '').replace('\r', '')
        if not i: continue
        Driver.get(i)
        time.sleep(1)
        _scroll_height_1 = Driver.execute_script('return document.documentElement.clientHeight;')
        _scroll_height_2 = 0
        if ScrollMove is None: ScrollMove = _scroll_height_1
        for _ in range(ScrollMax):
            Driver.execute_script(f"window.scrollBy (0,{ScrollMove});")
            _scroll_height_3 = Driver.execute_script('return document.documentElement.scrollTop || document.body.scrollTop;')
            time.sleep(2)
            if _scroll_height_3 == _scroll_height_2: break
            _scroll_height_2 = _scroll_height_3
        else:
            with Listener(on_press=_press) as listener:
                listener.join()
        time.sleep(1)
        Driver.execute_script('var q=document.documentElement.scrollTop=10')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 's')
        time.sleep(.5)
        new_path = os.path.join(Download, str(Number).zfill(4))
        if os.path.isdir(new_path): shutil.rmtree(new_path, ignore_errors=True)
        os.mkdir(new_path)
        time.sleep(1)
        pyperclip.copy(Download)
        pyautogui.typewrite([*(['shiftleft'] if Shift else []), 'home'])
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(.1)
        pyautogui.typewrite(['\\', *(i for i in str(Number).zfill(4)), '\\'])
        Number += 1
        time.sleep(1)
        pyautogui.typewrite(['enter'])
        if SleepMethod == 'auto':
            time.sleep(SleepSeconds)
        elif SleepMethod == 'manual':
            with Listener(on_press=_press) as listener:
                listener.join()


def _header():
    return r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Links</title>
    <script>
        function goin(x) {
            let ts = document.getElementById("ts")
            ts.innerHTML = x.innerText;
            ts.style.backgroundColor = "rgba(167,167,167,.9)"
        }

        function gout() {
            let ts = document.getElementById("ts")
            ts.style.backgroundColor = "rgba(0,0,0,0)"
            ts.innerHTML = "";
        }
    </script>
    <style>
        body {
            background: url("https://i.ibb.co/XZ9zt3p/593918ed85e56.png");
            background-size: cover;
        }

        body > div {
            width: 40%;
            background: #e5e5e5;
            margin: 5px 30% 0 30%;
            border-radius: 20px;
            background: -ms-linear-gradient(top, #cacaca, #a2b2ff);
            background: -moz-linear-gradient(top, #cacaca, #a2b2ff);
            background: -webkit-gradient(linear, 0% 0%, 0% 100%, from(#cacaca), to(#a2b2ff));
            background: -webkit-gradient(linear, 0% 0%, 0% 100%, from(#cacaca), to(#a2b2ff));
            background: -webkit-linear-gradient(top, #cacaca, #a2b2ff);
            background: -o-linear-gradient(top, #cacaca, #a2b2ff);
        }

        h1 {
            margin-top: 80px;
        }

        .link {
            padding: 2px 0 2px 10px;
        }

        .link:nth-child(1) {
            padding: 20px 0 2px 10px;
        }

        .link:nth-last-child(1) {
            padding: 2px 0 20px 10px;
        }

        a {
            font-size: 16px;
            display: block;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        a:link {
            color: #005400;
            text-decoration: none;
        }

        a:active {
            color: #005400;
            text-decoration: none;
        }

        a:visited {
            color: #005400;
            text-decoration: none;
        }

        a:hover {
            color: white;
            text-decoration: none;
        }

        #ts {
            height: 40px;
            z-index: 9999;
            position: fixed ! important;
            right: 0;
            top: 0;
            width: 100%;
            margin: 0;
            text-align: center;
            padding-top: 16px;
            font-size: 18px;
            letter-spacing: 2px;
        }

        ::-webkit-scrollbar {
            width: 10px;
            height: 1px;
        }

        ::-webkit-scrollbar-thumb {
            border-radius: 10px;
            background-color: #00b1ff;
            background-image: -webkit-linear-gradient(
                    45deg,
                    rgba(255, 255, 255, 0.5) 25%,
                    transparent 25%,
                    transparent 50%,
                    rgba(255, 255, 255, 0.5) 50%,
                    rgba(255, 255, 255, 0.5) 75%,
                    transparent 75%,
                    transparent
            );
        }

        ::-webkit-scrollbar-track {
            box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
            background: #ededed;
            border-radius: 10px;
        }
    </style>
</head>
<body>
<h1 align="center">保存的链接地址目录</h1>
<div>

    """


def _finish():
    return r"""
</div>
<p id="ts">
</p>
<br>
<br>
<br>
<br>
<br>
</body>
</html>    
    """


if __name__ == '__main__':
    _ = """
    help:
        Downlink2.0 版本实现下载指定的路由地址的 H5 界面至本地，
        并区分下载/解析/写入三个模块：
            下载：将路由界面下载至本地指定的文件夹内
            解析：解析主界面至 m_index.html 来正常显示其中内容，并通过 SHROUD 参数来声明是否对已解析的文件重新解析
            写入：已经携带了解析功能，将本地文件路由写入 links.html 文件
    
        options:
            -h [--help] 获取帮助信息
            -t [--test] 测试组件运行是否正常
            -d [--download] 下载 LINK_FILE 中的链接保存到 DOWNLOAD 目录下
            -w [--write] 将 DOWNLOAD 目录下的文件生成文件静态目录文件 links.html
            -a [--analysis] 格式化解析下载的 H5 界面
    """
    ops = webdriver.ChromeOptions()
    ops.add_argument('--ignore-certificate-errors')
    argv = sys.argv[1:]
    if not argv:
        download()
        write()
        sys.exit()
    if '-help' in argv or '--help' in argv:
        print(_)
        sys.exit()
    if not os.path.isdir(Download):
        if input(f'没有发现配置的 {Download} 文件夹路径，是否自动创建？ [Y/y]创建 or [other]退出：').upper() == 'Y':
            os.makedirs(Download)
            if not os.path.isdir(Download):
                print(f'创建未成功，请使用手动创建文件夹 {Download}')
                sys.exit()
        else:
            sys.exit()
    if not os.path.isfile(LinkFile):
        print(f'未发现路由地址文件：{LinkFile}')
        sys.exit()
    with open(LinkFile, 'r', encoding='UTF-8') as lf:
        links = lf.readlines()
        lf.close()
    if '-t' in argv or '--test' in argv:
        t_driver = webdriver.Chrome('chromedriver.exe', options=ops)
        t_driver.maximize_window()
        t_driver.get('https://www.baidu.com')
        time.sleep(2)
        t_driver.close()
        sys.exit()
    if '-d' in argv or '--download' in argv:
        download()
        Driver.get(f'file:///{os.path.abspath("point.html")}')
        with Listener(on_press=_press) as listener:
            listener.join()
        Driver.close()
    if '-w' in argv or '--write' in argv:
        write()
    elif '-a' in argv or '--analysis' in argv:
        [format_h5(i[1]) for i in _get_path()]
    sys.exit()
