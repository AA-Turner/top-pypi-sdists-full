#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/12/25 18:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI
from meutils.caches import rcache
from meutils.decorators.retry import retrying
from meutils.db.orm import select_first, update_or_insert
from meutils.db.redis_db import redis_aclient
from meutils.apis.oneapi.channel import get_channel_keys
from meutils.schemas.task_types import FluxTaskResponse
from meutils.schemas.db.oneapi_types import OneapiTask, OneapiUser, OneapiToken


@rcache(ttl=90 * 24 * 3600)
async def token2user(api_key: str):
    filter_kwargs = {
        "key": api_key.removeprefix("sk-"),
    }
    # logger.debug(filter_kwargs)
    if _ := await select_first(OneapiToken, filter_kwargs):
        return _.dict()


@rcache(ttl=15)
async def get_user_quota(api_key: Optional[str] = None, user_id: Optional[int] = None):
    assert any([api_key, user_id]), "api_key or user_id must be provided."

    if not user_id:
        if token_object := await token2user(api_key):
            token_object = OneapiToken(**token_object)

            user_id = token_object.user_id

    filter_kwargs = {
        "id": user_id
    }
    if user_object := await select_first(OneapiUser, filter_kwargs):
        return user_object.quota / 500000


@retrying()
async def polling_keys(
        biz: str, api_key: Optional[str] = None, batch_size: int = 1,
        channel_id: Optional[int] = None,
        skip_keys: Optional[str] = None
):  # 轮询
    """

    :param biz: model
    :param api_key:
    :param batch_size:
    :param channel_id:
    :return:
    """
    # all
    if channel_id:
        df = await get_channel_keys(channel_id, base_url='http://api.chatfire.cn')
        return df['key_preview'].to_list()  # 渠道所有 keys

    if batch_size > 1:
        tasks = [polling_keys(biz, api_key) for _ in range(batch_size)]
        api_keys = await asyncio.gather(*tasks)
        return api_keys

    client = AsyncOpenAI(
        # base_url="http://0.0.0.0:8000/v1",
        api_key=api_key
    )

    response = await client.audio.speech.create(model=biz, input=biz, voice=biz, extra_query={"biz": biz})
    response = response.json()
    logger.debug(bjson(response))
    api_key = response.get("api_key")

    return api_key


async def set_async_flux_signal(task_id: str, response: Union[BaseModel, dict]):
    # 异步任务信号 response:{task_id}
    if isinstance(response, BaseModel):
        response = response.model_dump(exclude_none=True)
    flux_task_response = FluxTaskResponse(id=task_id, result=response)
    if flux_task_response.status in {"Ready", "Error", "Content Moderated"}:
        if request_data := await redis_aclient.get(f"request:{task_id}"):
            flux_task_response.details['request'] = json.loads(request_data)

        data = flux_task_response.model_dump_json(exclude_none=True, indent=4)
        await redis_aclient.set(f"response:{task_id}", data, ex=7 * 24 * 3600)
        await redis_aclient.set(f"response-raw:{task_id}", json.dumps(response), ex=7 * 24 * 3600)

        return True  # 任务结束


async def polling_task(get_task: Callable, task_id: str, n: int = 1):  # todo 轮询获取结果，直到成功或失败  解耦出去
    if response := await redis_aclient.get(f"response-raw:{task_id}"):
        return json.loads(response)

    for i in range(n):
        await asyncio.sleep(5)

        logger.debug(f"Polling task {task_id} ... ({i + 1}/{n})")
        try:
            response = await get_task(task_id)
            if await set_async_flux_signal(task_id, response) or n == 1:  # 任务结束
                # break
                return response


        except Exception as e:
            logger.error(f"Get task error: {e}, retrying... ({i + 1}/10)")


if __name__ == '__main__':
    # from faker import Faker

    # with timer():
    #     arun(get_user_quota(os.getenv("OPENAI_API_KEY")))
    # arun(get_user_quota(user_id=1))

    # async def task():
    #     filter_kwargs = dict(
    #         username=f"{shortuuid.random(length=6)}@chatfire.com",
    #     )
    #     return await update_or_insert(OneapiUser, filter_kwargs)
    #
    #
    # async def main():
    #     await asyncio.gather(*[task() for _ in range(5000)])
    #
    #
    # arun(main())

    # arun(get_user_quota("sk-u8QN3zbulUFcCSvI9CIJ87OYsAONEQXGgSyEPyGC0sJhCFFJ"))
    # arun(get_user_quota("sk-x"))
    # arun(token2user("sk-iPNbgHSRkQ9VUb6iAcCa7a4539D74255A6462d29619d65199"))
    # arun(get_user_quota("sk-u8QN3zbulUFcCSvI9CIJ87OYsAONEQXGgSyEPyGC0sJhCFFJ"))
    # arun(polling_key("test"))
    # arun(polling_key('volc'))
    # arun(polling_keys('volc', batch_size=1))
    arun(polling_keys('volc', batch_size=2))
