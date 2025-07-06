#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : minimax
# @Time         : 2025/4/1 12:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import requests
import json

url = "https://api.minimax.chat/v1/text2voice"
api_key = "请输入您的api key"

payload = json.dumps({
    "gender": "female",
    "age": "old",
    "voice_desc": [
        "Kind and friendly",
        "Kind and amiable",
        "Kind hearted",
        "Calm tone"
    ],
    "text": "真正的危险不是计算机开始像人一样思考，而是人开始像计算机一样思考"
})
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}',
}

response = requests.request("POST", url, headers=headers, data=payload)
