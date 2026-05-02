#!/usr/bin/env python
#-*- coding:utf-8 -*-
import setuptools
long_description = '''
通过GA协议获取数据，用于调试GA控件树，示例：``ga-utils get 300 --port 2004``

##安装

``$ pip install ga-utils``

##使用

``ga-utils get CMD --port PORT``

##示例

- 获取控件树： ``ga-utils get 300 --port 2004``
- 获取控件的位置信息：``ga-utils get 103 --port 2004``

##说明

port为GA服务的本地端口号，可用adb forward命令到本地。示例：``adb forward tcp:2004 tcp:27019``。

请求的日志会存在当前目录的ga-utils.yyyy-MM-DD.log。
'''
setuptools.setup(
    name="ga-utils",                 
    version="1.0.6",                               
    author="janeluck",  
    license='MIT',
    author_email="janeluck158@outlook.com",
    url="https://git.woa.com/janeajian/ga-util",
    description="通过GA协议获取数据，用于调试GA控件树",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    install_requires=[
    'xmltodict>=0.13.0'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    entry_points = {
        'console_scripts': [
            'ga-utils=ga_utils.main:main',
        ]
    }
)