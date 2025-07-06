#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kling
# @Time         : 2024/11/28 16:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.async_utils import async_to_sync_pro
from meutils.async_task import worker, shared_task


class Request(BaseModel):
    method: str = "GET"
    url: str = "https://api.chatfire.cn/"

    class Config:
        frozen = True


@shared_task
def do_sync_task(sleep=10, **kwargs):
    logger.debug("同步任务")
    time.sleep(sleep)

    return kwargs


# AttributeError: 'AsyncToSync' object has no attribute '__name__'. Did you mean: '__ne__'?


@alru_cache()
async def create_task(request: Request, **kwargs):
    logger.debug(request)
    await asyncio.sleep(10)
    return request


worker.task()


@shared_task(pydantic=True)
@async_to_sync_pro
async def ado_pydantic_task(request: Request):
    logger.debug("同步任务+协程+结构体+缓存")
    logger.debug(request)
    if isinstance(request, dict):
        request = Request(**request)

    return await create_task(request)


@worker.task(pydantic=True)
@async_to_sync_pro
async def ado_pydantic_task_2(request: Request):
    logger.debug("同步任务+协程+结构体+缓存")
    logger.debug(request)

    return await create_task(request)


@shared_task(pydantic=True)
def do_pydantic_task(request: Request) -> Request:
    logger.debug(request)
    return request


@shared_task(retry_kwargs={'max_retries': 10})
def do_task_retry(*args, **kwargs):
    logger.debug("do_task_retry")

    return 1 / 0


@shared_task(
    default_retry_delay=3,
    retry_backoff=True,
    retry_kwargs={'max_retries': 10}
)
def do_task_retry_backoff_noautoretry(*args, **kwargs):
    logger.debug("do_task_retry_backoff")

    return 1 / 0


@shared_task(
    autoretry_for=(Exception,),
    default_retry_delay=3,
    retry_backoff=True,
    retry_kwargs={'max_retries': 10}
)
def do_task_retry_backoff(*args, **kwargs):
    logger.debug("do_task_retry_backoff autoretry")

    return 1 / 0


@shared_task(retry_kwargs={'max_retries': 3})
@retrying(10)
def do_task_retrying(*args, **kwargs):
    logger.debug("do_task_retrying")
    return 1 / 0


@shared_task
@retrying(3)
def proxy_task(**kwargs):
    method = kwargs.pop('method', '')
    url = kwargs.pop('url', '')

    logger.debug(kwargs)

    response = requests.request(method, url, **kwargs).json()

    return response


if __name__ == '__main__':
    # print(do_sync_task.apply_async(kwargs={'a': 1, 'b': 2}))
    print(AsyncToSync)
