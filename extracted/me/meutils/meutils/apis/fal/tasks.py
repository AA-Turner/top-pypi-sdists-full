#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/1/15 15:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : fal-ai/xx 动态路由

from meutils.pipe import *
from meutils.db.redis_db import redis_aclient

from meutils.apis.fal.images import check

from meutils.schemas.task_types import TaskResponse
from meutils.schemas.video_types import VideoRequest

from meutils.schemas.fal_types import FEISHU_URL
from meutils.config_utils.lark_utils import get_next_token_for_polling

from fal_client import AsyncClient
from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request, HTTPException, status, BackgroundTasks

# 平台/模型/版本
models_mapping = {
    "kling-video/v2/master/image-to-video": "latentsync",
    "kling-video/v2/master/text-to-video": "latentsync",
    "kling-video/lipsync/audio-to-video": "latentsync",  # todo
    "kling-video/lipsync/text-to-video": "latentsync",
}


async def create_task(model:str, request: dict, token: Optional[str] = None):
    """https://fal.ai/models/fal-ai/latentsync/api#queue-submit

    """
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True, check_token=check)
    logger.debug(request)

    application = f"fal-ai/{model.removeprefix('fal-ai/')}"  # fal-ai/flux-pro/kontext

    client = AsyncClient(key=token)
    response = await client.submit(
        application=application,
        arguments=request
    )
    request_id = response.request_id
    await redis_aclient.set(request_id, token, ex=7 * 24 * 3600)
    """
    {'cancel_url': 'https://queue.fal.run/fal-ai/flux-1/requests/db9b7555-efa8-495b-9be2-e6243e6406e6/cancel',
 'client': <httpx.AsyncClient object at 0x28d607fa0>,
 'request_id': 'db9b7555-efa8-495b-9be2-e6243e6406e6',
 'response_url': 'https://queue.fal.run/fal-ai/flux-1/requests/db9b7555-efa8-495b-9be2-e6243e6406e6',
 'status_url': 'https://queue.fal.run/fal-ai/flux-1/requests/db9b7555-efa8-495b-9be2-e6243e6406e6/status'}
 
 # AsyncRequestHandle(request_id='548a8736-eb56-492f-a788-c67432821919')

    """

    return {"request_id": request_id}


@alru_cache(ttl=5)
async def get_task(model:str, request_id: str):
    token = await redis_aclient.get(request_id)  # 绑定对应的 token
    token = token and token.decode()
    if not token:
        raise HTTPException(status_code=404, detail="TaskID not found")


    application = f"fal-ai/{model.removeprefix('fal-ai/')}"

    client = AsyncClient(key=token)
    response = await client.status(application, request_id, with_logs=True)

    logger.debug(response.__class__.__name__)  # Queued, InProgress, COMPLETED

    if metrics := response.__dict__.get("metrics"):  # {'inference_time': 17.29231595993042}
        response = await client.result(application, request_id)


    return response


if __name__ == '__main__':
    token = "cda184dc-4c6a-4776-be39-79bfd7771328:8c3f25093040ebd10afb93df6921e537"

    model = "fal-ai/flux-1/schnell"
    request = {
        "prompt": "Extreme close-up of a single tiger eye, direct frontal view. Detailed iris and pupil. Sharp focus on eye texture and color. Natural lighting to capture authentic eye shine and depth. The word \"FLUX\" is painted over it in big, white brush strokes with visible texture."
    }

    # r = arun(create_task(model, request, token))

    request_id = "548a8736-eb56-492f-a788-c67432821919"

    r = arun(get_task(model, request_id))
