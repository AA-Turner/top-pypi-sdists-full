#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2024/12/16 17:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from openai import AsyncClient
from meutils.pipe import *
from meutils.apis.jimeng.doubao_utils import generate_cookie, generate_params

from meutils.schemas.image_types import ImageRequest

from meutils.schemas.jimeng_types import BASE_URL, MODELS_MAP, FEISHU_URL
from meutils.config_utils.lark_utils import get_next_token_for_polling


async def create(token: Optional[str] = None):
    token = token or "712a47e7eec7c03b4cc7229775e06841"
    cookie = generate_cookie(token)
    params = generate_params()

    headers = {
        'Cookie': cookie,
        'agw-js-conv': 'str',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'content-type': 'application/json'
    }
    payload = {
        "messages": [
            {
                "content": "{\"text\":\"一只猫\"}",
                "content_type": 2009,
                "attachments": [

                ]
            }
        ],
        "completion_option": {
            "is_regen": False,
            "with_suggest": False,
            "need_create_conversation": False,
            "launch_stage": 1,
            "is_replace": False,
            "is_delete": False,
            "message_from": 0,
            "event_id": "0"
        },
        "section_id": "6287920686327298",
        "conversation_id": "6287920686327042",
        "local_message_id": "936eee40-354d-11f0-83df-6b1810ffef8a"

        # "local_message_id": str(uuid.uuid4())

    }

    client = AsyncClient(base_url="https://www.doubao.com/samantha", default_headers=headers, api_key='xx',
                         )
    response = await client.post("/chat/completion", body=payload, cast_to=object, stream=True,
                                 options=dict(params=params))
    async for i in response:
        print(i)
    # return response


if __name__ == '__main__':
    arun(create())
