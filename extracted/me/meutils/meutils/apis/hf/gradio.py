#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : gradio
# @Time         : 2024/9/27 10:25
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.apis.proxy import ips

from gradio_client import Client, handle_file as _handle_file

handle_file = lru_cache()(_handle_file)
@alru_cache()
async def create_client(endpoint, hf_token: Optional[str]=None, with_proxies: bool = False):
    httpx_kwargs = None
    if with_proxies:  # 无法使用
        proxies = await ips.get_proxies()
        httpx_kwargs = {
            "proxies": proxies,
        }

    client = Client(
        endpoint,
        download_files=False,
        httpx_kwargs=httpx_kwargs,
        hf_token=hf_token
    )

    return client
