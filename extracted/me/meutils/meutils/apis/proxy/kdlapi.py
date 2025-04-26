#!/usr/bin/env Python
# -*- coding: utf-8 -*-

from meutils.pipe import *
from meutils.caches import rcache
from meutils.decorators.retry import retrying

username = "d1999983904"  # 包月
password = "1h29rymg"


@rcache(ttl=60 - 50)
@retrying()
async def get_proxy_list():
    secret_id = os.getenv("KDLAPI_SECRET_ID") or "owklc8tk3ypo00ohu80o"
    signature = os.getenv("KDLAPI_SIGNATURE") or "8gqqy7w64g7uunseaz9tcae7h8saa24p"
    url = f"https://dps.kdlapi.com/api/getdps/?secret_id={secret_id}&signature={signature}&num=1&pt=1&format=json&sep=1"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        proxy_list = response.json().get('data').get('proxy_list')

        return [f"http://{username}:{password}@{proxy}" for proxy in proxy_list]


async def get_one_proxy():
    proxy_list = await get_proxy_list()
    return proxy_list[-1]


if __name__ == '__main__':
    # arun(get_proxy_list())

    page_url = "https://icanhazip.com/"  # 要访问的目标网页
    # page_url = "https://httpbin.org/ip"


    async def fetch(url):
        # proxy = await get_one_proxy()
        proxy = "http://154.9.253.9:38443"
        # proxy="https://tinyproxy.chatfire.cn"
        # proxy="https://pp.chatfire.cn"
        proxy="http://110.42.51.201:38443"
        proxy="http://110.42.51.223:38443"
        proxy = "http://110.42.51.223:38443"

        # proxy=None
        proxy="https://npjdodcrxljt.ap-northeast-1.clawcloudrun.com"

        async with httpx.AsyncClient(proxy=proxy, timeout=30) as client:
            resp = await client.get(url)
            logger.debug((f"status_code: {resp.status_code}, content: {resp.text}"))

    def run():
        loop = asyncio.get_event_loop()
        # 异步发出5次请求
        tasks = [fetch(page_url) for _ in range(3)]
        loop.run_until_complete(asyncio.wait(tasks))


    run()
