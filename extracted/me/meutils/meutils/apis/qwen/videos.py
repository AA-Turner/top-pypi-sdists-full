#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2026/1/16 11:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://bailian.console.aliyun.com/cn-beijing/?tab=api&accounttraceid=01bd0ba7095b400185920afa50d3ede3nmpi#/api/?type=model&url=2867393

from meutils.pipe import *
from openai import AsyncOpenAI
from meutils.schemas.video_types import SoraVideoRequest, Video

"""

curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.6-i2v",
    "input": {
        "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。",
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true,
        "duration": 10,
        "audio": true,
        "shot_type":"multi"
    }
}'

curl --location --request GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"


"""
BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
BASE_URL = "https://dashscope-intl.aliyuncs.com/api/v1"


# generate_audion
class Tasks(object):

    def __init__(self, base_url: Optional[str] = None, api_key: str = None):
        self.client = AsyncOpenAI(base_url=BASE_URL, api_key=api_key)

    async def create(self, request: SoraVideoRequest):
        payload = {
            "model": request.model,
            "input": {
                "prompt": request.prompt,
                # "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
                # "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
            },
            "parameters": {
                # "resolution": "720P",
                "prompt_extend": True,
                # "duration": 10,
                # "audio": true,
                # "shot_type": "multi"
            }
        }
        # parameters
        if request.seconds:
            payload["parameters"]["duration"] = int(request.seconds)

        if request.resolution:
            payload["parameters"]["resolution"] = request.resolution

        if request.shot_type:
            payload["parameters"]["shot_type"] = request.shot_type

        # 参考图
        if request.input_reference:
            payload['input']['img_url'] = request.input_reference

        if image_urls := request.input_reference:
            payload['model'] = request.model.replace("text-to-video", "image-to-video").replace("t2v", "i2v")

            payload['input']['img_url'] = image_urls[0]


        else:
            payload['model'] = request.model.replace("image-to-video", "text-to-video").replace("i2v", "t2v")

        # 首尾帧
        if request.first_frame_image:
            payload['input']['first_frame_url'] = request.first_frame_image

        if request.last_frame_image:
            payload['input']['last_frame_url'] = request.last_frame_image

        if request.video:
            if request.model.startswith(("alibaba/wan-2-6",)):
                payload["video_urls"] = [request.video]
                payload['model'] = "alibaba/wan-2-6-r2v"

            else:
                payload["video_url"] = request.video
                payload['keep_audio'] = True

                if request.model.endswith('edit'):  # kling
                    payload['model'] = "klingai/video-o1-video-to-video-edit"
                else:
                    payload['model'] = "klingai/video-o1-video-to-video-reference"

        logany(bjson(payload))

        response = await self.client.post(
            path="/video/generations",
            body=payload,
            cast_to=object
        )
        """
        {
    "id": "9913239d-4fa8-47ea-b51d-d313e29caba5:alibaba/wan2.5-i2v-preview",
    "status": "queued",
    "meta": {
        "usage": {
            "tokens_used": 105000
        }
    }

    {
    "generation_id": "339995387916622:minimax/hailuo-02",
    "status": "queued",
    "meta": {
        "usage": {
            "tokens_used": 588000
        }
    }
}
}
        """

        logger.debug(bjson(response))

        return response

    async def get(self, task_id: str):
        logger.debug(task_id)

        response = await self.client.get(
            path=f"/video/generations?generation_id={task_id}",
            cast_to=object
        )
        """
        {
    "id": "9913239d-4fa8-47ea-b51d-d313e29caba5:alibaba/wan2.5-i2v-preview",
    "status": "completed",
    "video": {
        "url": "https://cdn.aimlapi.com/alpaca/1d/dd/20251107/30b07d9c/42740107-9913239d-4fa8-47ea-b51d-d313e29caba5.mp4?Expires=1762593280&OSSAccessKeyId=LTAI5tBLUzt9WaK89DU8aECd&Signature=Guk6apyEnKeuniLv0mcBJhkHO%2FI%3D"
    }
}

{
    "id": "",
    "status": "unknown",
    "error": {
        "name": "Error",
        "message": "invalid params, task_id cannot by empty"
    }
}

        """
        logger.debug(bjson(response))

        status = response
        if response.get('error'):
            status = 'failed'

        video = Video(
            id=task_id,
            status=status,
            video_url=(response.get("video") or {}).get("url"),

            error=response.get("error")
        )

        # logger.debug(bjson(video))

        return video
