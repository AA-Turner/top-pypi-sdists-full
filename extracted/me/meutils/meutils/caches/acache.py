#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : acache
# @Time         : 2025/1/14 09:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from meutils.caches import cache, rcache

from aiocache import cached, Cache, RedisCache, caches
from aiocache import multi_cached
from meutils.schemas.image_types import ImageRequest

# logger.debug(async_pool.connection_kwargs)

REDIS_URL = "redis://:chatfirechatfire@110.42.51.143:6379"


@cached(ttl=60)
@cached(ttl=60)
async def cached_fc(user_id, **kwargs):
    logger.debug(user_id)
    return False


# global x
#
# key_builder = lambda *args, **kwargs: "key"
# key_builder = lambda *args, **kwargs: args[0].prompt
key_builder = lambda *args, **kwargs: args[1].prompt


def key_builder(*args, **kwargs):
    print(args)
    return args[1].prompt


@rcache(ttl=11, key_builder=key_builder)
async def redis_fcc(user_id, **kwargs):
    logger.debug(user_id)
    # 1 / 0
    return False


skip_cache_func = lambda x: False


# def key_builder(*args, **kwargs):
#     len(str(args[1]))

def skip_cache_func(*args, **kwargs):
    logger.debug(f"skip_cache_func: {args} {kwargs}")  # todo:缓存下载文件
    return False
    logger.debug(x)


@rcache(ttl=30, skip_cache_func=skip_cache_func)
async def skip_cache_fccc(*args, **kwargs):
    logger.debug(f"第一次调用：{args} {kwargs}")

    return  # 没缓存
    # return False # 缓存
    # return True # 缓存
    # return 'xxxxxxx' # 缓存


# @multi_cached(ttl=60) # 多key缓存
# async def complex_function(user_id, **kwargs):
#     logger.debug(user_id)
#     return False


# Cache.MEMORY

# Cache.REDIS
# mcache = cached(ttl=60, cache=Cache.REDIS)(cached)
# from aiocache import Cache
#
# Cache(Cache.REDIS)
#
# rcache = Cache.from_url("redis://:chatfirechatfire@110.42.51.201:6379/11")
# print(rcache)


# @cached(ttl=60)
# @cached(ttl=15, cache=rcache)
# async def complex_function(user_id, **kwargs):
#     logger.debug(user_id)
#     return False
#

class A(BaseModel):
    a: Any = 111


import asyncio
from aiocache import cached
from aiocache.backends.redis import RedisCache
from aiocache.serializers import PickleSerializer


# 使用 @cached 装饰器缓存函数结果
@cached(cache=RedisCache, endpoint="127.0.0.1", port=6379, namespace="main",
        # serializer=PickleSerializer(),
        key="my_key", ttl=60)
async def expensive_operation():
    print("Performing expensive operation...")
    await asyncio.sleep(2)  # 模拟耗时操作
    return {"result": "data"}


if __name__ == '__main__':

    from aiocache import cached, Cache, RedisCache, caches

    fn = skip_cache_fccc


    async def main(fn):
        for i in range(3):
            _ = await fn(i)
            # logger.debug(f"第{i}次: {_}")


    arun(main(fn))
