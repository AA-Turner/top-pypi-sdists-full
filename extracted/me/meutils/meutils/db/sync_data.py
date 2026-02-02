#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : to_db
# @Time         : 2025/8/26 17:08
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json

from meutils.pipe import *
from meutils.db.redis_db import redis_client
import os
from redis import Redis, ConnectionPool
from redis.asyncio import Redis as AsyncRedis, ConnectionPool as AsyncConnectionPool

# kwargs = {
#     "retry_on_timeout": True,
#     # "db": 6
# }
# REDIS_URL="redis://:chatfirechatfire@110.sdsd.51.201:6379" # 'redis://localhost:10/1?pool_max_size=1'
#     # logger.debug(REDIS_URL)
#
# pool = ConnectionPool.from_url(REDIS_URL, **kwargs)
# redis_client_main = Redis.from_pool(pool)

data = json.loads(open('FeHelper-20250826164705.json').read())





ids = list(set([item['task_id'] for item in data['data']['items']]))

#
#
# for id in ids:
#     if v := redis_client.get(id):
#         redis_client_main.set(id, v)
#
#
# redis_client_main.get("cgt-20250826155618-nrzxm")


