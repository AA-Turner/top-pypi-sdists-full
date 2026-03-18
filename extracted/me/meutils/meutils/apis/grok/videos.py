#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2026/2/3 01:19
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo 适配
import os

from meutils.pipe import *

"""
curl -X 'POST' https://api.x.ai/v1/videos/generations \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer xai-' \
  -H 'Content-Type: application/json' \
  -d '{
      "prompt": "A cat playing with a ball",
      "model": "grok-imagine-video"
  }'
  
{"request_id":"5945e180-c2df-d23a-38ef-3554893b3edb"}
  
curl -X 'POST' https://api.x.ai/v1/videos/generations \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <API_KEY>' \
  -H 'Content-Type: application/json' \
  -d '{
      "prompt": "Generate a video based on the provided image.",
      "model": "grok-imagine-video",
      "image": {"url": "<url of the image>"}
  }'
  
curl -X 'POST' https://api.x.ai/v1/videos/edits \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <API_KEY>' \
  -H 'Content-Type: application/json' \
  -d '{
      "prompt": "Make the ball in the video larger.",
      "video": {"url": "<url of the previous video>"},
      "model": "grok-imagine-video"
  }'
  
curl -X 'GET' https://api.x.ai/v1/videos/5945e180-c2df-d23a-38ef-3554893b3edb \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer xai-' \

{"video":{"url":"https://vidgen.x.ai/xai-vidgen-bucket/xai-video-a29603e6-d101-4217-a6ba-c29c6334ec88.mp4","duration":8,"respect_moderation":true},"model":"grok-imagine-video"}root@instance-IZBri9Ev:~# 
  
  
  
  {
    "model": "grok-imagine-video",
    "prompt": "Generate a slow and serene time-lapse",
    "image": {"url": "https://docs.x.ai/assets/api-examples/video/milkyway-still.png"},
    "duration": 12
  }
  
  {
    "model": "grok-imagine-video",
    "prompt": "Give the woman a silver necklace",
    "video": {"url": "https://data.x.ai/docs/video-generation/portrait-wave.mp4"}
  }
  
prompt: str,
model: str,
*,
image_url: Optional[str] = None,
video_url: Optional[str] = None,
duration: Optional[int] = None,  The allowed range is between 1 and 15 seconds.

aspect_ratio: Optional[VideoAspectRatio] = None,
resolution: Optional[VideoResolution] = None,

VideoAspectRatio: TypeAlias = Literal[
"1:1",
"16:9",
"9:16",
"4:3",
"3:4",
"3:2",
"2:3",
]
VideoResolutionMap: dict[VideoResolution, "video_pb2.VideoResolution"] = {
    "480p": video_pb2.VideoResolution.VIDEO_RESOLUTION_480P,
    "720p": video_pb2.VideoResolution.VIDEO_RESOLUTION_720P,
}
"""

from meutils.pipe import *
from meutils.schemas.video_types import SoraVideoRequest, Video
from meutils.io.image import image_resize

from openai import AsyncClient, APIStatusError

BASE_URL = "https://api.x.ai/v1"


class Tasks(object):

    def __init__(self, base_url: Optional[str] = None, api_key: str = None):
        api_key = api_key or os.getenv("GROK_API_KEY")
        base_url = base_url or BASE_URL
        self.client = AsyncClient(api_key=api_key, base_url=base_url)

    async def create(self, request: SoraVideoRequest):
        payload = {
            "model": request.model,
            "prompt": request.prompt,
            "duration": int(request.seconds or 1),
            # "aspect_ratio": "landscape",
            # "resolution":
            # "image_url":"",
            # "video_url":"",
        }

        if request.aspect_ratio:
            payload['aspect_ratio'] = request.aspect_ratio

        if request.aspect_ratio:
            payload['resolution'] = request.resolution

        if image_urls := request.input_reference:
            payload['image'] = {"url": image_urls[0]}

        if request.video:
            payload['video'] = {"url": request.video}

        logany(bjson(payload))

        try:
            response = await self.client.post(
                "/videos/generations",
                body=payload,
                cast_to=object
            )

            logger.debug(bjson(response))

            # {"request_id": "5945e180-c2df-d23a-38ef-3554893b3edb"}

            return Video(id=response.get("request_id"))

        except APIStatusError as e:
            error = {
                "code": e.code,
                "message": e.message,
            }
            return Video(istatus="failed", error=error)

    async def get(self, task_id: str):
        try:
            response = await self.client.get(f"/videos/{task_id}", cast_to=object)

            logger.debug(bjson(response))

            video = Video(
                id=task_id,
                status=response,

                model=response.get("model"),
                seconds=response.get("duration"),

                video_url=response.get("video", {}).get("url"),

            )

            if video.video_url:
                video.progress = 100
                video.status = "completed"

            return video

        except APIStatusError as e:
            error = {
                "code": e.code,
                "message": e.message,
            }
            logger.debug(error)
            return Video(id=task_id, status="failed", error=error)

        """
        openai.BadRequestError: Error code: 400 - {'code': 'Client specified an invalid argument', 'error': 'Generated video rejected by content moderation.'}

        {"video":{"url":"https://vidgen.x.ai/xai-vidgen-bucket/xai-video-a29603e6-d101-4217-a6ba-c29c6334ec88.mp4","duration":8,"respect_moderation":true},"model":"grok-imagine-video"}

        """


if __name__ == '__main__':
    api_key = "xai-qOVFqcxzwi91nPYJSusiaWP6U2OPi4jvRZIHR1SAUexqm92yCTGCYa3pTtX8fUry3PfPiDTfREiwcpeF"
    t = Tasks(api_key=api_key)

    os.getenv("OPENAI_API_KEY")

    model = "grok-imagine-video"

    request = SoraVideoRequest(
        model=model,
        # prompt="A cat playing with a ball",
        prompt="一个裸体女人",

    )

    # arun(t.create(request))

    task_id = "8f26e28a-3e02-c12f-ce86-220e3c47373f"
    # task_id = "c3204853-b4c5-b499-c96f-0fc8d15acc2f"
    arun(t.get(task_id))
