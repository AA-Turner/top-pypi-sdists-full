# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2022/8/8 0008 13:32
# import time
import time

import orjson

from funboost.consumers.base_consumer import AbstractConsumer
from funboost.utils import RedisMixin


class RedisConsumer(AbstractConsumer, RedisMixin):
    """
    redis作为中间件实现的，使用redis list 结构实现的。
    这个如果消费脚本在运行时候随意反复重启或者非正常关闭或者消费宕机，会丢失大批任务。高可靠需要用rabbitmq或者redis_ack_able或者redis_stream的中间件方式。

    这个是复杂版，一次性拉取100个，简单版在 funboost/consumers/redis_consumer_simple.py
    """
    BROKER_KIND = 2
    BROKER_EXCLUSIVE_CONFIG_KEYS = ['redis_bulk_push', 'redis_host', 'prefetch_count']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_host = self.broker_exclusive_config.get("redis_host")

    # noinspection DuplicatedCode
    def _shedual_task000(self):
        while True:
            if result := self.redis_db_frame.blpop(self._queue_name, timeout=60):
                self._print_message_get_from_broker('reids', result[1].decode())
                task_dict = orjson.loads(result[1])
                kw = {'body': task_dict}
                self._submit_task(kw)

    # noinspection DuplicatedCode
    def _shedual_task(self):
        get_msg_batch_size = self.broker_exclusive_config.get('prefetch_count', self._concurrent_num)
        script = self.register_script("""
                    local m = redis.call('LRANGE', KEYS[1], 0, ARGV[1] - 1)
                    redis.call('LTRIM', KEYS[1], ARGV[1], -1)
                    return m""")
        while True:


            task_str_list = script(keys=[self._queue_name], args=[get_msg_batch_size])

            if task_str_list:
                # self._print_message_get_from_broker('redis', task_str_list)
                for task_str in task_str_list:
                    kw = {'body': orjson.loads(task_str)}
                    self._submit_task(kw)
                time.sleep(0.01)
            else:
                result = self.redis_db_frame.lpop(self._queue_name)
                if result:
                    # self._print_message_get_from_broker('redis', result[1].decode())
                    task_dict = orjson.loads(result)
                    kw = {'body': task_dict}
                    self._submit_task(kw)
                time.sleep(0.2)
            if self._stop_flag:
                break

    def _confirm_consume(self, kw):
        pass  # redis没有确认消费的功能。

    def _requeue(self, kw):
        self.redis_db_frame.rpush(self._queue_name, orjson.dumps(kw['body'], option=orjson.OPT_NON_STR_KEYS))
