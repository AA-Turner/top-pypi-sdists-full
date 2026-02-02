#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : products
# @Time         : 2025/8/13 17:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.llm.clients import AsyncClient
"""
product-2c8b72 
4.5v

"""

async def create_pre_order(api_key, product_id: str = "product-2c8b72"):
    payload = {"channelCode": "BALANCE", "isMobile": False, "num": 1, "payPrice": 0, "productId": product_id}
    client = AsyncClient(base_url="https://bigmodel.cn", api_key=api_key)
    response = await client.post("/api/biz/product/createPreOrder", body=payload, cast_to=object)
    return response


if __name__ == '__main__':
    arun(create_pre_order("9df724995f384c2e91d673864d1d32eb.aeLMBoocPyRfGBx8"))


