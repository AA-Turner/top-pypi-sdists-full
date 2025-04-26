#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : replicateai
# @Time         : 2024/11/29 19:08
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.async_utils import async_to_sync_pro
from meutils.decorators.retry import retrying
from meutils.async_task import worker, shared_task

from meutils.apis.replicateai import raw as replicate


@shared_task(pydantic=True, retry_kwargs={'max_retries': 5, 'countdown': 10})
@async_to_sync_pro
async def create_task(request: replicate.ReplicateRequest, **kwargs):
    response = await replicate.create_task(request)
    return response
