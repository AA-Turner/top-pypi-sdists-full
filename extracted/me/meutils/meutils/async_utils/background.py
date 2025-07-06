#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : background
# @Time         : 2024/6/12 11:00
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.decorators import background_task

from asgiref.sync import async_to_sync
from starlette.background import BackgroundTask as _BackgroundTask, BackgroundTasks as _BackgroundTasks


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

    @background_task
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

    @background_task
    def call(self):
        async_to_sync(super().__call__)()


if __name__ == '__main__':
    from meutils.pipe import *


    async def f(x):
        logger.debug(x)

        for i in range(100):
            logger.debug(i)
            await asyncio.sleep(1)


    bt = BackgroundTasks()
    bt.add_task(f, x='xxxxxxxxxx')
    bt.call()

