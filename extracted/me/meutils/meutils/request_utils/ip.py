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

async def aget_myip():
    try:
        client = AsyncClient(base_url=BASE_URL)
        response = await client.get("/", cast_to=object)
        logger.debug(response)

        if "中国" in response:
            return True

    except Exception as e:
        logger.error(e)


def get_myip():
    try:
        client = Client(base_url=BASE_URL)
        response = client.get("/", cast_to=object)
        logger.debug(response)

        if "中国" in response:
            return True

    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    # arun(get_myip())
    get_myip()