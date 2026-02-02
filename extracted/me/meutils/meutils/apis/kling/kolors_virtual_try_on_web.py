#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : virtual_try_on
# @Time         : 2024/11/25 09:48
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""
dressInput
upperInput
lowerInput
{
    "type": "mmu_img2img_aitryon",
    "arguments": [
        {
            "name": "personType",
            "value": "WOMAN"
        },
        {
            "name": "__modelImageType",
            "value": "OFFICIAL_MODEL_女模特4.png"
        },
        {
            "name": "imageCount",
            "value": "2"
        },
        {
            "name": "biz",
            "value": "klingai"
        }
    ],
    "inputs": [
        {
            "name": "lowerInput",
            "inputType": "URL",
            "url": "https://h2.inkwai.com/bs2/upload-ylab-stunt/kling/tryon/model/v3/下装4.png"
        },
        {
            "name": "humanImage",
            "inputType": "URL",
            "url": "https://p2.a.kwimgs.com/bs2/upload-ylab-stunt/kling/tryon/model/v3/女模特4.png"
        }
    ]
}

"""
import jwt

from meutils.pipe import *
from meutils.schemas.task_types import TaskResponse  ############# 根据这个重构
from meutils.schemas.kling_types import API_BASE_URL, TryOnRequest, TaskResponse
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.decorators.retry import retrying

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=cjTepf"


def encode_jwt_token(token):
    ak, sk = token.split('|')
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 24 * 3600,  # 有效时间，此处示例代表当前时间+1800s(30min)
        "nbf": int(time.time()) - 5  # 开始生效的时间，此处示例代表当前时间-5秒
    }
    token = jwt.encode(payload, sk, headers=headers)
    logger.debug(token)
    return token


###################################################################### 重构

######################################################################
@alru_cache(ttl=3600)
@retrying(title=__name__)
async def create_task(request: TryOnRequest, token: Optional[str] = None):  ###### 所有的 TaskResponse标准化
    token = token or await get_next_token_for_polling(FEISHU_URL)
    token = encode_jwt_token(token)

    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = request.model_dump()
    async with httpx.AsyncClient(base_url=API_BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post("/v1/images/kolors-virtual-try-on", json=payload)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))

        return TaskResponse(**data, system_fingerprint=token)


@retrying(title=__name__)  # 触发重试
async def get_task(task_id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    async with httpx.AsyncClient(base_url=API_BASE_URL, headers=headers, timeout=60) as client:
        response = await client.get(f"/v1/images/kolors-virtual-try-on/{task_id}")
        response.raise_for_status()
        data = response.json()
        return TaskResponse(**data)


if __name__ == '__main__':
    request = TryOnRequest()
    # arun(create_task(request))
    # {
    #     "code": 0,
    #     "message": "SUCCEED",
    #     "request_id": "CjMVomdAMUcAAAAAAHcmvg",
    #     "data": {
    #         "task_id": "CjMVomdAMUcAAAAAAHcmvg",
    #         "task_status": "submitted",
    #         "created_at": 1732500869112,
    #         "updated_at": 1732500869112
    #     }
    # }

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkMmU1NmZkY2ZiODY0MmZmYWEyMjZlZWIxNzY4MzMyMiIsImV4cCI6MTczMzE4OTI4OSwibmJmIjoxNzMzMTAyODg0fQ.YjB792REbuFaUoyUXvd5bpI76_0PBWawDHDjPHOBA5Q'
    arun(get_task("CjiL9mdJhswAAAAAAG2C6g", token))
