#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2025/4/15 12:09
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
#!/usr/bin/env Python
# -*- coding: utf-8 -*-

"""
使用requests请求代理服务器
请求http和https网页均适用
"""

import random
import asyncio

import httpx
import requests


# API接口，返回格式为json
api_url = "https://dps.kdlapi.com/api/getdps/?secret_id=ot71jj2r4w9coubcip9o&signature=dldk7s859lixl44qxcg7idw8qocy6hrm&num=1&pt=1&format=json&sep=1"  # API接口


secret_id ="owklc8tk3ypo00ohu80o"
signature = "8gqqy7w64g7uunseaz9tcae7h8saa24p"
api_url = f"https://dps.kdlapi.com/api/getdps/?secret_id={secret_id}&signature={signature}&num=1&pt=1&format=json&sep=1"

# API接口返回的proxy_list
proxy_list = requests.get(api_url).json().get('data').get('proxy_list')

# 用户名密码认证(私密代理/独享代理)
username = "d1999983904"
password = "1h29rymg"


page_url = "http://icanhazip.com/"  # 要访问的目标网页


async def fetch(url):
    proxy = httpx.Proxy(
        url=f"http://{username}:{password}@{random.choice(proxy_list)}",
    )
    async with httpx.AsyncClient(proxy=proxy, timeout=10) as client:
        resp = await client.get(url)
        print(f"status_code: {resp.status_code}, content: {resp.content}")


def run():
    loop = asyncio.get_event_loop()
    # 异步发出5次请求
    tasks = [fetch(page_url) for _ in range(5)]
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    run()