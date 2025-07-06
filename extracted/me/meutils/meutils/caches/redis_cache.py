#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : redis_cache
# @Time         : 2024/12/6 10:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :  https://hermescache.readthedocs.io/en/latest/
# https://mp.weixin.qq.com/s/-T2UmkinmtQoNQo4DVpnfw


import hermes.backend.redis
import hermes.backend.inprocess

from meutils.db.redis_db import pool

cache = hermes.Hermes(
    backend=hermes.backend.redis.Backend,
    connection_pool=pool
)

cache_inmemory = hermes.Hermes(
    backend=hermes.backend.inprocess.Backend,
)

acache_inmemory = hermes.Hermes(
    backend=hermes.backend.inprocess.AsyncBackend,
)




if __name__ == '__main__':
    from meutils.pipe import *

    @cache(tags=('test',))
    async def foo(a, b):
        time.sleep(3)
        logger.debug('没有缓存')

        return a * b


    # @cache(tags=('test',), key=lambda fn, a, b: f'avg:{a}')  # 这样可以忽略b
    # async def func_ignore(a, b):
    #     await asyncio.sleep(5)
    #     logger.debug('异步函数')
    #     return a, b


    # arun(func_ignore(1, 1))
    # ttl: Optional[int] = None,
    # tags: Sequence[str] = (),
    # key: Optional[Callable] = None,
    # @cache(ttl=100, key=lambda fn, a, b: (a, b))
    # def func(x, y):
    #     logger.debug('xxxxxxx')
    #     return x

    arun(foo(1, 2))