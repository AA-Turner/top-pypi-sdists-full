#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : google2openai
# @Time         : 2025/4/1 13:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 
"""
1. 生图 编辑图 多轮
2. 文件上传、大文件问答

注意 ：借助 File API，您最多可为每个项目存储 20 GB 的文件，每个文件的大小上限为 2 GB。文件会存储 48 小时。您可以在该时间段内使用 API 密钥访问这些数据，但无法从 API 下载这些数据。在已推出 Gemini API 的所有地区，此功能均可免费使用。

"""
from meutils.pipe import *
from meutils.schemas.openai_types import CompletionRequest

from google import genai
from google.genai.types import HttpOptions, GenerateContentConfig, Content, HarmCategory, HarmBlockThreshold, Part

# Content(role="user", parts=[Part.from_text(text=prompt)]),
# Content(role="model", parts=[Part.from_text(text="Ok")]),

config = GenerateContentConfig(

    temperature=0.7,
    top_p=0.8,
    # response_modalities=['Text', 'Image'],

    # 公民诚信类别的默认屏蔽阈值为 Block none（对于别名为 gemini-2.0-flash、gemini-2.0-pro-exp-02-05 和 gemini-2.0-flash-lite 的 gemini-2.0-flash-001），适用于 Google AI Studio 和 Gemini API；仅适用于 Google AI Studio 中的所有其他模型的 Block most。
    # safety_settings=[
    #     SafetySetting(
    #         category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
    #         threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    #     ),
    # ]
)


# self._http_options.base_url = 'https://generativelanguage.googleapis.com/'
# self._http_options.api_version = 'v1beta'
client = genai.Client(
    api_key="AIzaSyAlpq4kR9ZP0NwaqQzqHtDKqiV8PLdUqnA",
    http_options=HttpOptions(
        base_url="https://all.chatfire.cc/genai"
    )
)

file = "/Users/betterme/PycharmProjects/AI/QR.png"
#
# file_object = client.files.upload(file=file)
# prompt = "一句话总结"

# file_object = client.aio.files.upload(file=file)
# https://generativelanguage.googleapis.com/v1beta/files/ickgffcfb9zl
#
# contents = ('Hi, can you create a 3d rendered image of a pig '
#             'with wings and a top hat flying over a happy '
#             'futuristic scifi city with lots of greenery?')
#
# prompt = "9.11 9.8哪个大呢"

uri='https://generativelanguage.googleapis.com/v1beta/files/88n7hk8tau7g'

# client.aio.chats.create(
#     model="gemini-2.0-flash-exp-image-generation",
# )

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        '解释下',
        Part.from_uri(file_uri=uri, mime_type='image/png')
    ],

    # model="gemini-2.5-pro-exp-03-25",
    # model="gemini-2.0-flash",

    # contents=[
    #     Part.from_uri(file_uri='https://generativelanguage.googleapis.com/v1beta/files/test', mime_type='image/png'),
    #
    #           "一句话总结"],
    config=config
)

# client.aio.
# client.aio.chats.create()

if __name__ == '__main__':
    # arun(file_object)
    pass
