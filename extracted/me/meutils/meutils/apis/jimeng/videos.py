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
from meutils.schemas.video_types import VideoRequest
from meutils.schemas.task_types import TaskResponse
from meutils.apis.jimeng.common import get_headers, check_token
from meutils.apis.jimeng.files import upload_for_image, upload_for_video

from meutils.config_utils.lark_utils import get_next_token_for_polling

from fake_useragent import UserAgent

ua = UserAgent()


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

        if video_urls := json_path(data, "$..video_url"):  # 角色检测 create_realman_avatar

            task_data = dict(zip(["video"] * len(video_urls), video_urls))
            response = TaskResponse(task_id=task_id, data=task_data, metadata=data, status="success")
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
                response.status = "success"

            return response


async def create_task(request: VideoRequest, token: Optional[str] = None):
    token = "d2d142fc877e696484cc2fc521127b36"  ################### 线上注释掉

    token = token or await get_next_token_for_polling(FEISHU_URL, check_token)

    url = "/mweb/v1/generate_video"

    headers = get_headers(url, token)

    task_extra = {
        "promptSource": "custom",
        "originSubmitId": str(uuid.uuid4()),
        "isDefaultSeed": 1,
        "originTemplateId": "",
        "imageNameMapping": {},
        "isUseAiGenPrompt": False,
        "batchNumber": 1
    }
    payload = {
        "submit_id": str(uuid.uuid4()),
        "task_extra": json.dumps(task_extra),
        "input": {
            "video_aspect_ratio": request.aspect_ratio,
            "seed": 1751603315,  ##### seed 10位
            "video_gen_inputs": [
                {
                    "prompt": request.prompt,
                    "fps": 24,
                    "duration_ms": request.duration * 1000,
                    "video_mode": 2,
                    "template_id": ""
                }
            ],
            "priority": 0,
            "model_req_key": "dreamina_ic_generate_video_model_vgfm_3.0",  # request.model
        },
        "mode": "workbench",
        "history_option": {},
        "commerce_info": {
            "resource_id": "generate_video",
            "resource_id_type": "str",
            "resource_sub_type": "aigc",
            "benefit_type": "basic_video_operation_vgfm_v_three"
        },
        "client_trace_data": {}
    }

    if request.image_url:
        # image_url = "tos-cn-i-tb4s082cfz/a116c6a9dcbc41b889f9aabdef645456"
        image_url = await upload_for_image(request.image_url, token, biz="video")
        # vid, uri = await upload_for_video(request.image_url, token)
        # logger.debug(f"vid: {vid}, uri: {uri}")
        payload['input'].pop('video_aspect_ratio', None)
        payload['input']['video_gen_inputs'][0]['first_frame_image'] = {
            "width": 1024,
            "height": 1024,
            "image_uri": image_url
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


if __name__ == '__main__':
    token = None
    token = "d2d142fc877e696484cc2fc521127b36"

    request = VideoRequest(
        model="dreamina_ic_generate_video_model_vgfm_3.0",
        prompt="笑起来",
        image_url="https://oss.ffire.cc/files/kling_watermark.png",  # 图生有问题
    )

    with timer():
        r = arun(create_task(request, token))
        print(r)

    # arun(get_task(r.task_id))
    # arun(get_task(r.task_id, "d2d142fc877e696484cc2fc521127b36"))
