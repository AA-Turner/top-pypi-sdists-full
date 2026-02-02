#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : sora
# @Time         : 2024/12/20 16:10
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 动态测试
import json

from meutils.pipe import *
from meutils.db.redis_db import redis_aclient

from meutils.schemas.video_types import SoraVideoRequest, Video

from openai import AsyncOpenAI


class Tasks(object):

    def __init__(self, base_url: Optional[str] = None, api_key: str = None):
        self.api_key = api_key
        self.base_url = base_url
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    async def create(self, request: SoraVideoRequest):  # todo 区分模型
        if video_object := await redis_aclient.get("sora"):
            video =  json.loads(video_object)
            logger.debug(bjson(video))
            return video

    async def get(self, task_id: str):
        if _ := await redis_aclient.get(task_id):
            try:
                video = json.loads(_)
                logger.debug(bjson(video))
                return video
            except Exception as e:
                pass

if __name__ == '__main__':
    arun(Tasks().get('74c084ec-2359-42ce-94c6-e19a0451fbf2'))
    # arun(Tasks().get('sora'))

    # arun(Tasks().create(SoraVideoRequest()))