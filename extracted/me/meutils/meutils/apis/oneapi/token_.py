#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : token
# @Time         : 2024/7/19 13:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *

import requests
import json

# check token: todo todo todo
url = "https://api.chatfire.cn/v1/dashboard/billing/subscription"

# 创建
url = "https://api.chatfire.cn/api/token/"

payload = json.dumps({
    "name": "xxx",
    "remain_quota": 500000,
    "expired_time": -1,
    "unlimited_quota": False,
    "model_limits_enabled": False,
    "model_limits": ""
})
headers = {
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

# 根据 key id 查询
import http.client

conn = http.client.HTTPSConnection("api.chatfire.cn")
payload = ''
conn.request("GET", "/api/token/1096", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

# 修改key信息

import requests
import json

url = "https://api.chatfire.cn/api/token/"

payload = json.dumps({
    "id": 1096,
    "user_id": 1,
    "key": "SNzQfo2enYpVqWV08f2e9023170245878d58F92bD820Af814",
    "status": 1,
    "name": "xxx",
    "created_time": 1721368510,
    "accessed_time": 1721368510,
    "expired_time": -1,
    "remain_quota": 5000001,
    "unlimited_quota": False,
    "model_limits_enabled": False,
    "model_limits": "",
    "used_quota": 0,
    "DeletedAt": None
})

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)

# 查key 余额与
import requests

url = "https://api.chatfire.cn/v1/dashboard/billing/usage" # ?start_date=2024-4-10&end_date=2024-7-19

payload = {}
headers = {
    'authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

# 查key 消费行为；可定位到 key id  user id
# https://api.chatfire.cn/api/log/token?key=sk-


# key信息
import requests

url = "https://api.chatfire.cn/v1/dashboard/billing/subscription"

payload = {}
headers = {
    'authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
    'priority': 'u=1, i',
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

# 查询用户下所有 key
# https://api.chatfire.cn/api/token/?p=0&size=1
# https://api.chatfire.cn/api/token/1096 # 根据超级管理员查询用户access token然后再查询key信息
