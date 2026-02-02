#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/12/25 18:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI
from meutils.caches import rcache
from meutils.db.orm import select_first, update_or_insert
from meutils.schemas.db.oneapi_types import OneapiTask, OneapiUser, OneapiToken
from meutils.apis.oneapi.channel import get_channel_keys


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


async def polling_keys(biz: str, api_key: Optional[str] = None, batch_size: int = 1,
                       channel_id: Optional[int] = None):  # 轮询
    # all
    if channel_id:
        df = await get_channel_keys(channel_id, base_url='https://api.chatfire.cn')
        return df['key_preview'].to_list()  # 渠道所有 keys

    if batch_size > 1:
        tasks = [polling_keys(biz, api_key) for _ in range(batch_size)]
        api_keys = await asyncio.gather(*tasks)
        return api_keys

    # "biz-channel_id" => sk-channel_id

    try:
        client = AsyncOpenAI(
            # base_url="http://0.0.0.0:8000/v1",
            api_key=api_key
        )
        response = await client.audio.speech.create(model=biz, input=biz, voice=biz, extra_query={"biz": biz})
        api_key = response.json().get("api_key")

        # if api_key:
        #     # logger.debug(bjson(response))
        #     logger.debug("获取轮询key成功")

        return api_key
    except Exception as e:
        logger.debug(e)
        return None


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
    arun(polling_keys('volc', batch_size=1))
