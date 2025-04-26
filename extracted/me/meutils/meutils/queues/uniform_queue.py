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
from queue import Queue, Empty


class UniformQueue(object):

    def __init__(self, generator: Generator):
        self.queue = Queue()

        self.producer(generator)

    def smooth(self, interval: float = 0.05, timeout: float = 30, break_fn: Callable = lambda item: item is None):
        return self.consumer(interval, timeout, break_fn)

    def consumer(self, interval: float = 0.066, timeout: float = 10, break_fn: Callable = lambda item: item is None):
        """

        :param interval:
        :param timeout:
        :param break_fn: 默认item为None跳出
            lambda line: line.choices[0].finish_reason == 'stop'
        :return:
        """
        while True:
            try:
                item = self.queue.get(timeout=timeout)
                yield item

                if break_fn(item):  # 跳出队列，很重要：最后一个会被返回【注意None值的处理】
                    break

            except Empty:
                break

            time.sleep(interval)

    @background
    def producer(self, generator):
        for i in generator:
            self.queue.put(i)


if __name__ == '__main__':

    def gen():
        while 1:
            yield '#'


    for i in tqdm(UniformQueue(gen()).consumer(interval=0.1)):
        print(i)
