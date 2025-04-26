#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : watermark_remove
# @Time         : 2025/3/23 11:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import requests
import json


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


class CommonOcr(object):
    def __init__(self, img_path=None, is_url=False):
        # 图像水印去除
        self._url = 'https://api.textin.com/ai/service/v1/image/watermark_remove'
        # 请登录后前往 “工作台-账号设置-开发者信息” 查看 x-ti-app-id
        # 示例代码中 x-ti-app-id 非真实数据
        self._app_id = 'c81f*************************e9ff'
        # 请登录后前往 “工作台-账号设置-开发者信息” 查看 x-ti-secret-code
        # 示例代码中 x-ti-secret-code 非真实数据
        self._secret_code = '5508***********************1c17'
        self._img_path = img_path
        self._is_url = is_url

    def recognize(self):
        head = {}
        try:
            head['x-ti-app-id'] = self._app_id
            head['x-ti-secret-code'] = self._secret_code
            if self._is_url:
                head['Content-Type'] = 'text/plain'
                body = self._img_path
            else:
                image = get_file_content(self._img_path)
                head['Content-Type'] = 'application/octet-stream'
                body = image
            result = requests.post(self._url, data=body, headers=head)
            return result.text
        except Exception as e:
            return e


if __name__ == "__main__":
    # 示例 1：传输文件
    response = CommonOcr(img_path=r'example.jpg')
    print(response.recognize())
    # 示例 2：传输 URL
    response = CommonOcr(img_path='http://example.com/example.jpg', is_url=True)
    print(response.recognize())
