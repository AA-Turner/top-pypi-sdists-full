#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : raw
# @Time         : 2024/11/20 16:16
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from meutils.pipe import *
from meutils.schemas.replicate_types import FEISHU_URL, ReplicateRequest, ReplicateResponse
from meutils.config_utils.lark_utils import get_next_token_for_polling

from replicate import Client


@alru_cache(ttl=3600)
async def get_version(model="black-forest-labs/flux-schnell", token: Optional[str] = None):
    replicate = Client(api_token=token)

    model = await replicate.models.async_get(model)
    version = model.latest_version.id
    return version


async def create_task(request: ReplicateRequest):
    token = await get_next_token_for_polling(FEISHU_URL)
    replicate = Client(api_token=token)

    version = await get_version(request.ref, token)
    prediction = await replicate.predictions.async_create(
        version=version,
        input=request.input  # {"prompt": "Watercolor painting of an underwater submarine"})
    )
    return ReplicateResponse(**prediction.dict(), system_fingerprint=token)


async def get_task(task_id, token: Optional[str]=None):
    replicate = Client(api_token=token)

    prediction = await replicate.predictions.async_get(task_id)

    return ReplicateResponse(**prediction.dict())


if __name__ == '__main__':
    request = ReplicateRequest(input={"prompt": "a cat"})
    # task = arun(create_task(request))

    # arun(get_task(task.id))

    arun(get_task("77e6rwn5v5rmc0ck964acn75dc"))

