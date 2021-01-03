#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
from flask import Flask, render_template
import yaml.scanner

try:
    cf = open('./config.yaml', 'r', encoding='UTF-8')
    cs = cf.read()
    cf.close()
    conf = yaml.safe_load(cs)
except FileNotFoundError:
    print('未发现配置文件 config.yaml')
    exit()
except yaml.scanner.ScannerError:
    print('配置文件 config.yaml 格式错误，无法识别')
    exit()

app = Flask(
    __name__,
    template_folder=conf['DOWNLOAD'],
    static_folder=conf['DOWNLOAD'],
    static_url_path="",
)


@app.route('/')
def index():
    return render_template('links.html')


if __name__ == '__main__':
    app.run(debug=(conf['DEBUG'] == 1), host=conf['HOST'], port=conf['PORT'])
