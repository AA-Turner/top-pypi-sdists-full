#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : log
# @Time         : 2024/7/19 14:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.schemas.oneapi import BASE_URL

BASE_URL = "https://api.ffire.cc"


async def get_one_log(api_key: str):
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/log/token", params={"key": api_key})
        logger.debug(response.text)
        # {
        #     "data": ...,
        #     'message': '',
        #     "success": true
        # }
        # data
        # {'channel': 190,
        #  'completion_tokens': 0,
        #  'content': '模型倍率 7.50，分组倍率 1.00',
        #  'created_at': 1721287087,
        #  'id': 3308480,
        #  'is_stream': False,
        #  'model_name': 'tts-1',
        #  'other': '{"group_ratio":1,"model_ratio":7.5}',
        #  'prompt_tokens': 1500,
        #  'quota': 11250,
        #  'token_id': 1092,
        #  'token_name': 'apifox',
        #  'type': 2,
        #  'use_time': 11,
        #  'user_id': 1,
        #  'username': 'chatfire'}
        if response.is_success:
            data = response.json()['data']
            return data and data[-1]


if __name__ == '__main__':
    arun(get_one_log("sk-Qpwj5NcifMz00FBbS2MDa7Km6JCW70UAi0ImJeX9UKfnTviC"))
