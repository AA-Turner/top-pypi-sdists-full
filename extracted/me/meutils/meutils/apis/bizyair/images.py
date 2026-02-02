#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/12/3 15:12
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

# Python 示例代码
import requests
import json

url = "https://api.bizyair.cn/w/v1/webapp/task/openapi/create"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-"
}
data = {
      "web_app_id": 40046,
      "suppress_preview_output": False,
      "input_values": {
        "26:CLIPTextEncode.text": "3D高级感手办，ip形象，动物ip，潮酷版小黄鸭，高挑的个子，，潮酷类型的头身比例，表情冷酷，扁圆的可爱小黄鸭的脸部轮廓，酷帅的小黄鸭造型，身穿宽松嘻哈文化时装搭，潮酷，飒爽，干净背景",
        "19:EmptySD3LatentImage.width": 1024,
        "19:EmptySD3LatentImage.height": 1024,
        "22:KSampler.seed": 1079022223487044
      }
    }

response = requests.post(url, headers=headers, json=data)
result = response.json()
print("生成结果:", result)