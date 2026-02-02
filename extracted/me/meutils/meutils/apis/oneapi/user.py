#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : user
# @Time         : 2024/7/19 14:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: redis缓存, 通过数据库获取 用户余额，补偿余额【扣费逻辑：用户余额够就直接计费，先请求计费+创建任务】，计费函数可返回用户信息
import json
import os

from meutils.pipe import *
from meutils.schemas.oneapi import BASE_URL
from meutils.notice.feishu import send_message
from meutils.caches import cache, rcache
from meutils.apis.oneapi.utils import get_user_quota

# https://api.chatfire.cn/api/user/814

token = os.environ.get("CHATFIRE_ONEAPI_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    'rix-api-user': '1',
    'new-api-user': '1',
    'one-api-user': '1'

}


# https://api.chatfire.cn/api/user/token 刷新token
# https://api.chatfire.cn/api/user/1
# async def get_user(user_id):
#     async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
#         response = await client.get(f"/api/user/{user_id}")
#         logger.debug(response.text)
#
#         if response.is_success:
#             data = response.json()
#             return data
# @rcache(ttl=7 * 24 * 3600)
async def get_api_key_log(api_key: str) -> Optional[list]:  # 日志查询会超时：为了获取 user_id, todo缓存 永久缓存 sk => user
    try:
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30) as client:
            response = await client.get("/api/log/token", params={"key": api_key})
            response.raise_for_status()
            data = response.json()
            if onelog := data['data'][:1]:
                return onelog
    except Exception as e:
        logger.error(e)
        send_message(f"获取api-key日志失败：{api_key}", title=__name__)
        return


async def get_user(user_id):
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.get(f"/api/user/{user_id}")

        if response.is_success:
            data = response.json()
            return data


# get_user_quota
async def get_user_money(api_key):
    return await get_user_quota(api_key=api_key) or 0
    # if onelog := await get_api_key_log(api_key):
    #     onelog = onelog[0]
    #     user_id = onelog['user_id']
    #
    #     data = await get_user(user_id)
    #     logger.debug(data)
    #     if data:
    #         username = data['data']['username']
    #         quota = data['data']['quota']
    #         return quota / 500000  # money
    #
    # logger.debug(onelog)


# 补偿
async def put_user(payload, quota: float = 0):
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        payload['quota'] = quota  # 1块钱对应50万

        response = await client.put("/api/user/", json=payload)
        # logger.debug(response.text)
        # logger.debug(response.status_code)

        return response.json()


async def update_user_for_refund(user_id, quota: int = 0):  # 1块钱对应50万tokens
    data = await get_user(user_id)

    if data := data['data']:
        data['quota'] += quota

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        response = await client.put("/api/user/", json=data)

        return response.json()


@cache()
@rcache()
async def get_user_from_api_key(api_key):
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=15) as client:
        response = await client.get("/api/log/token", params={"key": api_key})
        response.raise_for_status()
        data = response.json()
        # logger.debug(data)

        if data['data'] and (onelog := data['data'][0]):
            return onelog


async def get_user_for_quota(api_key):
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/user/self", headers=headers)
        response.raise_for_status()
        data = response.json()
        # logger.debug(data)

        return data


if __name__ == '__main__':
    pass
    # api-key => get_one_log => get_user => put_user
    # arun(get_user(10988))
    # payload = arun(get_user(1))
    # print(payload)
    # arun(put_user(payload['data'], -1))

    # arun(get_api_key_log("sk-"))

    # arun(get_api_key_log(os.getenv("OPENAI_API_KEY")))

    # arun(get_api_key_log('sk-'))
    arun(get_user_money('sk-x'))

    # arun(get_user_quota("sk-x"))

    # arun(get_user(11327))

    # arun(update_user_for_refund(2, quota=73065879))
