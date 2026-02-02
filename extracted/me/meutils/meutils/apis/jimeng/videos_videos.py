#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : lip_sync
# @Time         : 2025/1/3 16:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""
1. 上传图片 image_to_avatar检测
2. 上传视频 video_to_avatar检测
3. 上传音频+创建任务

"""
import asyncio

from meutils.pipe import *
from meutils.str_utils.json_utils import json_path

from meutils.schemas.jimeng_types import BASE_URL, MODELS_MAP, FEISHU_URL
from meutils.schemas.video_types import LipsyncVideoRequest
from meutils.schemas.task_types import TaskResponse
from meutils.apis.jimeng.common import get_headers, check_token
from meutils.apis.jimeng.files import upload_for_image, upload_for_video

from meutils.config_utils.lark_utils import get_next_token_for_polling

from fake_useragent import UserAgent

ua = UserAgent()


async def create_realman_avatar(image_url: str, token: str):
    if image_url.startswith("http"):
        image_url = await upload_for_image(image_url, token)

    url = "/mweb/v1/create_realman_avatar"
    headers = get_headers(url, token)

    payload = {
        "input_list": [
            {
                "image_uri": image_url,
                "submit_id": str(uuid.uuid4()),
                "mode": 0
            },
            {
                "image_uri": image_url,
                "submit_id": str(uuid.uuid4()),
                "mode": 1
            }
        ]
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))  # 1914628189186

        response = TaskResponse(metadata=data, system_fingerprint=token)
        if task_ids := json_path(data, "$..task_id"):  # 返回 imageurl vid
            response.task_id = ' '.join(task_ids)
            return response

        else:
            response.message = str(json_path(data, "$..message"))
            response.status = "fail"
            return response


async def get_task(task_id: str, token: str = "916fed81175f5186a2c05375699ea40d"):
    """
    $..image_to_avatar 成功： 先检测图片or视频
    :param task_ids:
    :return:
    """
    task_ids = task_id.split()

    url = "/mweb/v1/mget_generate_task"
    headers = get_headers(url, token)

    payload = {"task_id_list": task_ids}
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))

        if json_path(data, "$..image_to_avatar"):  # 角色检测 create_realman_avatar
            resource_id_std = resource_id_loopy = ""
            if resource_id_stds := json_path(data, "$..resource_id_std"):
                resource_id_std = "".join(resource_id_stds)

            if resource_id_loopys := json_path(data, "$..resource_id_loopy"):
                resource_id_loopy = "".join(resource_id_loopys)

            task_data = {
                "resource_id_std": resource_id_std,
                "resource_id_loopy": resource_id_loopy
            }
            response = TaskResponse(task_id=task_id, data=task_data, metadata=data)
            if resource_id_std and resource_id_loopy:
                response.status = "success"

            if (message := json_path(data, "$..image_to_avatar.message")) and "fail" in str(message).lower():
                response.message = str(message)
                response.status = "fail"

            return response

        else:
            response = TaskResponse(task_id=task_id, metadata=data)
            if (message := json_path(data, "$..fail_msg")) and "success" not in str(message).lower():
                response.message = str(message)
                response.status = "fail"
                return response

            if will_cost := json_path(data, "$..will_cost"):
                response.will_cost = will_cost[0]

            if video_urls := json_path(data, "$..[360p,480p,720p].video_url"):
                response.data = [{"video": _} for _ in video_urls]

            return response


async def create_task(request: LipsyncVideoRequest, token: Optional[str] = None):
    # token = token or await get_next_token_for_polling(FEISHU_URL, check_token)
    token = "7c5e148d9fa858e3180c42f843c20454"  # 年付
    token = "916fed81175f5186a2c05375699ea40d"  # 月付

    url = "/mweb/v1/batch_generate_video"

    headers = get_headers(url, token)

    model = request.model
    scene = "lip_sync_image"
    image_url = await upload_for_image(request.image_url, token)

    # 角色检测
    realman_avatar_response = await create_realman_avatar(image_url, token)
    if realman_avatar_response.status == "fail":
        return realman_avatar_response

    else:
        for _ in range(10):
            task_response = await get_task(realman_avatar_response.task_id, token)
            if task_response.status == "fail":
                logger.debug("fail")
                return task_response
            elif task_response.status == "success":
                logger.debug("success")

                realman_avatar_response = task_response
                break
            else:
                await asyncio.sleep(3)
                continue

    audio_vid, audio_url = await upload_for_video(request.audio_url, token)

    resource_id_std = realman_avatar_response.data.get("resource_id_std")
    resource_id_loopy = realman_avatar_response.data.get("resource_id_loopy")

    i2v_opt = v2v_opt = {}
    if request.video_url:
        v2v_opt = {}

    # payload = {
    #     "submit_id": "",
    #     "task_extra": "{\"promptSource\":\"photo_lip_sync\",\"generateTimes\":1,\"lipSyncInfo\":{\"sourceType\":\"local-file\",\"name\":\"vyFWygmZsIZlUO4s0nr2n.wav\"},\"isUseAiGenPrompt\":false,\"batchNumber\":1}",
    #     "http_common_info": {
    #         "aid": 513695
    #     },
    #     "input": {
    #         "seed": 3112889115,
    #         "video_gen_inputs": [
    #             {
    #                 "v2v_opt": {},
    #                 "i2v_opt": {
    #                     "realman_avatar": {
    #                         "enable": True,
    #                         "origin_image": {
    #                             # "width": 800,
    #                             # "height": 1200,
    #                             "image_uri": "tos-cn-i-tb4s082cfz/4dead1bfc8e84572a91f2e047016a351",
    #                             "image_url": ""
    #                         },
    #                         "origin_audio": {
    #                             # "duration": 9.976625,
    #                             "vid": "v02870g10004cu8d4r7og65j2vr5opb0"
    #                         },
    #
    #                         "resource_id_std": "381c534f-bcef-482e-8f17-5b30b64e41a1",
    #                         "resource_id_loopy": "b9ac51cb-e26c-4b63-81d9-34ed24053032",
    #                         #
    #                         # "tts_info": "{\"name\":\"vyFWygmZsIZlUO4s0nr2n.wav\",\"source_type\":\"local-file\"}"
    #                     }
    #                 },
    #                 "audio_vid": "v02870g10004cu8d4r7og65j2vr5opb0",
    #                 "video_mode": 4
    #             }
    #         ]
    #     },
    #     "mode": "workbench",
    #     "history_option": {},
    #     "commerce_info": {
    #         "resource_id": "generate_video",
    #         "resource_id_type": "str",
    #         "resource_sub_type": "aigc",
    #         "benefit_type": "lip_sync_avatar_std",  # 5积分
    #         # "benefit_type": "lip_sync_avatar_lively" # 10积分
    #     },
    #     "scene": "lip_sync_image",
    #     "client_trace_data": {},
    #     "submit_id_list": [
    #         str(uuid.uuid4())
    #     ]
    # }

    if request.image_url:
        i2v_opt = {
            "realman_avatar": {
                "enable": True,
                "origin_image": {
                    "image_uri": image_url,
                    "image_url": ""
                },
                "resource_id_loopy": resource_id_loopy,
                "resource_id_std": resource_id_std,
                "origin_audio": {
                    "vid": audio_vid
                },
                # "tts_info": "{\"name\":\"vyFWygmZsIZlUO4s0nr2n.wav\",\"source_type\":\"local-file\"}"
            }
        }

    payload = {
        "submit_id": "",
        # "task_extra": "{\"promptSource\":\"photo_lip_sync\",\"generateTimes\":1,\"lipSyncInfo\":{\"sourceType\":\"local-file\",\"name\":\"vyFWygmZsIZlUO4s0nr2n.wav\"},\"isUseAiGenPrompt\":false,\"batchNumber\":1}",
        "http_common_info": {
            "aid": 513695
        },
        "input": {
            "seed": 2032846910,
            "video_gen_inputs": [
                {
                    "v2v_opt": v2v_opt,
                    "i2v_opt": i2v_opt,
                    "audio_vid": audio_vid,
                    "video_mode": 4
                }
            ]
        },
        "mode": "workbench",
        "history_option": {},
        "commerce_info": {
            "resource_id": "generate_video",
            "resource_id_type": "str",
            "resource_sub_type": "aigc",
            "benefit_type": model,
            # "benefit_type": "lip_sync_avatar_lively" # 10积分
        },
        "scene": scene,
        "client_trace_data": {},
        "submit_id_list": [
            str(uuid.uuid4())
        ]
    }

    logger.debug(bjson(payload))

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))

    if task_ids := json_path(data, "$..task.task_id"):
        task_id = task_ids[0]
        return TaskResponse(task_id=task_id, system_fingerprint=token)


# {
#     "submit_id": "740e28e3-12fd-4ab6-82da-7f2028ac6314",
#     "task_extra": "{\"promptSource\":\"custom\",\"originSubmitId\":\"3575ebec-1d35-42f1-bd19-6cf0c8dee0b1\",\"isDefaultSeed\":1,\"originTemplateId\":\"\",\"imageNameMapping\":{},\"isUseAiGenPrompt\":false,\"batchNumber\":1}",
#     "input": {
#         "video_aspect_ratio": "16:9",
#         "seed": 840565633,
#         "video_gen_inputs": [
#             {
#                 "prompt": "现代几何构图海报模板，庆祝男演员都市爱情剧《街角晚风》成功。画面分割为几个深红和灰色块面。一个灰色块内展示清晰的德塔文景气指数上升曲线图（深红线条）。一个色块放置男演员侧脸剧照。剧名和标语“人气飙升，全城热恋”分布在不同色块上，字体设计现代。整体风格简约、结构化、高级。",
#                 "fps": 24,
#                 "duration_ms": 5000,
#                 "video_mode": 2,
#                 "template_id": ""
#             }
#         ],
#         "priority": 0,
#         "model_req_key": "dreamina_ic_generate_video_model_vgfm_3.0"
#     },
#     "mode": "workbench",
#     "history_option": {},
#     "commerce_info": {
#         "resource_id": "generate_video",
#         "resource_id_type": "str",
#         "resource_sub_type": "aigc",
#         "benefit_type": "basic_video_operation_vgfm_v_three"
#     },
#     "client_trace_data": {}
# # }

if __name__ == '__main__':
    token = "916fed81175f5186a2c05375699ea40d"

    request = LipsyncVideoRequest(
        model="lip_sync_avatar_std",
        image_url="https://oss.ffire.cc/files/kling_watermark.png",
        video_url="",
        audio_url="https://oss.ffire.cc/files/lipsync.mp3"
    )

    # with timer():
    #     r = arun(create_realman_avatar(request.image_url, token))
    #     arun(get_task(r.task_id))

    # image_uri = "tos-cn-i-tb4s082cfz/387649a361e546f89549bd3510ab926d"
    # task_ids = arun(create_realman_avatar(image_uri, token="7c5e148d9fa858e3180c42f843c20454"))
    # arun(mget_generate_task(task_ids))
    with timer():
        r = arun(create_task(request))
    # arun(get_task(r.task_id))
