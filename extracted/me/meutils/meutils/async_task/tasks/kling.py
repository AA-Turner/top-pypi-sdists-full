#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kling
# @Time         : 2024/11/28 16:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 注册任务

from meutils.async_utils import async_to_sync_pro
from meutils.async_task import worker, shared_task

from meutils.apis.kling import kolors_virtual_try_on


@shared_task(pydantic=True, retry_kwargs={'max_retries': 5, 'countdown': 10})
@async_to_sync_pro
async def create_task(request: kolors_virtual_try_on.TryOnRequest, **kwargs):
    if isinstance(request, dict):
        request = kolors_virtual_try_on.TryOnRequest(**request)

    response = await kolors_virtual_try_on.create_task(request)
    return response.model_dump()


if __name__ == '__main__':
    pass
    # create_task.apply_async()
    create_task.apply_async(kwargs={"request": kolors_virtual_try_on.TryOnRequest().model_dump()})
