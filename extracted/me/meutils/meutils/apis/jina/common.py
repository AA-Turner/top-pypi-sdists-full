#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2025/3/17 18:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from httpx import AsyncClient

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.caches import cache, rcache


@retrying()
@rcache(ttl=600)
async def _url_reader(url: str):
    """markdown"""

    async with AsyncClient(base_url="https://r.jina.ai", headers={}, timeout=300) as client:
        response = await client.get(f"/{url}")
        response.raise_for_status()

        return response.text


async def url_reader(urls: Union[str, List[str]]):
    if isinstance(urls, str):
        return await _url_reader(urls)

    tasks = [_url_reader(url) for url in urls]
    return await asyncio.gather(*tasks)


if __name__ == '__main__':
    url = "https://top.baidu.com/board?tab=realtime"
    url = "https://mp.weixin.qq.com/s/qvR1KbYVOq7XQO1tmEMVJA"

    # print(arun(url_reader(url)))

    print(arun(url_reader([url])))
