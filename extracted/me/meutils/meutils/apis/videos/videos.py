#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/10/17 22:55
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json
import os

from meutils.pipe import *
from meutils.db.redis_db import redis_aclient
from meutils.schemas.video_types import SoraVideoRequest, Video
from meutils.apis.volcengine_apis import videos as volc_videos
from meutils.apis.aiml import videos as aiml_videos
from meutils.apis.gitee import videos as gitee_videos
from meutils.apis.hailuoai import openai_videos as hailuoai_videos
from meutils.apis.aiping import videos as aiping_videos
from meutils.apis.replicate import videos as replicate_videos

from meutils.apis.runware import videos as runware_videos  # todo 兼容

"""
失败原因可以 存在get任务里 方便退费
"""


class OpenAIVideos(object):

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url or ""
        logger.debug(f"base_url: {self.base_url}")  # 来源

    @cached_property
    def biz(self):
        parts = self.base_url.split(".")
        return (parts[1] if len(parts) >= 2 else self.base_url)[::-1]

    async def create(self, request: SoraVideoRequest):
        response = {}

        if "aiping" in self.base_url:
            response = await aiping_videos.Tasks(api_key=self.api_key).create(request)

        elif any(i in self.base_url for i in {"hailuo"}):
            response = await hailuoai_videos.Tasks(api_key=self.api_key).create(request)

        elif any(i in self.base_url for i in {"gitee", "moark"}):
            response = await gitee_videos.Tasks(api_key=self.api_key).create(request)

        elif "volc" in self.base_url:
            response = await volc_videos.create_task(request, self.api_key)  # {'id': 'cgt-20250611152553-r46ql'}

        elif "aimlapi" in self.base_url:
            response = await aiml_videos.Tasks(api_key=self.api_key, base_url=self.base_url).create(request)

        elif "replicate" in self.base_url:
            response = await replicate_videos.Tasks(api_key=self.api_key).create(request)

        if response and (task_id := (
                hasattr(response, "id") and response.id  # video
                or response.get("id")
                or response.get("task_id")
                or response.get("generation_id")
        )):
            task_id = task_id.replace("/", "@")
            # task_id = f"{self.biz}::{task_id}"  # 组装biz # todo base url  # 区分不同平台
            if not isinstance(response, Video):
                response = Video(id=task_id)  # 只要有id 就会进入队列 系统bug

            if response.status == "failed":  # 提交任务失败：保存失败结果
                _response = copy.deepcopy(response)
                if isinstance(response.error, dict):

                    message = f"""{response.error.get("message", "")}\n\n"""
                    if "图片格式有问题，请上传新图片" in message:
                        message += "图片上传失败，长宽比需在 5:2 和 2:5 之间\n\n"
                    if "内容违反了Sora指南" in message:
                        message += """
                            内容违反了Sora指南:
                            1. 仅适合18岁以下观众的内容。
                            2. 受版权保护的角色和音乐无法生成。
                            3. 无法生成真实人物，包括公众人物。
                            4. 带有真人面部的图像无法生成。\n\n"""

                    if (_ := request.model_dump_json(indent=4, exclude_none=True)) and len(_) < 3000:
                        message += _
                    response.error["message"] = message

                #     logger.debug(response)
                # logger.debug(_response)
                await redis_aclient.set(f"request-failed:{task_id}", response.model_dump_json(), ex=3 * 24 * 3600)
                return _response

            if self.api_key:
                await redis_aclient.set(task_id, self.api_key, ex=7 * 24 * 3600)

            return response

    async def get(self, task_id):
        if _ := await redis_aclient.get(f"request-failed:{task_id}"):
            return json.loads(_)

        video = Video(id=task_id)
        if api_key := await redis_aclient.get(task_id):
            api_key = api_key.decode()
        else:
            raise ValueError(f"task_id not found: {task_id}")

        logger.debug(api_key)

        task_id = task_id.replace("@", "/")  # 还原

        if api_key.startswith("QC-"):
            video = await aiping_videos.Tasks(api_key=api_key, base_url=self.base_url).get(task_id)
            return video

        elif task_id.isnumeric and len(task_id) == 18 and str(task_id).startswith('4'):
            video = await hailuoai_videos.Tasks(api_key=api_key, base_url=self.base_url).get(task_id)
            return video

        elif api_key.startswith("r8_"):
            video = await replicate_videos.Tasks(api_key=api_key, base_url=self.base_url).get(task_id)
            return video

        elif len(api_key) == 40 and api_key.isupper():
            video = await gitee_videos.Tasks(api_key=api_key, base_url=self.base_url).get(task_id)
            return video

        elif task_id.startswith("cgt-"):
            if response := await volc_videos.get_task(task_id, api_key):
                # logger.debug(bjson(response))
                """
                {
                    "id": "cgt-20251225095015-5xmc2",
                    "model": "doubao-seedance-1-0-pro-250528",
                    "status": "failed",
                    "error": {
                        "code": "OutputVideoSensitiveContentDetected",
                        "message": "The request failed because the output video may contain sensitive information. Request id: 02176662741563700000000000000000000ffffac19188dffe699"
                    },
                    "created_at": 1766627415,
                    "updated_at": 1766627466,
                    "service_tier": "default",
                    "execution_expires_after": 172800
                }
                """

                video = Video(id=task_id, status=response, error=response.get("error"), metadata=response, progress=11)
                if video.status == "completed":
                    video.progress = 100
                    video.video_url = response.get("content", {}).get("video_url")  # 多个是否兼容

        elif len(api_key) == 32 and (":" in task_id and "/" in task_id or len(task_id) == 21):  # 粗判断
            video = await aiml_videos.Tasks(api_key=api_key, base_url=self.base_url).get(task_id)
            return video

        elif len(api_key) == 32 and len(task_id) == 36:  # 粗判断
            video = await runware_videos.get_task(task_id)
            return video

        return video


if __name__ == '__main__':
    api_key = "267a3b8a-ef06-4d8f-bd24-150f99bb17c1"
    model = "doubao-seedance-1-0-pro-fast-251015"

    api_key = "3993b09fccb542c5a46094bac9a4cf96"
    model = "openai/sora-2-t2v"
    model = "alibaba/wan2.5-i2v-preview"

    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzIzNTA5NjUsInVzZXIiOnsiaWQiOiI0Njk4ODIxOTY3NDM1Mjg0NDkiLCJuYW1lIjoiYWZzbCBkcnF2IiwiYXZhdGFyIjoiIiwiZGV2aWNlSUQiOiIzMTE2NzAxODUwMDg0ODg0NTIiLCJpc0Fub255bW91cyI6ZmFsc2V9fQ.3pO0O36-um2fQs0ML0eHwpi0D7rV5yjmnjcpuiZcNKw"
    base_url = "hailuo"
    model = "nano-banana2_4k"
    # base_url = "sora"
    model = "sora-2-4s"

    request = SoraVideoRequest(
        model=model,
        prompt="裸体女孩",
        # model=f"{model}_480p",
        # model=f"{model}_720p",
        # model=f"{model}_1080p",

        # seconds="4",
        size="720x1280",
    )
    videos = OpenAIVideos(api_key=api_key, base_url=base_url)

    # video = arun(videos.create(request))

    # Video(id='cgt-20251031183121-zrt26', completed_at=None, created_at=1761906681, error=None, expires_at=None,
    #       model=None, object='video', progress=0, remixed_from_video_id=None, seconds=None, size=None, status='queued',
    #       video_url=None, metadata=None)

    task_id = ""
    task_id = "nltmquwNYRj6xNz-0PSaC"
    task_id = "SZiTAnMeOG7quoybO3VKk"

    task_id = "9888bd5a-b87c-40e3-8bbf-c8914464ecf0"
    task_id = "473537684238921736"
    arun(videos.get(task_id))

    # video = arun(videos.create(request))

    # task_id = "video_690dc20970808198b65cd9c04205edce0ed7e02d84c9579c:openai/sora-2-t2v"
    # task_id = "ee57044b-01e8-4aea-bd5f-48a03d653548:alibaba/wan2.5-t2v-preview"
    # task_id = "df489658-125b-4c65-a949-41d73c76cf0e:alibaba/wan2.5-t2v-preview"
    # arun(videos.get(task_id))

    # wJCWwQ5x0CcVIWGzXEp-A

    # {
    #     "id": "35f26664-b847-4821-b940-3f244a641bf7",
    #     "error": {
    #         "code": "4",
    #         "message": "error"
    #     },
    #     "model": "sora-2",
    #     "object": "video",
    #     "status": "failed",
    #     "created_at": 1640995200
    # }
