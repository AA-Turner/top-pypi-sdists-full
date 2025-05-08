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

from meutils.schemas.task_types import TaskResponse
from meutils.schemas.video_types import FalVideoRequest

from meutils.schemas.fal_types import FEISHU_URL
from meutils.config_utils.lark_utils import get_next_token_for_polling

from fal_client import AsyncClient


# 平台/模型/版本
def model_mapper(model: str):
    return f"fal-ai/{model.removeprefix('fal-ai/')}"


async def create_task(request: FalVideoRequest, token: Optional[str] = None):
    """https://fal.ai/models/fal-ai/latentsync/api#queue-submit

    todo: 判别任务
    """
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL)
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
    application = f"fal-ai/{model}"

    client = AsyncClient(key=token)
    response = await client.status(application, request_id, with_logs=True)

    logger.debug(response.__class__.__name__)  # Queued, InProgress, COMPLETED

    if metrics := response.__dict__.get("metrics"):  # {'inference_time': 17.29231595993042}
        response = await client.result(application, request_id)

    return response


if __name__ == '__main__':
    model = "latentsync"
    # model = "sync-lipsync"
    audio_url = "https://oss.ffire.cc/files/lipsync.mp3"
    video_url = "https://oss.ffire.cc/files/lipsync.mp4"

    audio_url = "https://oss-shanghai.sanwubeixin.cn/cache/file/20250218/173988875057269.mp3"
    video_url = "https://oss.sanwubeixin.cn/material/test/output2.mp4"
    request = FalVideoRequest(
        model=model,
        audio_url=audio_url,
        video_url=video_url
    )

    model = "fal-ai/kling-video/v2/master/image-to-video"
    model = "fal-ai/kling-video/v1/standard/text-to-video"

    #
    # r = arun(create_task(request))
    # logger.debug(f"{r.task_id, r.system_fingerprint}")
    #
    # task_id = r.task_id
    # arun(get_task(task_id, r.system_fingerprint))

    # task_id = "latentsync::b2350e2b-5a48-4390-9089-120fb74f6b7b"
    # token = "843e6ba3-cfb1-4305-be0d-39e923295949:72bce9f9cd5257011ab18f335e2661d4"
    #
    # r = arun(get_task(task_id, token))

    # task_id, token = ('sync-lipsync::45b89e28-8b52-47cb-99de-9b68ce65b9b8',
    #                   '843e6ba3-cfb1-4305-be0d-39e923295949:72bce9f9cd5257011ab18f335e2661d4')
    #
    # r = arun(get_task(task_id, token))

    # task_id, token = ('latentsync::7246cb3b-55e8-490f-bcb1-f05d8c515350',
    #                   '3f712efa-a692-4e7f-9409-e6c505bab4e2:151a0b6093312cc8f66fc52b7c4c92a8')
    #
    # r = arun(get_task(task_id, token))

    task_id, token = ("latentsync::a90be257-3c21-43b2-a05c-6274543c3d02",
                      '843e6ba3-cfb1-4305-be0d-39e923295949:72bce9f9cd5257011ab18f335e2661d4')

    r = arun(get_task(task_id, token))
