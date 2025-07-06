#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : suno_api
# @Time         : 2025/2/25 14:16
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

# "https://api.chatfire.cn/suno/submit/music"

from openai import AsyncOpenAI
from meutils.schemas.suno_types import SunoAIRequest
from meutils.decorators.retry import retrying


@retrying()  # 触发重试
async def get_task(task_id):  # task_id 实际是 clip_ids， 必须指定token获取任务
    client = AsyncOpenAI(base_url="https://api.chatfire.cn/suno")
    response = await client.get(f"/fetch/{task_id}", cast_to=object)
    return response


async def create_task(request: SunoAIRequest):
    client = AsyncOpenAI(base_url="https://api.chatfire.cn/suno")

    response = await client.post(
        "/submit/music",
        body=request.model_dump(exclude_none=True),
        cast_to=object,

    )

    logger.debug(response)
    return response.get("data")


if __name__ == '__main__':
    pass
