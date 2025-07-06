#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tasks
# @Time         : 2025/6/18 16:51
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI


# dynamic_router
# async def create_task(
#         request: dict,
#         api_key: Optional[str] = None
# ):
#     payload = request
#     client = AsyncOpenAI(base_url=base_url, api_key=api_key)
#     response = client.post(
#         ,
#         body=payload,
#         cast_to=dict,
#     )
#     return response
