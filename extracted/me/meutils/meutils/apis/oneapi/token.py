#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : token
# @Time         : 2024/7/19 13:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 优化扣费逻辑
import asyncio

from meutils.pipe import *
from meutils.schemas.oneapi import BASE_URL


@alru_cache(ttl=30)
async def get_api_key_money(api_key):
    headers = {
        'authorization': f'Bearer {api_key}'
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        tasks = [
            client.get("/v1/dashboard/billing/usage"),
            client.get("/v1/dashboard/billing/subscription")  # 查令牌
        ]
        response1, response2 = await asyncio.gather(*tasks)
        logger.debug(response1.status_code)
        logger.debug(response1.json())
        logger.debug(response2.status_code)
        logger.debug(response2.json())
        # {'error': {'message': '该令牌状态不可用 (request id: 20241029105800334407026WGK1hBhC)','type': 'new_api_error'}}

        # {"object":"list","total_usage":13665.746200000001}
        # {"object":"billing_subscription","has_payment_method":true,"soft_limit_usd":2000,"hard_limit_usd":2000,"system_hard_limit_usd":2000,"access_until":0}

        response1.raise_for_status()
        response2.raise_for_status()

        total_usage = response1.json()['total_usage'] / 100
        hard_limit_usd = response2.json()['hard_limit_usd']
        return hard_limit_usd - total_usage


if __name__ == '__main__':
    arun(get_api_key_money(os.getenv("OPENAI_API_KEY_GUOCHAN")))

