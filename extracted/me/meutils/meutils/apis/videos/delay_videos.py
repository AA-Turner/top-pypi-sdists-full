#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : delay_videos
# @Time         : 2026/2/16 11:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import shortuuid

from meutils.pipe import *
from meutils.schemas.video_types import SoraVideoRequest, Video, VolcVideoResponse
from meutils.db.redis_db import redis_aclient


class Tasks(object):

    def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
    ):
        self.api_key = api_key
        self.base_url = base_url or ""

    async def create(self, request: SoraVideoRequest):
        task_id = f"delay::{shortuuid.random()}"
        return Video(id=task_id)

    async def get(self, task_id: str):
        return Video(id=task_id)


if __name__ == '__main__':
    request = SoraVideoRequest()
    arun(Tasks().create(request))
