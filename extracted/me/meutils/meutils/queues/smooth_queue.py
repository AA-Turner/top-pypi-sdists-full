#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : uniform_queue
# @Time         : 2023/12/6 17:59
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import time

from meutils.pipe import *


class SmoothQueue(object):
    def __init__(self, end=None):
        self.queue = asyncio.Queue()
        self.end = end

    async def producer(self, generator):  # 生产者将任务放入队列
        if inspect.isasyncgen(generator) or hasattr(generator, '__anext__'):  # if hasattr(future, '__anext__'):
            async for i in generator:
                await self.queue.put(i)
        else:
            for i in generator:
                await self.queue.put(i)

        # 生产结束
        await self.queue.put(self.end)  # 使用 None 作为生产结束的标志

    async def consumer(self, generator, delay: float = 1, debug: bool = False):
        producer_task = asyncio.create_task(self.producer(generator))  # 是否合理？

        for i in range(100000):
            item = await self.queue.get()  # await asyncio.wait_for(self.queue.get(), timeout=2)

            if debug: logger.debug(item)

            if item == self.end: break  # 生产者已经结束生产

            yield item  # 不包含【结束值】

            # 生成器等待，模拟处理速度，这里处理速度是均匀的
            if i > 5: await asyncio.sleep(delay)  # 调整此处的等待时间来控制消费的速度

        await producer_task

    async def main(self, generator):
        producer_task = asyncio.create_task(self.producer(generator))

        async for item in self.consumer(generator):
            print(f'Consumed {item}')

        await producer_task


if __name__ == '__main__':
    async def gen():
        await asyncio.sleep(10)
        for i in range(10):
            logger.debug(time.ctime())
            # 模拟不均匀的生产速度
            await asyncio.sleep(random.random())
            print(f'{time.ctime()}: Produced {i}')
            yield i


    sq = SmoothQueue()


    async def main():
        iters = sq.consumer(gen(), delay=2)
        for i in range(10):
            await asyncio.sleep(1)
            logger.debug(f"{time.ctime()}: {i}")

        async for item in iters:
            print(f'Consumed {item}')

        # await producer_task


    arun(main())

    # import asyncio
    # import random
    #
    #
    # async def producer(queue):
    #     for i in range(10):
    #         # 模拟不均匀的生产速度
    #         await asyncio.sleep(random.random())
    #         await queue.put(i)
    #         print(f'Produced {i}')
    #     # 生产结束
    #     await queue.put(None)  # 使用 None 作为生产结束的标志
    #
    #
    # async def consumer(queue):
    #     while True:
    #         item = await queue.get()
    #         if item is None:
    #             # 生产者已经结束生产
    #             break
    #         # 生成器等待，模拟处理速度，这里处理速度是均匀的
    #         await asyncio.sleep(1)  # 调整此处的等待时间来控制消费的速度
    #         yield item
    #
    #
    # async def main():
    #     queue = asyncio.Queue()
    #     producer_task = asyncio.create_task(producer(queue))
    #
    #     async for item in consumer(queue):
    #         print(f'Consumed {item}')
    #
    #     await producer_task
    #
    #
    # asyncio.run(main())
