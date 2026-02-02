#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/6/20 11:31
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://ppio.com/pricing

from meutils.pipe import *
from meutils.db.redis_db import redis_aclient
from meutils.apis.utils import make_request
from meutils.schemas.hailuo_types import VideoRequest, VideoResponse, Video
from meutils.config_utils.lark_utils import get_series, get_next_token_for_polling, get_next_token
from meutils.llm.check_utils import check_token_for_ppinfra as check_token

from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request, HTTPException, status, BackgroundTasks

base_url = "https://api.ppinfra.com/v3"
feishu_url = "https://xchatllm.feishu.cn/sheets/Z59Js10DbhT8wdt72LachSDlnlf?sheet=b0e241"



async def get_valid_token(min_points=18000):
    _ = await get_next_token(feishu_url, check_token, min_points=min_points, ttl=600)
    logger.debug(_)
    return _


# minimax-hailuo-02-6s-768p minimax-hailuo-02-6s-768p minimax-hailuo-02-6s-1080p

async def create_task(request: VideoRequest, api_key: Optional[str] = None):
    api_key = api_key or await get_valid_token()

    # api_key="sk_4Ja29OIUBVwKo5GWx-PRTsRcTyxxRjZDpYxSdPg75QU"

    path = "/async/minimax-hailuo-02"

    payload = {

        "prompt": request.prompt,
        "image_url": request.first_frame_image,

        "duration": request.duration,
        "resolution": request.resolution.upper(),
        "enable_prompt_expansion": request.prompt_optimizer
    }
    response = await make_request(
        base_url=base_url,
        api_key=api_key,

        path=path,
        payload=payload,
    )

    # return response  # {'task_id': 'f97d3f93-bb29-47d9-9327-77e70982bd43'}

    video_response = VideoResponse(
        task_id=response['task_id'],
        base_resp={
            "status_code": 0,
            "status_msg": "Processing"
        }
    )

    await redis_aclient.set(video_response.task_id, api_key, ex=7 * 24 * 3600)  # todo 装饰器
    return video_response


async def get_task(task_id: str):
    token = await redis_aclient.get(task_id)  # 绑定对应的 token
    token = token and token.decode()

    logger.debug(f"token: {token}")
    if not token:
        raise HTTPException(status_code=404, detail="TaskID not found")

    response = await make_request(
        base_url=base_url,
        api_key=token,

        path=f"/async/task-result?task_id={task_id}",

        method='GET'
    )
    logger.debug(bjson(response))

    if code := response.get("code"):
        raise HTTPException(status_code=code, detail=response)
    """
{
    "audios": [],
    "extra": {},
    "images": [],
    "task": {
        "eta": 0,
        "progress_percent": 0,
        "reason": "",
        "status": "TASK_STATUS_SUCCEED",
        "task_id": "f97d3f93-bb29-47d9-9327-77e70982bd43",
        "task_type": "MINIMAX_HAILUO_02_6S_768P"
    },
    "videos": [
        {
            "nsfw_detection_result": null,
            "video_type": "mp4",
            "video_url": "https://faas-minimax-video-1312767721.cos.ap-shanghai.myqcloud.com/prod/281961854701760-ceb3b321-0ed3-43a3-9bb8-ca579a8abd4f.mp4?q-sign-algorithm=sha1&q-ak=AKIDHOHvKVnrgHkyxhCTyOdeSjoiRxGPSJ0V&q-sign-time=1750392487%3B1750396087&q-key-time=1750392487%3B1750396087&q-header-list=host&q-url-param-list=&q-signature=202c563db2ab6385a7ebe3e4650ee01ed3376e06",
            "video_url_ttl": "0"
        }
    ]
}
    """
    video_response = VideoResponse(
        task_id=task_id,
        status="Processing",
        base_resp={
            "status_code": 0,
            "status_msg": "Processing"
        }
    )
    if response['task']['status'] == 'TASK_STATUS_SUCCEED':
        video_response.status = "Success"
        video_response.base_resp.status_msg = "Success"
        # video_response.videos = Video()
        video_url = response['videos'][0]['video_url']
        video_response.file_id = video_url
        video_response.videos = [Video(videoURL=video_url, downloadURL=video_url, status=2)]


    elif any(i in response['task']['status'].lower() for i in {"fail", 'error'}):
        video_response.status = "Failed"
        video_response.base_resp.status_code = 1027
        video_response.base_resp.status_msg = "Failed"

    return video_response  # {'task_id': 'f97d3f93-bb29-47d9-9327-77e70982bd43'}


if __name__ == '__main__':
    api_key = os.getenv('PPIO_API_KEY')

    payload = {
        "image_url": "https://static.ppinfra.com/docs/assets/minimax-hailuo-video-02-input-image.jpg",
        "prompt": "戴着太阳镜的毛茸茸的熊猫在日出时的雪山顶上跳舞，左移运镜",
        "duration": 6,
        "resolution": "768P",
        "enable_prompt_expansion": True
    }

    request = VideoRequest(
        prompt="戴着太阳镜的毛茸茸的熊猫在日出时的雪山顶上跳舞，左移运镜",
        first_frame_image="https://static.ppinfra.com/docs/assets/minimax-hailuo-video-02-input-image.jpg",
        duration=6,
        resolution="768P",
    )
    api_key = None
    r = arun(create_task(request, api_key=api_key))

    # arun(get_task("d425c44f-da09-4cff-a471-f78757786046"))

    # print(request.model_dump_json(exclude_none=True))

    # arun(get_task("959d759e-da77-42f9-95c5-c29cccc6a894"))

    # arun(get_valid_token())

# "0c830895-1933-4c41-a0cb-37b7387b643a"
"""
curl \
-X POST https://api.ppinfra.com/v3/async/minimax-hailuo-02 \
-H "Authorization: Bearer sk_4Ja29OIUBVwKo5GWx-PRTsRcTyxxRjZDpYxSdPg75QU" \
-H "Content-Type: application/json" \
-d '{
  "image_url": "https://static.ppinfra.com/docs/assets/minimax-hailuo-video-02-input-image.jpg",
  "prompt": "戴着太阳镜的毛茸茸的熊猫在日出时的雪山顶上跳舞，左移运镜",
  "duration": 6,
  "resolution": "1080P",
  "enable_prompt_expansion": true
}'
"""