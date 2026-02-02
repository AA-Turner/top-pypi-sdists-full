#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2026/1/29 14:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo 基础 继承
import os

from meutils.pipe import *
from meutils.schemas.video_types import SoraVideoRequest, Video

from openai import AsyncOpenAI
from openai import APIError

"""https://aiping.cn/docs/API/VideoAPI/KLING_VIDEO_API_DOC
o1

文生视频
图生视频（首尾帧）
图片/主体参考生成视频
视频编辑（指令变换）
视频风格/运镜参考
视频延长（生成下一个/上一个镜头）

动作控制 API 支持通过参考图像和参考视频生成动作控制视频，生成视频中的人物动作与参考视频一致。



目前kling-video-o1正确的示例是这样的👇

curl -X 'https://www.aiping.cn/api/v1/videos' \
--header 'Authorization: Bearer xxx' \
--header 'Content-Type: application/json' \
--data '{
            "model": "Kling-Video-O1",
            "prompt": "参考<<<video_1>>>的运镜方式，生成一段视频：<<<element_1>>>和<<<element_2>>>在东京街头漫步，偶遇<<<image_1>>>",
            "reference_images": [
               "http://wanx.alicdn.com/material/20250318/stylization_all_1.jpeg"
            ],
            "element_list": [
                {
                    "element_id": "146"
                },
                {
                    "element_id": "145"
                }
            ],
            "video_list": [
                {
                    "video_url": "https://cdn.wanx.aliyuncs.com/static/demo-wan26/vace.mp4",
                    "refer_type": "feature",
                    "keep_original_sound": "yes"
                }
            ],
            "mode": "pro",
            "aspect_ratio": "1:1",
            "duration": "7"
        }'
"""

BASE_URL = "https://aiping.cn/api/v1"


class Tasks(object):

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("AIPING_API_KEY")
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=BASE_URL)

    async def create(self, request: SoraVideoRequest):  # todo 区分模型
        payload = {
            "model": request.model,
            "prompt": request.prompt,
            "seconds": request.seconds,
        }

        if request.model.endswith("-pro"):
            payload["mode"] = "pro"
            payload["model"] = payload["model"].strip("-pro")
        elif request.model.endswith("-std"):
            payload["mode"] = "std"
            payload["model"] = payload["model"].strip("-std")

        for param in ["aspect_ratio", "action_control", "callback_url", "character_orientation"]:
            if hasattr(request, param) and getattr(request, param) is not None:
                payload[param] = getattr(request, param)

        if urls := request.input_reference:
            payload['image_url'] = urls[0]  # 845850588004376646_437103
            payload['reference_images'] = urls

        if url := request.first_frame_image:
            payload['first_frame_url'] = url

        if url := request.last_frame_image:
            payload['last_frame_url'] = url

        if url := request.image:
            payload["image_url"] = url

        if url := request.video:
            payload['video_url'] = url

        logger.debug(bjson(payload))

        try:

            response = await self.client.post(path="/videos", body=payload, cast_to=object)
            logger.debug(response)
            """
            {'id': '845809073383034963_437103', 'status': 'queued', 'created_at': '2026-01-29T11:11:56.304273Z', 'model': 'Kling-Video-O1', 'provider': '可灵AI'}
            
            openai.InternalServerError: Error code: 500 - {'detail': {'message': "ERROR: Provider 可灵AI returned status 400: {'code': 1201, 'message': 'Aspect ratio must be specified when no first image and not video editing', 'request_id': '9d490e21-b381-4b26-a071-f04afd83efb8'} (status=400)", 'error_type': 'internal_error'}}
            """
            if isinstance(response, dict) and (task_id := response.get("id")):
                response.pop("created_at", None)
                return Video(**response)

        except APIError as e:
            error = {
                'code': e.code, 'message': e.message
            }
            # return Video(status="failed", error=error)
            raise e

    async def get(self, task_id: str, ):
        response = await self.client.get(path=f"/videos/{task_id}", cast_to=object)
        logger.debug(bjson(response))
        if response.get("status") == "completed":
            response.pop("created_at", None)
            response.pop("completed_at", None)

            return Video(**response)

        """
        {
    "id": "845809073383034963_437103",
    "status": "completed",
    "created_at": "2026-01-29T11:11:56.000000Z",
    "model": "Kling-Video-O1",
    "completed_at": "2026-01-29T11:17:12.746607Z",
    "updated_at": "2026-01-29T11:17:12.746607Z",
    "video_url": "https://v4-fdl.kechuangai.com/ksc2/pNKqHLkicA7peTCVLqaCxKvdsGNOBvxTnPaNWI9B6jufiqlFt2WiyAlMSd5NtBIa0ltAD74tDG9kdlxYasJxoOUBjwZzBjiHNw5x45ryioAHK3gLZxA2I-THacdKLOaPx2nLXZhRW4bXz4wjd6B-ZNFchWoR6flf85Kll44wAPoai5x4zk3sRFzEIs4KafgcMSWIhWOg-2vx4AP2SmToHQ.mp4?cacheKey=ChtzZWN1cml0eS5rbGluZy5tZXRhX2VuY3J5cHQSsAGGLL3aBUGCX5e0UqY87UWl6t4SFbxKr5xtoA6iRap5mQRIGvAZNb_t0O8xMlBLYtt-3drDYWmmABJyD8m8jE1pQ_zatvsYkEPZXxWhXXi48QrXbQwqtCNhuVOyMiiBtSwdDaq_a1a9k6WToopVBEyoKGazRM_ls38pt7yrBnwka2nvbkdiUknhuxXlul5y0RT6w-JzOwMVTiffkeZe1zGm2v5rxn1vd8OVRqGvAhqBrhoSK9DDR3Zts0AO39BBzVqoebvyIiDqaVNmCGa6E5OcURU5sWKA7aHrUnblB0T7_qwLc6_RSigFMAE&x-kcdn-pid=112757&pkey=AAUPAfYdTaZ0RM3N37CbkD6NjOFIU0Va0gh0erjEo6oMxbjhUNt58DFTsqMR0QqyElhUJ2V0RPvRidOboyAZQdUXih3gzOMwIgzS5NtgYG-CSytBbjPduh5EsU03Z5KIiIU",
    "raw_response": {
        "code": 0,
        "message": "SUCCEED",
        "request_id": "db60eb9b-a00c-4e90-8e98-a5e881939d16",
        "data": {
            "task_id": "845809073383034963",
            "task_status": "succeed",
            "task_info": {},
            "task_result": {
                "videos": [
                    {
                        "id": "845809073525633087",
                        "url": "https://v4-fdl.kechuangai.com/ksc2/pNKqHLkicA7peTCVLqaCxKvdsGNOBvxTnPaNWI9B6jufiqlFt2WiyAlMSd5NtBIa0ltAD74tDG9kdlxYasJxoOUBjwZzBjiHNw5x45ryioAHK3gLZxA2I-THacdKLOaPx2nLXZhRW4bXz4wjd6B-ZNFchWoR6flf85Kll44wAPoai5x4zk3sRFzEIs4KafgcMSWIhWOg-2vx4AP2SmToHQ.mp4?cacheKey=ChtzZWN1cml0eS5rbGluZy5tZXRhX2VuY3J5cHQSsAGGLL3aBUGCX5e0UqY87UWl6t4SFbxKr5xtoA6iRap5mQRIGvAZNb_t0O8xMlBLYtt-3drDYWmmABJyD8m8jE1pQ_zatvsYkEPZXxWhXXi48QrXbQwqtCNhuVOyMiiBtSwdDaq_a1a9k6WToopVBEyoKGazRM_ls38pt7yrBnwka2nvbkdiUknhuxXlul5y0RT6w-JzOwMVTiffkeZe1zGm2v5rxn1vd8OVRqGvAhqBrhoSK9DDR3Zts0AO39BBzVqoebvyIiDqaVNmCGa6E5OcURU5sWKA7aHrUnblB0T7_qwLc6_RSigFMAE&x-kcdn-pid=112757&pkey=AAUPAfYdTaZ0RM3N37CbkD6NjOFIU0Va0gh0erjEo6oMxbjhUNt58DFTsqMR0QqyElhUJ2V0RPvRidOboyAZQdUXih3gzOMwIgzS5NtgYG-CSytBbjPduh5EsU03Z5KIiIU",
                        "duration": "5.041"
                    }
                ]
            },
            "task_status_msg": "",
            "created_at": 1769685116248,
            "updated_at": 1769685162155,
            "final_unit_deduction": "4"
        }
    },
    "usage": {
        "seconds": 5.041,
        "video_count": 1
    }
}
        """


if __name__ == '__main__':
    api_key = "QC-26c8f1bf2f34ced0079651def44a5e84-1023520e28cbc06c1a54eb1a85ae2200"  # os.getenv("AIPING_API_KEY")

    model = "Kling-Video-O1"  # 845851366781628485_437103
    # 3-10，文生视频仅支持 5 和 10

    request = SoraVideoRequest(
        model=model,
        prompt="让花被风吹动",
        seconds=5,
        aspect_ratio="9:16",
        # first_frame_image="http://wanx.alicdn.com/material/20250318/stylization_all_1.jpeg",
        input_reference=["http://wanx.alicdn.com/material/20250318/stylization_all_1.jpeg"],

        # prompt="视频中女生用图片中人物的动作",
        # action_control=True,
        # character_orientation="image",
        # image="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
        # video="https://v4-fdl.kechuangai.com/ksc2/WDy7TzddQesPc-yzgBHGLPC-DvJ1-H7xTMOmXwQyWLqad7vNOco9rc4aaG2TUWYGqLjRbIfafrJKn4BKLbkawwZsP7XbXQjyZejDDnV72jn7_uOKClcPl_3iIfXtHjik6qPjvmUX8BMCVAJu-9SnQfKNe24uiR78liroaGqRYtK-N_fG73vxHzRKCzkLlGT7No6T2cwFXwB-N25EbGzEnA.mp4?cacheKey=ChtzZWN1cml0eS5rbGluZy5tZXRhX2VuY3J5cHQSsAEma1yqW3VkomHRW0QCf5HwtoGt1rsP1BfAaMCMvDUwUAQgKlNOKcqrRXahLmKVhnsgoDAIr_8ClW7Alw0lH5jlAnCMEDaevpHviFPuz_l2o1AiF-2MAuH85g_3pxisF25afS-VkzHeF345qaxRQpXl9svOZ5KJY-iGnO2MZsk8d5sq-T8BgaiacFbWhYGDsAGIl6cUtyKhje6Q0iavjLp2FWU6qRBNpxQMr5y-flEUVRoS09j_LL38Qv8Yv5Zh0thEYW8BIiBztCBY7m6iJP0Ol_qpaQSK1zVVBP52cd9VUG0X30dhHygFMAE&x-kcdn-pid=112757&pkey=AAVML7K6rCyYzbp4euU3NAb4liSq8HDEALE2jL_AqZqjp8ylQaYSG0AWd4-sSxFiQXblYdsfN46p1KRhcn1JfQLKTL30VMioea-RzCILZQ_lHHOkDkLQwT2MfkktWUeLDSA"
    )

    t = Tasks(api_key=api_key)
    # arun(t.create(request))
    #
    # arun(t.get("845850588004376646_437103"))
    # task_id = "845852484547010604_437103"
    task_id = "845857300375576633_437103"
    arun(t.get(task_id))
