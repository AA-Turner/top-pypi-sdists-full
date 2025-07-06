#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : polling
# @Time         : 2024/12/26 14:08
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import time

from meutils.pipe import *


def poll(n: int = 30, sleep_fn: Optional[Callable] = None):
    if sleep_fn is None:
        sleep_fn = lambda i: max(n / (i + 1), 1)  # 预估大概 2~3 *n

    def decorator(fn):
        is_coroutine = inspect.iscoroutinefunction(fn)

        @wraps(fn)
        async def wrapper(*args, **kwargs):
            for i in range(n):
                await asyncio.sleep(sleep_fn(i))
                # 根据函数类型选择调用方式
                result = await fn(*args, **kwargs) if is_coroutine else fn(*args, **kwargs)
                if result:  # 跳出
                    return result
            return None

        return wrapper

    return decorator


if __name__ == '__main__':
    @poll(n=5)
    async def check_something():
        # 你的检查逻辑

        logger.debug(time.ctime())
        return {"status": "ok"}


    arun(check_something())
