#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2024/11/28 15:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from meutils.async_task import worker
from meutils.async_task.tasks import test, kling, hailuo
from celery.result import AsyncResult

# print(worker.conf)

# @shared_task(
#     autoretry_for=(Exception,),      # 自动重试的异常类型
#     retry_kwargs={
#         'max_retries': 3,            # 最大重试次数
#         'countdown': 60              # 重试等待时间（秒）
#     },
#     retry_backoff=True,              # 启用指数退避
#     retry_backoff_max=600,           # 最大退避时间（秒）
#     retry_jitter=True                # 添加随机抖动
# )
# def my_task():
#     try:
#         # 任务逻辑
#         result = some_operation()
#         return result
#     except Exception as exc:
#         logger.error(f"Task failed: {exc}")
#         raise  # 触发自动重试


if __name__ == '__main__':
    # r = test.do_sync_task.apply_async(kwargs={'a': 1, 'b': 2})
    # logger.debug(r.backend)
    # test.ado_sync_task.apply_async(kwargs={'a': 1, 'b': 2})
    # test.ado_sync_task.apply_async(kwargs={'a': 1, 'b': 3})
    # print(AsyncResult("42e191a0-6099-419e-b61d-07bf7e2df2fc").result)
    # result.backend
    # AsyncResult("42e191a0-6099-419e-b61d-07bf7e2df2fc").get()
    # AsyncResult(r.id).result

    # test.do_pydantic_task.apply_async(kwargs={'request': test.Request()})

    # test.do_pydantic_task.apply_async(kwargs={"request": {"method": "POST", "url": "测试"}})

    # print(type(test.do_pydantic_task))

    # test.do_pydantic_task.apply_async(kwargs={"request": {"method": "POST", "url": "测试"}})
    # test.do_pydantic_task.apply_async(kwargs={"request": {"method": "xx"}})
    # test.do_pydantic_task.apply_async(args=({"method": "xxxxxxx"},))

    #
    # test.do_task_retrying.apply_async(kwargs={'name': "###do_task_retrying"})
    # test.do_task_retry.apply_async(kwargs={'name': "###do_task_retry"})
    # test.do_task_retry_backoff.apply_async(kwargs={'name': "###do_task_retry_backoff"})
    # test.ado_pydantic_task.apply_async(kwargs={'name': "###do_task_retry_backoff"})

    test.Request()
    # test.ado_pydantic_task.apply_async(kwargs={"request": None})

    # test.ado_pydantic_task.apply_async(kwargs={"request": test.Request().model_dump()})
    # test.ado_pydantic_task_2.apply_async(kwargs={"request": test.Request().model_dump()})

    # kling.create_task.apply_async(kwargs={"request": kling.kolors_virtual_try_on.TryOnRequest().model_dump()})

    hailuo.create_task.apply_async(kwargs={"request": hailuo.VideoRequest(prompt='a dog').model_dump()})
