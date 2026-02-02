#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : firecrawl
# @Time         : 2024/7/29 10:07
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://www.firecrawl.dev/pricing

from meutils.pipe import *
import requests
import json

url = "https://api.firecrawl.dev/v0/scrape"


async def scrape_url(url):
    payload = {
        "url": "https://mp.weixin.qq.com/s/kFJS7sk66V8Eq0hEwJWw7g",
        "crawlerOptions": {
            "generateImgAltText": False
        },
        "pageOptions": {
            "onlyMainContent": False,
            "removeTags": [
                ""
            ],
            "onlyIncludeTags": [
                ""
            ]
        },
        "origin": "website-preview"
    }
    headers = {
        'authorization': 'Bearer this_is_just_a_preview_token',
    }
    async with httpx.AsyncClient(headers=headers, timeout=60) as client:
        response = await client.post(url=url, json=payload)
        if response.is_success:
            return response.json()


if __name__ == '__main__':
    arun(scrape_url(url))
