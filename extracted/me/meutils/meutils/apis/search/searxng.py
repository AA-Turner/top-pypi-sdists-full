#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : searxng
# @Time         : 2024/11/6 11:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://docs.searxng.org/dev/search_api.html
import os

from meutils.pipe import *


@alru_cache(ttl=5 * 60)
async def search(
        query: str = "chatfire",
        response_format: str = "json",
        **kwargs):
    """

    :param query:
    :param response_format: json, csv, rss
    :param kwargs:
    :return:
    """
    params = {
        "q": query,

        "format": response_format,

        **kwargs
    }

    async with httpx.AsyncClient(base_url=os.getenv("SEARXNG_BASE_URL"), follow_redirects=True, timeout=15) as client:
        response = await client.get("", params=params)
        response.raise_for_status()
        return response.json()


if __name__ == '__main__':
    arun(search())
