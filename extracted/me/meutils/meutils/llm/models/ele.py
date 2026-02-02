#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ele
# @Time         : 2025/8/25 18:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *

"""
curl https://api.elevenlabs.io/v1/models \
     -H "xi-api-key: xi-api-key"
"""


async def get_models():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.elevenlabs.io/v1/models", headers={"xi-api-key": api_key})
        response.raise_for_status()
        data = response.json()
        return [m.get("model_id") for m in data]


if __name__ == '__main__':
    models = arun(get_models())

    print(','.join([f"elevenlabs/{m}" for m in models]))


# deepseek-ai/DeepSeek-V3.1