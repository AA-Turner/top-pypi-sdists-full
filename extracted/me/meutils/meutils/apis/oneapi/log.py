#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : log
# @Time         : 2024/7/19 14:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from meutils.schemas.oneapi import BASE_URL


async def get_one_log_for_key(api_key: str, base_url: str = "https://api.chatfire.cn"):
    async with httpx.AsyncClient(base_url=base_url) as client:
        response = await client.get("/api/log/token", params={"key": api_key})
        response.raise_for_status()
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
        # logger.debug(response.json())
        if response.is_success:
            data = response.json()['data']
            return data and data[-1]


async def get_logs(response_id: str, base_url: str = "https://api.chatfire.cn", **kwargs):
    """

    :param response_id:
    :param type: 日志类型
        2 消费层级
    :param base_url:
    :return:
    """
    headers = {
        'rix-api-user': '1',
        'new-api-user': '1',

        'Authorization': os.getenv("CHATFIRE_ONEAPI_TOKEN"),
    }

    submit_timestamp = int(time.time() - 24 * 3600)
    end_timestamp = int(time.time() - 10 * 60)

    params = {

        "start_timestamp": submit_timestamp,
        "end_timestamp": end_timestamp,
        "response_id": response_id,
        **kwargs
    }

    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=60) as client:
        response = await client.get("/api/log/", params=params)
        response.raise_for_status()

        response = response.json()
        # logger.debug(bjson(response))
        return response


if __name__ == '__main__':
    arun(get_one_log_for_key("sk-Qpwj5NcifMz00FBbS2MDa7Km6JCW70UAi0ImJeX9UKfnTviC"))

    task_id = "d7d0efe4-8bdc-455f-8009-67561e83dce9"

    arun(get_logs(task_id, type=2))
