#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/1/15 15:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.apis.fal.images import check

from meutils.schemas.task_types import TaskResponse
from meutils.schemas.video_types import VideoRequest

from meutils.schemas.fal_types import FEISHU_URL
from meutils.config_utils.lark_utils import get_next_token_for_polling

from fal_client import AsyncClient


# 平台/模型/版本
models_mapping ={
    "kling-video/v2/master/image-to-video": "latentsync",
    "kling-video/v2/master/text-to-video": "latentsync",
    "kling-video/lipsync/audio-to-video": "latentsync", # todo
    "kling-video/lipsync/text-to-video": "latentsync",
}

async def create_task(request: VideoRequest, token: Optional[str] = None):
    """https://fal.ai/models/fal-ai/latentsync/api#queue-submit

    """
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True, check_token=check)
    logger.debug(request)

    application = f"fal-ai/{request.model.removeprefix('fal-ai/')}"

    client = AsyncClient(key=token)
    response = await client.submit(
        application=application,
        arguments=request.model_dump(exclude_none=True, exclude={"model"})
    )
    # AsyncRequestHandle(request_id='0b7ab6b8-c7dc-4f17-a655-4ee56dd0f864')

    return TaskResponse(task_id=f"{request.model}::{response.request_id}", system_fingerprint=token)


@alru_cache(ttl=5)
async def get_task(task_id: str, token: Optional[str] = None):
    model, request_id = task_id.rsplit('::', 1)
    application = f"fal-ai/{model.removeprefix('fal-ai/')}"

    client = AsyncClient(key=token)
    response = await client.status(application, request_id, with_logs=True)

    logger.debug(response.__class__.__name__)  # Queued, InProgress, COMPLETED

    if metrics := response.__dict__.get("metrics"):  # {'inference_time': 17.29231595993042}
        response = await client.result(application, request_id)

    return response


if __name__ == '__main__':
    model = "latentsync"
    # model = "sync-lipsync"


    model = "fal-ai/kling-video/v2/master/image-to-video"
    model = "fal-ai/kling-video/v1/standard/text-to-video"

    request = VideoRequest(
        model=model,
        prompt="A cute cat",
    )


    r = arun(create_task(request))


    # r = arun(get_task(task_id, token))

    arun(get_task(r.task_id, r.system_fingerprint))