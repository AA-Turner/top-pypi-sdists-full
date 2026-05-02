# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2022/8/8 0008 13:32
import json
from funboost.consumers.base_consumer import AbstractConsumer
from funboost.utils import RedisMixin


class RedisConsumer(AbstractConsumer, RedisMixin):
    """
    redis作为中间件实现的。
    """
    BROKER_KIND = 2
    BROKER_EXCLUSIVE_CONFIG_KEYS = ['redis_host']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_host = self.broker_exclusive_config.get("redis_host")
    def _shedual_task(self):
        while True:
            result = self.redis_db_frame.blpop(self._queue_name,timeout=60)
            if result:
                self._print_message_get_from_broker('redis',result[1].decode())
                task_dict = json.loads(result[1])
                kw = {'body': task_dict}
                self._submit_task(kw)

    def _confirm_consume(self, kw):
        pass  # redis没有确认消费的功能。

    def _requeue(self, kw):
        self.redis_db_frame.rpush(self._queue_name, json.dumps(kw['body']))


