#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_files.py
# @Time         : 2025/2/25 12:16
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from openai import OpenAI, AsyncOpenAI

client = AsyncOpenAI(
    base_url="https://all.chatfire.cn/qwen/v1",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjMxMGNiZGFmLTM3NTQtNDYxYy1hM2ZmLTllYzgwMDUzMjljOSIsImV4cCI6MTc0MzAzNTk4OH0.GVAoSFtK94a9CgxqHCEnxzAnRi7gafIvYyH9mIJUh4s"
)


async def upload():
    file_object = await client.files.create(
        file=Path("招标文件备案表（第二次）.pdf"),
        purpose="file-extract"
    )
    return file_object


if __name__ == '__main__':
    pass