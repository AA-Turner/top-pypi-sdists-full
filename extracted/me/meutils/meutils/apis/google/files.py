#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : files
# @Time         : 2025/4/2 10:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 一般大文件问答需要
# https://ai.google.dev/gemini-api/docs/document-processing?hl=zh-cn&lang=python

from meutils.pipe import *

file = "/Users/betterme/PycharmProjects/AI/QR.png"
#
# file_object = client.files.upload(file=file)
# prompt = "一句话总结"

# file_object = client.aio.files.upload(file=file)


async def upload(self, files: Union[str, List[str]], client: Optional[genai.Client] = None):  # => openai files
    client = client or await self.get_client()

    if isinstance(files, list):
        return await asyncio.gather(*map(self.upload, files))

    file_config = {"name": f"{shortuuid.random().lower()}", "mime_type": guess_mime_type(files)}
    return await client.aio.files.upload(file=io.BytesIO(await to_bytes(files)), config=file_config)
