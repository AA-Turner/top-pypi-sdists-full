#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : rag
# @Time         : 2024/11/21 16:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

file_object = client.files.create(file=Path("百炼系列手机产品介绍.docx"), purpose="file-extract")
print(file_object.id) # file-fe-fUEnuSjIEbuMnKWpWSPKWGVe

# print(client.files.retrieve_content("file-fe-fUEnuSjIEbuMnKWpWSPKWGVe"))
#
# completion = client.chat.completions.create(
#     model="qwen-turbo-2024-11-01",
#     messages=[
#         {'role': 'system', 'content': 'You are a helpful assistant.'},
#         {'role': 'system', 'content': f'fileid://{file_object.id}'},
#         {'role': 'user', 'content': '这篇文章讲了什么？'}
#     ],
#     stream=True,
#     stream_options={"include_usage": True}
# )
#
# for chunk in completion:
#     print(chunk.model_dump())


print(client.files.content(file_id=file_object.id).text)