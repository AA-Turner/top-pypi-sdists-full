#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2024/9/25 15:27
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
# from minio import Minio
from meutils.oss.minio_oss import Minio
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

file = client.files.create(
    file=open("/Users/betterme/PycharmProjects/AI/docker-compose.yml", "rb"),
    purpose='file-extract'
)
client.files.content(file.id)

if __name__ == '__main__':
    print(file)