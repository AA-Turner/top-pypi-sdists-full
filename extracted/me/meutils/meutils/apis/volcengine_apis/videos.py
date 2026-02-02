#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/6/11 15:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import asyncio
import os

from meutils.pipe import *
from meutils.io.files_utils import to_url, to_base64
from meutils.decorators.retry import retrying
from meutils.apis.oneapi.utils import polling_keys

from meutils.llm.clients import AsyncClient
from meutils.schemas.openai_types import CompletionRequest
from meutils.schemas.video_types import VideoRequest, SoraVideoRequest
from meutils.schemas.image_types import ImageRequest

from meutils.db.redis_db import redis_aclient
from meutils.llm.check_utils import check_token_for_volc
# from meutils.llm.check_utils import check_token_for_volc_with_cache as check_token_for_volc

from meutils.config_utils.lark_utils import get_next_token_for_polling, get_series

from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request, HTTPException, status, BackgroundTasks

# Please activate
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Z59Js10DbhT8wdt72LachSDlnlf?sheet=rcoDg7"


async def get_valid_token(tokens: Optional[list] = None, batch_size: Optional[int] = None, seed: int = 0,
                          recheck: bool = False):
    """返回 tokens
    api_key = np.random.choice(api_key.split())

    """
    for i in range(3):  # 最多轮询3次，
        _ = await polling_keys('volc')
        if check_token_for_volc(_):
            tokens = tokens or _
            break

    if not tokens:
        logger.debug("获取轮询key失败，走兜底")

    api_key = tokens or os.getenv('VOLC_API_KEY') or await get_next_token_for_polling(
        feishu_url=FEISHU_URL,
        from_redis=True,
        ttl=24 * 3600,
        check_token=check_token_for_volc
    )
    if isinstance(api_key, list):  # 向下兼容
        api_key = '\n'.join(api_key)

    return api_key

    # tokens = tokens or await get_series(FEISHU_URL, duplicated=True)
    # batch_size = batch_size or 1
    #
    #
    # if seed == 0 and (volc_tokens := await redis_aclient.get(f"volc_tokens")):  # 刷新
    #     volc_tokens = volc_tokens.decode()
    #     if recheck:
    #         valid_tokens = await check_token_for_volc(volc_tokens.split('\n'))
    #
    #         volc_tokens = '\n'.join(valid_tokens)
    #
    #     return volc_tokens
    #
    # valid_tokens = []
    # for token in tokens:
    #     if token := await check_token_for_volc([token]):
    #         valid_tokens += token
    #
    #         logger.debug(valid_tokens)
    #         if len(valid_tokens) == batch_size:
    #             _ = '\n'.join(valid_tokens)
    #             await redis_aclient.set(f"volc_tokens", _, ex=2 * 3600)
    #             # ttl =await redis_aclient.ttl(f"volc_tokens")
    #
    #             return _


# check_image_and_video = partial(check, purpose='video and image')


@retrying()
async def create_task(request: Union[CompletionRequest, VideoRequest, SoraVideoRequest, ImageRequest],
                      api_key: Optional[str] = None):
    # api_key = api_key or await get_next_token_for_polling(feishu_url=FEISHU_URL, check_token=check)
    # api_key = api_key or await get_valid_token()
    #
    # api_key = np.random.choice(api_key.split('\n'))  # todo 轮询

    api_key = api_key or await polling_keys('volc')
    api_key = api_key or await get_next_token_for_polling(
        feishu_url=FEISHU_URL,
        from_redis=True,
        ttl=24 * 3600,
        check_token=check_token_for_volc
    )
    logany(request)

    logger.debug(f"api_key: {api_key}")
    if isinstance(request, SoraVideoRequest):  # todo 首尾帧 参考图
        # logger.debug(request.input_reference)
        # logger.debug(request.first_frame_image)
        # request.input_reference # 数组

        if "lite" in request.model and (
                request.input_reference or request.first_frame_image or request.last_frame_image
        ):
            request.model = request.model.replace("t2v", "i2v")

        request.prompt = request.prompt.split('--', maxsplit=1)[0]  # 取消命令行参数
        request.prompt = f"{request.prompt} --dur {request.seconds}"
        if request.ratio:
            request.prompt += f" --rt {request.ratio}"
        if request.resolution:
            request.prompt += f" --rs {request.resolution}"

        payload = {
            "model": request.model,
            "return_last_frame": True,
            # "callback_url": request.callback_url,
            "callback_url": request.callback_url or f"""{os.getenv("WEBHOOK_URL")}/seedance""",

            "service_tier": "default",

            "content": [
                {
                    "type": "text",
                    "text": request.prompt
                }
            ]
        }
        if request.first_frame_image:
            payload["content"] += [
                {
                    "role": "first_frame",
                    "type": "image_url",
                    "image_url": {
                        "url": request.first_frame_image
                    },
                }
            ]
        if request.last_frame_image:
            payload["content"] += [
                {
                    "role": "last_frame",
                    "type": "image_url",
                    "image_url": {
                        "url": request.last_frame_image
                    },
                }
            ]

        if request.input_reference:  # url
            payload["content"] += [
                {
                    "role": "reference_image",
                    "type": "image_url",
                    "image_url": {
                        "url": image
                    },
                }

                for image in request.input_reference if image
            ]



    elif isinstance(request, VideoRequest):  # 兼容jimeng
        request.prompt = f"{request.prompt.replace('--', '')} --rt {request.aspect_ratio} --dur {request.duration} --rs 1080p"

        payload = {
            "model": "doubao-seedance-1-0-lite-t2v-250428",
            "service_tier": "default",

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
                "service_tier": "default",

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

        if "-pro" in request.model:
            payload['model'] = "doubao-seedance-1-0-pro-250528"  # 未来注销
    elif isinstance(request, ImageRequest):
        text = request.prompt if request.prompt.startswith("--") else ""

        payload = {
            "model": request.model,
            "service_tier": "default",

            "content": [
                {
                    "type": "text",
                    "text": text or "--subdivisionlevel medium --fileformat glb"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": request.image_urls[-1]
                    }
                }
            ]
        }

    else:

        payload = {
            "model": request.model,
            "service_tier": "default",

        }

        if hasattr(request, 'content'):
            payload["content"] = request.content

        elif image_urls := request.last_urls.get("image_url"):
            if payload["model"] not in {"doubao-seedance-1-0-lite-i2v-250428", "doubao-seedance-1-0-pro-250528"}:
                payload["model"] = "doubao-seedance-1-0-lite-i2v-250428"

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

    logany(bjson(payload))

    client = AsyncClient(base_url="https://ark.cn-beijing.volces.com/api/v3", api_key=api_key)

    response = await client.post(
        path="/contents/generations/tasks",
        cast_to=object,
        body=payload
    )

    if task_id := response.get('id'):
        await redis_aclient.set(task_id, api_key, ex=7 * 24 * 3600)

    return response  # {'id': 'cgt-20250611152553-r46ql'}


async def get_task(task_id: str, api_key: Optional[str] = None):
    if isinstance(task_id, list):
        tasks = [get_task(_, api_key) for _ in task_id]
        return asyncio.gather(*tasks)

    if api_key is None:
        token = api_key or await redis_aclient.get(task_id)  # 绑定对应的 token
        api_key = token and token.decode()
        if not token:
            raise HTTPException(status_code=404, detail="TaskID not found")

    client = AsyncClient(base_url="https://ark.cn-beijing.volces.com/api/v3", api_key=api_key)

    response = await client.get(
        path=f"/contents/generations/tasks/{task_id}",
        cast_to=object,
    )

    return response


async def get_task_from_feishu(task_id: Union[str, list], tokens: Optional[list] = None):  # todo: 定时校验
    feishu_url = "https://xchatllm.feishu.cn/sheets/Z59Js10DbhT8wdt72LachSDlnlf?sheet=rcoDg7"
    tokens = tokens or await get_series(feishu_url)

    if isinstance(task_id, list):
        tasks = [get_task_from_feishu(_, tokens) for _ in task_id]
        return await asyncio.gather(*tasks)

    if not await redis_aclient.get(task_id):

        for api_key in tqdm(tokens):
            client = AsyncClient(base_url="https://ark.cn-beijing.volces.com/api/v3", api_key=api_key)
            try:
                response = await client.get(
                    path=f"/contents/generations/tasks/{task_id}",
                    cast_to=object,
                )
                logger.debug(f"{task_id} => {api_key}")

                await redis_aclient.set(task_id, api_key, ex=7 * 24 * 3600)
                break

            except Exception as e:
                # logger.error(e)
                continue


# 执行异步函数
if __name__ == "__main__":
    # api_key = "07139a08-44e2-ba31-07f379bf99ed"  # {'id': 'cgt-20250611164343-w2bzq'} todo 过期调用get

    api_key = "c2449725-f758-42af-8f2c-e05b68dd06ad"  # 欠费

    # api_key = None

    request = CompletionRequest(
        model="doubao-seedance-1-0-pro-250528",
        # model="doubao-seaweed-241128",
        messages=[
            {"role": "user",
             "content": "无人机以极快速度穿越复杂障碍或自然奇观，带来沉浸式飞行体验  --resolution 1080p  --duration 5 --camerafixed false"}
        ],
    )
    request = VideoRequest(
        model="doubao-seedance-1-0-pro-250528",
        prompt="无人机以极快速度穿越复杂障碍或自然奇观，带来沉浸式飞行体验",
        duration=10
    )
    # r = arun(create_task(request, api_key))
    # r = {'id': 'cgt-20250612172542-6nbt2'}

    # arun(get_task(r.get('id')))

    # arun(get_task("cgt-20250707162431-smhwc"))

    # arun(get_task("cgt-20250707160713-j8kll"))

    tokens = arun(polling_keys('', channel_id=21385))

    tokens = list(set(tokens)) + ['68b877dc-a337-4a20-9091-738bb0fcd79c']
    from meutils.apis.oneapi.tasks import get_tasks

    ids = arun(get_tasks(return_ids=True))

    ids = ['cgt-20260126144127-hghhr']


    arun(get_task_from_feishu(ids, tokens))

    # arun(get_valid_token())

    # request = ImageRequest(
    #     model="doubao-seed3d-1-0-250928",
    #     prompt="无人机以极快速度穿越复杂障碍或自然奇观，带来沉浸式飞行体验",
    #     image=[
    #         "https://ark-project.tos-cn-beijing.volces.com/doc_image/seed3d_imageTo3d.png"
    #     ]
    # )
    #
    # r = arun(create_task(request, None))
