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

from meutils.caches.redis_cache import cache, cache_inmemory
from meutils.db.orm import select_first, update_or_insert
from meutils.schemas.db.oneapi_types import OneapiTask, OneapiUser, OneapiToken


@cache(ttl=15 * 24 * 3600)
async def token2user(api_key: str):
    filter_kwargs = {
        "key": api_key.removeprefix("sk-"),
    }
    # logger.debug(filter_kwargs)
    return await select_first(OneapiToken, filter_kwargs)


@alru_cache(ttl=60)
async def get_user_quota(api_key: Optional[str] = None, user_id: Optional[int] = None):
    assert any([api_key, user_id]), "api_key or user_id must be provided."

    if not user_id:
        token_object = await token2user(api_key)
        user_id = token_object.user_id

    filter_kwargs = {
        "id": user_id
    }
    user_object = await select_first(OneapiUser, filter_kwargs)
    # logger.debug(user_object)
    return user_object.quota / 500000


if __name__ == '__main__':
    # from faker import Faker

    # with timer():
    #     arun(get_user_quota(os.getenv("OPENAI_API_KEY")))
    # arun(get_user_quota(user_id=1))

    async def task():
        filter_kwargs = dict(
            username=f"{shortuuid.random(length=6)}@chatfire.com",
        )
        return await update_or_insert(OneapiUser, filter_kwargs)


    async def main():
        await asyncio.gather(*[task() for _ in range(5000)])


    arun(main())
