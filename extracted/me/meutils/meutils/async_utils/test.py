#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : test
# @Time         : 2024/6/12 10:47
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo； 并没有啥用

from meutils.pipe import *
from starlette.background import BackgroundTask as _BackgroundTask, BackgroundTasks as _BackgroundTasks
from asgiref.sync import sync_to_async, async_to_sync


class BackgroundTask(_BackgroundTask):
    """
    async def f(x):
        for i in range(100):
            logger.debug(i)
            await asyncio.sleep(1)
    BackgroundTask(f, x='xxxxxxxxxx').call()

    bt = BackgroundTasks()
    bt.add_task(f, x='xxxxxxxxxx')
    bt.call()
    """

    def call(self):
        async_to_sync(super().__call__)()


class BackgroundTasks(_BackgroundTasks):
    """
    async def f(x):
        for i in range(100):
            logger.debug(i)
            await asyncio.sleep(1)
    BackgroundTask(f, x='xxxxxxxxxx').call()

    bt = BackgroundTasks()
    bt.add_task(f, x='xxxxxxxxxx')
    bt.call()
    """

    def call(self):
        async_to_sync(super().__call__)()
