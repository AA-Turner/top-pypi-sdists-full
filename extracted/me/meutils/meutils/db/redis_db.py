#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : redis
# @Time         : 2024/3/26 11:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
# from meutils.pipe import *

import os
from redis import Redis, ConnectionPool
from redis.asyncio import Redis as AsyncRedis, ConnectionPool as AsyncConnectionPool

kwargs = {
    "retry_on_timeout": True,
    # "db": 6
}
if REDIS_URL := os.getenv("REDIS_URL"):
    # logger.debug(REDIS_URL)

    pool = ConnectionPool.from_url(REDIS_URL, **kwargs)
    redis_client = Redis.from_pool(pool)

    async_pool = AsyncConnectionPool.from_url(REDIS_URL, **kwargs)
    redis_aclient = AsyncRedis.from_pool(async_pool)
    # redis_client = Redis.from_url(REDIS_URL, **kwargs)
    # redis_aclient = AsyncRedis.from_url(REDIS_URL, **kwargs)

else:
    redis_client = Redis(**kwargs)  # decode_responses=True
    redis_aclient = AsyncRedis(**kwargs)


async def sadd(name, *values, ttl: int = 0):
    await redis_aclient.sadd(name, *values)

    if ttl:
        await redis_aclient.expire(name, ttl)


if __name__ == '__main__':
    from meutils.pipe import *

    # print(arun(redis_aclient.get("")))
    # print(redis_client.lrange("https://api.moonshot.cn/v1",0, -1))

    # print(redis_client.lrange("https://api.deepseek.com/v1",0, -1))
    # print(redis_client.exists("https://api.deepseek.com/v1"))

    # print(type(redis_aclient.get("test")))

    # print(redis_client.delete("https://api.deepseek.com/v1"))
    feishu_url = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=79272d"
    feishu_url = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=EYgZ8c"

    # with timer():
    #     print(feishu_url in redis_client)
    #
    # with timer():
    #     redis_client.exists(feishu_url)
    # with timer():
    #     print(redis_client.llen(feishu_url))

    # print(redis_client.set('a', 'xx21212'))
    # print(redis_client.set('b', b'xx21212'))
    #
    # print(redis_client.get('a'))
    # print(redis_client.get('b'))

    #
    # print(redis_client.type(feishu))
    # _ = redis_client.lrange(feishu, 0, -1)
    # print(len(eval(_)))

    task_id = "celery-task-meta-ca94c602-a2cc-4db5-afe4-763f30df8a18"


    # arun(redis_aclient.get('celery-task-meta-72d59447-1f88-4727-8067-8244c2268faa'))
    #
    # arun(redis_aclient.select(1))

    # async def main():
    #     r = await redis_aclient.select(1)
    #     return await redis_aclient.get(task_id)
    #
    #
    # arun(main())

    async def main():
        return await redis_aclient.lpop("redis_key")


    # arun(main())

    # r = redis_client.sadd('set1', 'a', 'b', 'c')
    # r = redis_client.sadd('set1', 'd')
    k="meutils.config_utils.lark_utils.commonaget_spreadsheet_values()[(＇feishu_url＇, ＇https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=Gvm9dt＇), (＇to_dataframe＇, True)]	"
    redis_client.delete(k)
