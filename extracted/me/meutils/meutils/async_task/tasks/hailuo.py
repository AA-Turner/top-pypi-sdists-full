#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : hailuo
# @Time         : 2024/12/6 09:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.async_utils import async_to_sync_pro
from meutils.async_task import worker, shared_task
from meutils.apis.hailuoai.videos import VideoRequest, create_task as remote_create_task, get_task


@shared_task(pydantic=True, retry_kwargs={'max_retries': 10, 'countdown': 10})
@async_to_sync_pro
async def create_task(request, **kwargs):
    if isinstance(request, dict):
        request = VideoRequest(**request)

    response = await remote_create_task(request)
    return response.model_dump()
