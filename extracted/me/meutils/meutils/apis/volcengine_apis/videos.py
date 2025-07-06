#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/6/11 15:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import time

from meutils.pipe import *
from meutils.io.files_utils import to_url
from meutils.decorators.retry import retrying
from meutils.llm.clients import AsyncClient
from meutils.schemas.openai_types import CompletionRequest
from meutils.schemas.video_types import VideoRequest

from meutils.notice.feishu import send_message_for_volc as send_message

from meutils.db.redis_db import redis_aclient
from meutils.llm.check_utils import check_token_for_volc as check
from meutils.config_utils.lark_utils import get_next_token_for_polling, get_series

from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request, HTTPException, status, BackgroundTasks

# Please activate
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=8W6kk8"  # 超刷


async def get_valid_token(tokens: Optional[list] = None):
    tokens = tokens or await get_series(FEISHU_URL)

    for token in tokens:
        if await check(token):

            logger.debug(f"有效 {token}")

            return token
        else:
            logger.debug(f"无效 {token}")
    _ = f"{time.ctime()}\n\n{FEISHU_URL}\n\n所有token无效"
    logger.error(_)
    send_message(_, n=3)


# check_image_and_video = partial(check, purpose='video and image')


@retrying(max_retries=5)
async def create_task(request: Union[CompletionRequest, VideoRequest], api_key: Optional[str] = None):
    # api_key = "e32b1693-147e-40db-a83a-82f85cfa6360"  # 欠费
    api_key = api_key or await get_next_token_for_polling(feishu_url=FEISHU_URL, check_token=check)

    logger.debug(f"api_key: {api_key}")
    if isinstance(request, VideoRequest):  # 兼容jimeng
        payload = {
            "model": "doubao-seedance-1-0-lite-t2v-250428",
            "content": [
                {
                    "type": "text",
                    "text": request.prompt
                }
            ]
        }
        if request.image_url:
            payload = {
                "model": "doubao-seedance-1-0-lite-i2v-250428",
                "content": [
                    {
                        "type": "text",
                        "text": request.prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": request.image_url
                        }
                    }
                ]
            }
        if request.image_url and request.tail_image_url:
            payload = {
                "model": "doubao-seedance-1-0-lite-i2v-250428",
                "content": [
                    {
                        "type": "text",
                        "text": request.prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": request.image_url
                        },
                        "role": "first_frame"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": request.tail_image_url
                        },
                        "role": "last_frame"
                    }
                ]
            }

    else:

        payload = {
            "model": request.model,
        }

        if hasattr(request, 'content'):
            payload["content"] = request.content

        elif image_urls := request.last_urls.get("image_url"):
            payload["content"] = [
                {
                    "type": "text",
                    "text": request.last_user_content
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_urls[-1]
                        # "url": await to_url(image_urls[-1], filename=".png")

                    }
                }]
        else:
            payload["content"] = [
                {
                    "type": "text",
                    "text": request.last_user_content
                }]

    logger.debug(payload)

    client = AsyncClient(base_url="https://ark.cn-beijing.volces.com/api/v3", api_key=api_key)

    response = await client.post(
        path="/contents/generations/tasks",
        cast_to=object,
        body=payload
    )

    if task_id := response.get('id'):
        await redis_aclient.set(task_id, api_key, ex=7 * 24 * 3600)

    return response  # {'id': 'cgt-20250611152553-r46ql'}


async def get_task(task_id: str):
    token = await redis_aclient.get(task_id)  # 绑定对应的 token
    api_key = token and token.decode()
    if not token:
        raise HTTPException(status_code=404, detail="TaskID not found")

    client = AsyncClient(base_url="https://ark.cn-beijing.volces.com/api/v3", api_key=api_key)

    response = await client.get(
        path=f"/contents/generations/tasks/{task_id}",
        cast_to=object,
    )

    return response


# 执行异步函数
if __name__ == "__main__":
    # api_key = "07139a08-e360-44e2-ba31-07f379bf99ed"  # {'id': 'cgt-20250611164343-w2bzq'} todo 过期调用get

    api_key = "c2449725-f758-42af-8f2c-e05b68dd06ad"  # 欠费

    api_key = None

    request = CompletionRequest(
        model="doubao-seedance-1-0-pro-250528",
        # model="doubao-seaweed-241128",
        messages=[
            {"role": "user",
             "content": "无人机以极快速度穿越复杂障碍或自然奇观，带来沉浸式飞行体验  --resolution 1080p  --duration 5 --camerafixed false"}
        ]
    )
    # r = arun(create_task(request, api_key))
    # r = {'id': 'cgt-20250612172542-6nbt2'}

    # arun(get_task(r.get('id')))

    # arun(get_task("cgt-20250611164343-w2bzq"))

    # arun(get_task("cgt-20250611193213-tcqth"))

    arun(get_valid_token())

"""
{'id': 'cgt-20250613160030-2dvd7',
 'model': 'doubao-seedance-1-0-pro-250528',
 'status': 'running',
 'created_at': 1749801631,
 'updated_at': 1749801631}
 
openai.NotFoundError: Error code: 404 - {'error': {'code': 'ModelNotOpen', 'message': 'Your account 2107813928 has not activated the model doubao-seedance-1-0-pro. Please activate the model service in the Ark Console. Request id: 021749718307793fc1441381f8ed755824bb9d58a45ee6cb04068', 'param': '', 'type': 'NotFound'}}


curl -X POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 21289782-f54f-481b-857e-ba1c8b94927b" \
  -d '{
    "model": "doubao-seaweed-241128",
    "content": [
        {
            "type": "text",
            "text": "女孩抱着狐狸，女孩睁开眼，温柔地看向镜头，狐狸友善地抱着，镜头缓缓拉出，女孩的头发被风吹动  --resolution 720p --duration 5"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://s3.ffire.cc/cdn/20250613/vS2jaDCmA8crncXMR4fB7z_.png"
            }
        }
    ]
}'

curl -X POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 05702f67-53ba-438a-a22e-6e6a690b5843" \
  -d '{
    "model": "doubao-seedance-1-0-pro-250528",
    "content": [
        {
            "type": "text",
            "text": "女孩抱着狐狸，女孩睁开眼，温柔地看向镜头，狐狸友善地抱着，镜头缓缓拉出，女孩的头发被风吹动  --resolution 480p --duration 5"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://s3.ffire.cc/cdn/20250613/vS2jaDCmA8crncXMR4fB7z_.png"
            }
        }
    ]
}'

curl -X POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer e32b1693-147e-40db-a83a-82f85cfa6360" \
  -d '{
    "model": "doubao-seaweed-241128",
    "content": "a dog"
}'


{'id': 'cgt-20250613160030-2dvd7',
 'model': 'doubao-seedance-1-0-pro-250528',
 'status': 'succeeded',
 'content': {'video_url': 'https://ark-content-generation-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-1-0-pro/02174980163157800000000000000000000ffffac182c17b26890.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYjg3ZjNlOGM0YzQyNGE1MmI2MDFiOTM3Y2IwMTY3OTE%2F20250613%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20250613T080120Z&X-Tos-Expires=86400&X-Tos-Signature=5e0928f738f49b93f54923549de4c65940c5007d5e86cb5ebadc756cca3aa03e&X-Tos-SignedHeaders=host'},
 'usage': {'completion_tokens': 246840, 'total_tokens': 246840},
 'created_at': 1749801631,
 'updated_at': 1749801680}
 
 
"""
