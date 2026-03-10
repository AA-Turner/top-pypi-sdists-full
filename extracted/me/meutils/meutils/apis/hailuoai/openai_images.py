#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2024/10/21 20:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://platform.minimaxi.com/document/video_generation?key=66d1439376e52fcee2853049
# https://useapi.net/docs/start-here/setup-minimax
# token 过期时间一个月: 看下free hailuo
# https://jwt.io/
import asyncio

# todo: check token 跳过错误 敏感


from meutils.pipe import *
from meutils.hash_utils import md5
from meutils.io.files_utils import to_bytes, to_url, to_image
from meutils.schemas.hailuo_types import BASE_URL_ABROAD as BASE_URL

from meutils.decorators.retry import retrying, IgnoredRetryException

from meutils.apis.hailuoai.yy import get_yy
from meutils.apis.hailuoai.utils import PARAMS as params, get_access_token, upload

from meutils.schemas.image_types import ImageRequest, ImagesResponse
from meutils.schemas.video_types import SoraVideoRequest, Video

MODELS_MAPPING = {
    "async/nano-banana-pro": "nano-banana2"
}


# @rcache(ttl=7 * 24 * 3600, skip_cache_func=skip_cache_func)

async def generate(request: ImageRequest, api_key: Optional[str] = None, is_async: bool = False):
    refresh_token = api_key or os.getenv("HAILUOAI_API_KEY")
    token = await get_access_token(refresh_token)

    request.model = MODELS_MAPPING.get(request.model, request.model)

    payload = {
        "quantity": request.n,
        "parameter": {
            "modelID": request.model,
            "desc": request.prompt,
            "fileList": [],
            "useOriginPrompt": True if "--enhance" not in request.prompt else False,  # enhance-prompt
            "aspectRatio": request.aspect_ratio or "Auto",
            "resolution": (request.resolution or "1K").title()

            # "resolution": ""

        }
    }

    if request.model.startswith('gpt'):
        if payload['parameter']['aspectRatio'] not in {"Auto", "1:1", "2:3", "3:2"}:
            payload['parameter']['aspectRatio'] = "Auto"

    elif request.model.startswith('nano-banana'):
        if payload['parameter']['aspectRatio'] not in {
            "Auto", '1:1', '21:9', '16:9', '2:3', '3:4', '5:4', '4:5', '4:3', '9:16', '3:2'}:
            payload['parameter']['aspectRatio'] = "Auto"
            payload['parameter']['desc'] += f" --size {request.aspect_ratio}"

    elif request.model.startswith('mj'):
        if payload['parameter']['aspectRatio'] not in {
            "Auto", '1:1', '21:9', '16:9', '2:3', '3:4', '5:4', '4:5', '4:3', '9:16', '3:2'}:
            payload['parameter']['aspectRatio'] = "Auto"

    if request.image:
        payload['parameter']['fileList'] = [
            {
                # "url": url,
                # "url": await to_url(url, filename='xx.jpeg'), # 不是真转换

                "url": await to_image(url, mini_aspect_ratio="2:5"),  # 重置为 jpg

                # "id": "469899357624119304",
                # "name": "image.png",
                # "type": "png",
                # "frameType": 3
            }
            for url in request.image_urls
        ]

    logger.debug(bjson(payload))
    # return
    path = "/v2/api/multimodal/generate/image"
    headers = {
        'Content-Type': 'application/json',
        'token': token,
        'yy': get_yy(payload, params, path),
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(path, params=params, content=json.dumps(payload))
        response.raise_for_status()

        data = response.json()

        logger.debug(bjson(data))

        # 异步任务
        if is_async:
            if task_id := (data.get('data') or {}).get('task', {}).get('batchID'):  # 图片取 batchID
                return Video(id=task_id, status=data)
            else:
                return Video(status='failed', error=data.get("statusInfo"))

        image_response = None
        if task_id := (data.get('data') or {}).get('task', {}).get('batchID'):
            logger.debug(f"TASK_ID: {task_id}")

            for _ in range(60):
                await asyncio.sleep(5) if _ else await asyncio.sleep(16)

                if image_response := await get_task(task_id, token):
                    if image_response.data and len(image_response.data) == request.n:
                        return image_response

        if image_response and image_response.data:
            return image_response
        else:
            raise Exception(f"invalid image null: {task_id} \n\n {request.prompt[:1000]}")


async def get_task(task_id: str, token: str):
    batch_id = task_id

    payload = {
        "batchInfoList": [
            {
                "batchID": batch_id,
                "batchType": 1
            }
        ],
        "type": 1
    }

    path = "/v4/api/multimodal/video/processing"
    headers = {
        'Content-Type': 'application/json',
        'token': token,
        'yy': get_yy(payload, params, url=path),
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(path, params=params, content=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))

        # if any(i in str(data) for i in {"内容生成失败", "请求异常"}):
        #     raise Exception(f"invalid image: {task_id} \n\n {request.prompt[:1000]}")

        if batchs := data['data']['batchVideos']:
            for batch in batchs:
                if batch["batchID"] == task_id:
                    _ = batch["assets"][0]
                    logger.debug(bjson(_))

                    if url := _.get("downloadURL"):
                        data = [{"url": url}]
                        return ImagesResponse(data=data, metadata=payload)

            return ImagesResponse(metadata=payload)
        # if batchs := data['data']['batchVideos']:
        #     if batchs and (assets := batchs[0]['assets']):  # 取第一个
        #
        #         data = [
        #             {"url": image.get("downloadURL")}
        #             for image in assets if image.get("downloadURL")
        #         ]
        #
        #         return ImagesResponse(data=data, metadata=payload)


# todo: 任务状态接口
if __name__ == '__main__':
    token = None
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzIyODE1NzcsInVzZXIiOnsiaWQiOiI0NDQyMjk2MDAzMzA0OTgwNTUiLCJuYW1lIjoibWZ1aiBiamhuIiwiYXZhdGFyIjoiIiwiZGV2aWNlSUQiOiIzMzkxMTQ5Mjg4NjU1Mjk4NjQiLCJpc0Fub255bW91cyI6ZmFsc2V9fQ.__NDyZQQqyYb7TLrumo944EfuCmrbzYngQloNBK4CmM"
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzIzNTA5NjUsInVzZXIiOnsiaWQiOiI0Njk4ODIxOTY3NDM1Mjg0NDkiLCJuYW1lIjoiYWZzbCBkcnF2IiwiYXZhdGFyIjoiIiwiZGV2aWNlSUQiOiIzMTE2NzAxODUwMDg0ODg0NTIiLCJpc0Fub255bW91cyI6ZmFsc2V9fQ.3pO0O36-um2fQs0ML0eHwpi0D7rV5yjmnjcpuiZcNKw"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzIzNTA5NjUsInVzZXIiOnsiaWQiOiI0Njk4ODIxOTY3NDM1Mjg0NDkiLCJuYW1lIjoiYWZzbCBkcnF2IiwiYXZhdGFyIjoiIiwiZGV2aWNlSUQiOiIzMTE2NzAxODUwMDg0ODg0NTIiLCJpc0Fub255bW91cyI6ZmFsc2V9fQ.3pO0O36-um2fQs0ML0eHwpi0D7rV5yjmnjcpuiZcNKw"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzU1MzI2NjAsInVzZXIiOnsiaWQiOiIzMDI4MzM4Njc3NzE5NDkwNTgiLCJuYW1lIjoibWUgYmV0dGVyIiwiYXZhdGFyIjoiIiwiZGV2aWNlSUQiOiIzMDI4MzM3NTk1MTI3NjQ0MTciLCJpc0Fub255bW91cyI6ZmFsc2V9fQ.L5H98MBYB88Gdfokq3O7f5rCMrt19ONTl3hkjgvWcK0"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzU3NDU3NTksInVzZXIiOnsiaWQiOiI0ODQxNjM2NzE3MDE4MzE2ODgiLCJuYW1lIjoi5p2wIOiigSIsImF2YXRhciI6IiIsImRldmljZUlEIjoiMzAyODMzNzU5NTEyNzY0NDE3IiwiaXNBbm9ueW1vdXMiOmZhbHNlfX0.U3oQESgf7qReJ_18WbP5FiGhzrl-eBCaw5K3K6nQD28"
    model = "nano-banana2"
    # model = "nano-banana2_2k"
    # model = "nano-banana2_4k"

    # model = "gpt-image-1.5_High"
    # model = "seedream-4.5_4k"

    # seedream-4.5
    # gpt-image-1.5 {"quantity":1,"parameter":{"modelID":"","desc":"a dog","fileList":[],"useOriginPrompt":true,"aspectRatio":"Auto","resolution":"Low"}}
    # Low
    # Medium
    # High
    # {"quantity":1,"parameter":{"modelID":"gpt-image-1.5","desc":"a dog","fileList":[],"useOriginPrompt":true,"aspectRatio":"Auto","resolution":"Medium"}}

    # model = "gpt-image-1.5"

    # model = "seedream-4.5_2K"
    data = {
        "model": "nano-banana2",
        "prompt": "使图片变清晰，不改变原图比例 --4K",
        # "image": [
        #     "https://cdnzjzai.m.nengshuohuihua.com/banana/refer/202602/02/20260202185746552733.jpeg?auth_key=1770029895-78f88911851543c692009bcfb89072b9-0-073258e5b2a3121093e5fc0875908869"
        # ],
        "resolution": "4k"
    }
    request = ImageRequest(**data)

    model = "mj_v7_4K"
    # mj_niji7
    request = ImageRequest(
        model=model,
        n=1,
        # prompt="笑起来",
        # prompt="哭起来",
        # prompt="裸体少女 没传内裤",
        prompt="a cat",

        # image="https://s3.ffire.cc/files/jimeng.jpg",
        # image=["https://s3.ffire.cc/files/jimeng.jpg"] * 3,

        # size="16:9"
        # resolution="Low"
        # resolution=None
    )

    r = arun(generate(request, api_key=token, is_async=True))

    # model = "veo3.1-t2v-fast"
    task_id = "469896308304285702_469873163803475974"
    # "message": "内容生成失败，请重试",

    # task_id = "469872667202084865_469872667202084866"
    # 469872667202084865
    # task_id = "469901294006366214_469901294006366212"  # n=1
    task_id = "469901776552665096_469901776552665097"  # n=2

    task_id = "469902511826763781"  # n=3

    task_id = "472570702555033603"  # 4k

    # task_id = "472571658445312008"
    task_id = "20251225095015"
    # arun(get_task(task_id=task_id, token=token))

