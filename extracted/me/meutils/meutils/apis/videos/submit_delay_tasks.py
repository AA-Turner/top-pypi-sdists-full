#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : run_delay_tasks
# @Time         : 2026/2/16 13:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from meutils.db.redis_db import redis_aclient
from meutils.apis.volcengine_apis import videos_nx

from meutils.apis.oneapi.tasks import get_tasks



async def submit():
    task_ids = await get_tasks(platform="", channel_id="21496", status="UNFINISHED", return_ids=True)
    print(task_ids)
    for task_id in task_ids:
        redis_aclient.get(task_id)

        if request := await videos_nx.Tasks().get(task_id=task_id):
            print(request)
        # 获取结构体
        # 执行异步任务
        # await videos_nx.Tasks().create(task_id=i)
        # await submit_task(task_id=i)

        # 获取response 并写入 redis # 定时调度执行 等等


