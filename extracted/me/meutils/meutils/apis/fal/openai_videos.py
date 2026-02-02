#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_videos
# @Time         : 2026/1/27 19:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from meutils.apis.fal.images import check

from meutils.schemas.task_types import TaskResponse
from meutils.schemas.video_types import VideoRequest

from meutils.schemas.fal_types import FEISHU_URL
from meutils.config_utils.lark_utils import get_next_token_for_polling

from fal_client import AsyncClient
from meutils.schemas.video_types import SoraVideoRequest, Video


class Tasks(object):

    def __init__(self, base_url: Optional[str] = None, api_key: str = None):
        self.api_key = api_key
        self.client = AsyncClient(key=api_key)

    async def create(self, request: SoraVideoRequest):
        application = request.model

        payload = {
            "prompt": request.prompt,
            "delete_video": False,
            "aspect_ratio": "auto"
        }

        if request.model.startswith(("fal-ai/sora",)):
            payload["duration"] = min(int(request.seconds or 4), 12)

            if request.resolution:
                payload['resolution'] = request.resolution

            if request.aspect_ratio:
                payload['aspect_ratio'] = request.aspect_ratio

            if images := request.input_reference:
                payload['image_url'] = images[0]

        response = await self.client.submit(
            application=application,
            arguments=payload
        )
        logger.debug(response.__class__.__name__)  # Queued, InProgress, COMPLETED
        logger.debug(response.__dict__)  # Queued, InProgress, COMPLETED

        task_id = f"{application.replace('/', '|')}::{response.request_id}"

        return Video(id=task_id, status=response.__dict__)

    async def get(self, task_id: str, api_key: Optional[str] = None):
        if api_key:
            self.client = AsyncClient(key=api_key)

        application, task_id = task_id.split('::')
        application = application.replace('|', '/')

        response = await self.client.status(application, task_id, with_logs=True)

        logger.debug(response.__class__.__name__)  # Queued, InProgress, COMPLETED
        logger.debug(response.__dict__)  # Queued, InProgress, COMPLETED

        if metrics := response.__dict__.get("metrics"):  # {'inference_time': 17.29231595993042}
            logger.debug(metrics)
            try:
                response = await self.client.result(application, task_id)

            except Exception as e:

                print(str(e))
                """
                [{'loc': ['body', 'aspect_ratio'], 'msg': "unexpected value; permitted: '9:16', '16:9'", 'type': 'value_error.const', 'ctx': {'given': 'auto', 'permitted': ['9:16', '16:9']}}]
                """

        return response


if __name__ == '__main__':
    request = SoraVideoRequest(model="fal-ai/sora-2/text-to-video")

    api_key = os.getenv("FAL_KEY")
    t = Tasks(api_key=api_key)

    # arun(t.create(request))

    task_id = "fal-ai|sora-2|text-to-video::303f48a7-507e-424a-a9ce-2ddaf0bf21b6"
    arun(t.get(task_id, api_key))
