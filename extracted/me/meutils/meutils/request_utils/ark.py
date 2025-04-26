#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ark
# @Time         : 2024/12/31 13:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json
import os

from meutils.pipe import *
import volcenginesdkcore
from volcenginesdkcore.signv4 import SignerV4
import volcenginesdkark

# sign(path, method, headers, body, query, ak, sk, region, service)

headers = {}
payload = {
    "Prompt": "关于星空的歌",
    "Genre": "R&B/Soul",
    "Mood": "Dynamic/Energetic",
    "Gender": "Male",
    "ModelVersion": "v4.0"
}
params = {"Action": "GenLyrics", "Version": "2024-08-12"}
SignerV4.sign(
    path="/",
    method="POST",
    query=params,
    body=json.dumps(payload),
    headers=headers,
    ak=os.getenv("ARK_ACCESS_KEY"),
    sk=os.getenv("ARK_SECRET_ACCESS_KEY"),
    region="cn-beijing",
    service="imagination"
)

print(headers)

s = ''
for k, v in headers.items():
    s += f"{k}:{v}\n"

print(s)
