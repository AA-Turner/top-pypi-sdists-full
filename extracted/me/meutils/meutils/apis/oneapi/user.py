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

from meutils.pipe import *
from meutils.schemas.oneapi import BASE_URL
from meutils.notice.feishu import send_message
from meutils.db.redis_db import redis_aclient
from meutils.caches import cache, rcache

# https://api.chatfire.cn/api/user/814

token = os.environ.get("CHATFIRE_ONEAPI_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    'rix-api-user': '1'
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
@alru_cache(ttl=3 * 60 * 60)  # todo cache
async def get_api_key_log(api_key: str) -> Optional[list]:  # 日志查询会超时：为了获取 user_id, todo缓存 永久缓存 sk => user
    try:
        if onelog := await redis_aclient.get(f"user:{api_key}"):
            return json.loads(onelog)
        else:

            async with httpx.AsyncClient(base_url=BASE_URL) as client:
                response = await client.get("/api/log/token", params={"key": api_key})
                response.raise_for_status()
                data = response.json()
                if onelog := data['data'][:1]:
                    await redis_aclient.set(f"user:{api_key}", json.dumps(onelog))
                    return onelog
    except Exception as e:
        logger.error(e)
        send_message(f"获取api-key日志失败：{api_key}", title=__name__)
        return


@alru_cache(ttl=60)
async def get_user(user_id):
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.get(f"/api/user/{user_id}")
        # logger.debug(response.text)

        if response.is_success:
            data = response.json()
            return data


async def get_user_money(api_key):
    onelog = await get_api_key_log(api_key)
    if onelog:
        user_id = onelog[0]['user_id']
        data = await get_user(user_id)
        logger.debug(data)
        if data:
            username = data['data']['username']
            quota = data['data']['quota']
            return quota / 500000  # money

    logger.debug(onelog)


async def put_user(payload, add_money: float = 0):
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        payload['quota'] = max(payload['quota'] + add_money * 500000, 0)  # 1块钱对应50万

        response = await client.put("/api/user/", json=payload)
        # logger.debug(response.text)
        # logger.debug(response.status_code)

        return response.json()


@cache()
@rcache()
async def get_user_from_api_key(api_key):
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/log/token", params={"key": api_key})
        response.raise_for_status()
        data = response.json()
        # logger.debug(data)

        if data['data'] and (onelog := data['data'][0]):
            return onelog


if __name__ == '__main__':
    # api-key => get_one_log => get_user => put_user
    # arun(get_user(814))
    # payload = arun(get_user(924))
    # print(payload)
    # arun(put_user(payload, -1))

    # arun(get_api_key_log('sk-gpoH1z3G6nHovD8MY40i6xx5tsC1vbh7B3Aao2jmejYNoKhv'))
    # arun(get_user_money("sk-LlB4W38z9kv5Wy1c3ceeu4PHeIWs6bbWsjr8Om31jYvsucRv"))
    arun(get_user_from_api_key('sk-ROgrPPp2TUdGUC8aNOBwO8Lv0AHZjECKjoT7rBbHbvAKVTKA'))
