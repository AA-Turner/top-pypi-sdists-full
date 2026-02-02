#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2024/3/22 15:55
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import asyncio
import random
import time


async def producer(queue: asyncio.Queue, name: str):
    for i in range(10):
        # 模拟数据生成需要的时间
        await asyncio.sleep(random.random())
        item = (name, i)
        # 将数据放入队列
        await queue.put(item)
        print(f'生产者 {name} 生产了 {item}')
    # 生产完毕后发送结束信号
    await queue.put(None)


async def consumer(queue: asyncio.Queue, name: str):
    while True:
        # 从队列中获取数据
        item = await queue.get()
        if item is None:
            # 生产者发送了结束信号，终止循环
            break
        # 模拟数据处理需要的时间
        await asyncio.sleep(random.random())
        print(f'消费者 {name} 消费了 {item}')
        queue.task_done()


async def main():
    queue = asyncio.Queue()

    # 创建生产者和消费者协程
    producers = [producer(queue, f'P{i}') for i in range(2)]  # 两个生产者
    consumers = [consumer(queue, f'C{i}') for i in range(3)]  # 三个消费者

    # 启动所有协程
    await asyncio.gather(*producers, *consumers)

    # 等待队列被处理完毕
    await queue.join()


asyncio.run(main())
