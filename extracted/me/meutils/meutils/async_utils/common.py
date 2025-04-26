#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/8/25 18:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

import inspect
import asyncio
from typing import Union, Any, Coroutine, AsyncIterator, Iterator, Iterable, AsyncIterable, Optional, Callable

import numpy as np
import pandas as pd
from async_lru import alru_cache
from asgiref.sync import sync_to_async, async_to_sync
from httpx import Client, AsyncClient
from loguru import logger
from pprint import pprint
from aiostream import stream
from functools import wraps


def async_to_sync_pro(func):
    @wraps(func)  # 添加这行来保留原函数的属性
    def wrapper(*args, **kwargs):
        return async_to_sync(func)(*args, **kwargs)

    return wrapper


async def achain(*iterables: Union[Iterator[Any], AsyncIterator[Any]], delay: int = 0) -> AsyncIterator[Any]:
    """
        async def async_generator_1() -> AsyncIterator[str]:
            for i in range(1, 6):
                await asyncio.sleep(1)
                yield f'gen1-{i}'


        async def async_generator_2() -> AsyncIterator[str]:
            for i in range(1, 6):
                await asyncio.sleep(1.5)
                yield f'gen2-{i}'


        async def main():
            async for value in achain(async_generator_1(), async_generator_2()):
                print(value)


        asyncio.run(main())
    :param iterables:
    :return:
    """

    for iterable in iterables or []:

        # logger.debug(f"{iterable}: {type(iterable)}")

        if isinstance(iterable, AsyncIterator):
            async for item in iterable:
                yield item
                delay and await asyncio.sleep(delay)

        else:
            # await asyncio.sleep(0)  # 神奇的代码：不起作用

            for item in iterable or []:
                # logger.debug(item)
                yield item
                await asyncio.sleep(delay)  # 神奇的代码：同步转异步


def arun(awaitable_object: Union[Coroutine, AsyncIterator], debug: bool = True):
    # asyncio.iscoroutine(coroutine)
    # logger.debug(type(awaitable_object))
    # logger.debug(isinstance(awaitable_object, Coroutine))
    # logger.debug(isinstance(awaitable_object, AsyncIterator))
    #
    # logger.debug(inspect.isawaitable(awaitable_object))
    # logger.debug(inspect.isasyncgen(awaitable_object))
    # logger.debug(inspect.isasyncgenfunction(awaitable_object))

    # asyncio.iscoroutine(awaitable_object)
    if inspect.isasyncgen(awaitable_object):
        async def main():
            async for i in awaitable_object:
                print(i, end='')
            # return await stream.list(awaitable_object)

        _awaitable_object = main()
    else:
        _awaitable_object = awaitable_object

    _ = asyncio.run(_awaitable_object, debug=debug)
    if debug:
        isinstance(_, (np.ndarray, pd.Series, pd.DataFrame)) or _ and pprint(_)
    return _


def aclose():
    import nest_asyncio
    nest_asyncio.apply()


close_event_loop = aclose


def async2sync_generator(generator):
    """
    async2sync_generator(generator)  | xprint

        async def async_generator():
            for i in range(10):
                await asyncio.sleep(1)
                yield i

        # 使用同步生成器
        for item in async2sync_generator(range(10)):
            print(item)
    :param generator:
    :return:
    """
    if inspect.isasyncgen(generator):
        # close_event_loop()
        while 1:
            try:
                yield asyncio.run(generator.__anext__())

            except StopAsyncIteration:
                break
    else:
        yield from generator


async def arequest(url, method='get', payload=None, **client_params):
    if payload:
        if method.lower() == 'get':
            payload = {"params": payload}
        else:
            payload = {"json": payload}
    async with AsyncClient(**client_params) as client:
        resp = await client.request(method=method, url=url, **payload)
        return resp


async def poll(fn, n: int = 30, sleep_fn: Optional[Callable] = None):
    if sleep_fn is None:
        sleep_fn = lambda i: max(n / (i + 1), 1)  # 预估大概 2~3 *n

    for i in range(n):
        await asyncio.sleep(sleep_fn(i))
        if _ := await fn():  # 跳出
            return _


if __name__ == '__main__':
    from meutils.pipe import *


    # async def async_generator():
    #     for i in range(10):
    #         await asyncio.sleep(1)
    #         yield i
    #
    #
    # async_generator() | xprint

    # async def async_generator_1() -> AsyncIterator[str]:
    #     for i in range(1, 6):
    #         await asyncio.sleep(1)
    #         yield f'gen1-{i}'
    #
    #
    # def async_generator_2():
    #     for i in range(1, 6):
    #         yield f'gen2-{i}'
    #
    #
    # async def main():
    #     async for value in achain(async_generator_1(), async_generator_2()):
    #         print(value)
    #
    #
    # asyncio.run(main())

    async def main():
        async for value in achain():
            print(value)


    asyncio.run(main())
