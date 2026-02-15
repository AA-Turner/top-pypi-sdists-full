#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ip
# @Time         : 2026/2/6 15:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from openai import AsyncClient, Client

BASE_URL = "http://myip.ipip.net"
# curl cip.cc

base_urls = [
    "http://myip.ipip.net",
    # "https://cip.cc" todo 备用
]


async def aget_myip():
    try:
        for base_url in base_urls:
            client = AsyncClient(base_url=base_url)
            response = await client.get("/", cast_to=object)
            logger.debug(response)
            logger.debug(base_url)

            if "中国" in response:
                return True

    except Exception as e:
        logger.error(e)


@lru_cache()
def get_myip():
    try:
        for base_url in base_urls:
            client = Client(base_url=base_url)
            response = client.get("/", cast_to=object)
            logger.debug(response)

            if "中国" in response: #  and "南京" not in response
                return True

    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    # arun(aget_myip())
    get_myip()
