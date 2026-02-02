#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2026/1/13 11:34
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from openai import AsyncOpenAI
from meutils.schemas.video_types import SoraVideoRequest, Video
# Python 示例代码
import requests
import json


class Tasks(object):

    def __init__(self, base_url: Optional[str] = None, api_key: str = None):
        base_url = "https://api.bizyair.cn/w/v1/webapp/task/openapi"

        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)

    async def create(self, request: SoraVideoRequest):
        payload = {
            "web_app_id": request.model,
            "suppress_preview_output": True,
            "input_values": {
                # "18:LoadImage.image": "https://bizyair-prod.oss-cn-shanghai.aliyuncs.com/inputs/20251227/CSbjai7F7Cl6CCDZsnzrrU3270kDCmsk.png",
                "54:BizyAir_Sora_V2_I2V_API.prompt": "镜头从杂乱桌面推近到焦虑的二冰侧面，画面分屏展示手动操作步骤快切，最终定格在闪烁的待办便利贴特写。画外音，手动重复操作真折磨人，必须要用自动化搞定！",
                "54:BizyAir_Sora_V2_I2V_API.aspect_ratio": request.ratio,
                "54:BizyAir_Sora_V2_I2V_API.duration": request.seconds,
                "54:BizyAir_Sora_V2_I2V_API.size": "large"
            }
        }



        logany(bjson(payload))

        default_headers = {
            "X-BizyAir-Task-WebHook-Url": f"""{os.getenv("WEBHOOK_URL")}/{payload['model']}"""
        }

        response = await self.client.post(
            path="/video/generations",
            body=payload,
            cast_to=object,
            options={"headers": default_headers}
        )
        """
        生成结果: {'request_id': '8307183e-8387-4e62-895b-a41781a3123c'}

        """

        logger.debug(bjson(response))

        return response

    async def get(self, task_id: str):
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

        """
        logger.debug(bjson(response))

        video = Video(
            id=task_id,
            status=response,
            video_url=(response.get("video") or {}).get("url"),

            error=response.get("error")
        )

        # logger.debug(bjson(video))

        return video


api_key = os.getenv("BIZYAIR_API_KEY")

url = "https://api.bizyair.cn/w/v1/webapp/task/openapi/create"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "X-BizyAir-Task-WebHook-Url": f"""{os.getenv("WEBHOOK_URL")}/sora"""
}
data = {
    "web_app_id": 41928,
    "suppress_preview_output": True,
    "input_values": {
        "18:LoadImage.image": "https://bizyair-prod.oss-cn-shanghai.aliyuncs.com/inputs/20251227/CSbjai7F7Cl6CCDZsnzrrU3270kDCmsk.png",
        "54:BizyAir_Sora_V2_I2V_API.prompt": "镜头从杂乱桌面推近到焦虑的二冰侧面，画面分屏展示手动操作步骤快切，最终定格在闪烁的待办便利贴特写。画外音，手动重复操作真折磨人，必须要用自动化搞定！",
        "54:BizyAir_Sora_V2_I2V_API.aspect_ratio": "9:16",
        "54:BizyAir_Sora_V2_I2V_API.duration": 15,
        "54:BizyAir_Sora_V2_I2V_API.size": "large"
    }
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print("生成结果:", result)


# X-BizyAir-Task-WebHook-Url

# async def create
# [b'{"type": "API", "status": "Success", "created_at": "2026-01-13 13:09:01", "updated_at": "2026-01-13 13:14:17", "executed_at": "2026-01-13 13:09:02", "running_at": "2026-01-13 13:09:03", "ended_at": "2026-01-13 13:14:17", "expired_at": "2026-01-28 00:00:00", "request_id": "8307183e-8387-4e62-895b-a41781a3123c", "outputs": [{"object_url": "https://storage.bizyair.cn/outputs/e09fca58-56c4-4496-bd1a-97eaea28fe0c_f73b572084eacc48e6284141c9143bb4_video_ComfyUI_91b561c8_00001_.mp4", "output_ext": ".mp4", "cost_time": 315030, "audit_status": 2, "error_type": "NOT_ERROR"}], "cost_times": {"inference_cost_time": 315095, "running_cost_time": 315944, "total_cost_time": 316152, "real_cpu_cost_time": 425, "real_total_cost_time": 4667, "real_bizyair_cost_time": 4242}}']
