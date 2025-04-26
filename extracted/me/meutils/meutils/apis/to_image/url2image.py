#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : url2image
# @Time         : 2024/9/19 08:51
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

BASE_URL = 'https://url2pic.php127.com'


async def url2image(url, width: int = 1440, type: str = 'jpg'):
    """

    :param url: str or list
    :param width: 640 1080 1440
    :param type: 输出格式 jpg|png|svg|bmp|pdf 默认jpg
    :return:
    """

    payload = {
        'url': url,
        'width': width,
        'type': type,
        'key': 'u2p66eb73ff63b0266eb73ff63b03632',  # todo: 多key轮询

    }
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=60) as client:
        response = await client.post('/api/url2pic', json=payload)
        if response.is_success:
            return response.json()


if __name__ == '__main__':
    url = 'https://www.baidu.com'

    arun(url2image(url, 640))
