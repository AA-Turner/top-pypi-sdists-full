#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : express
# @Time         : 2024/4/24 17:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

@lru_cache
def express_query(express_no=780098068058, path: str = '/kdi', appcode: Optional[str] = None):
    """

    :param appcode:
        appcode = '0ccd86184de94ca19c37cbb215b1f3722'  # 开通服务后 买家中心-查看AppCode

    :param express_no:
    :param path:
    :return:
    """
    base_url = "https://wuliu.market.alicloudapi.com"
    with httpx.Client(base_url=base_url) as client:
        headers = {"Authorization": f'APPCODE {appcode or os.getenv("EXPRESS_APP_CODE")}'}
        params = {'no': express_no}

        response = client.get(path, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}


async def aexpress_query(express_no=780098068058, path: str = '/kdi', appcode: Optional[str] = None):
    """

    :param appcode:
        appcode = '0ccd86184de94ca19c37cbb215b1f372'  # 开通服务后 买家中心-查看AppCode

    :param express_no:
    :param path:
    :return:
    """
    base_url = "https://wuliu.market.alicloudapi.com"
    async with httpx.AsyncClient(base_url=base_url) as client:
        headers = {"Authorization": f'APPCODE {appcode or os.getenv("EXPRESS_APP_CODE")}'}
        params = {'no': express_no}
        response = await client.get(path, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}


if __name__ == '__main__':
    # print(express_query('0ccd86184de94ca19c37cbb215b1f372'))

    print(arun(aexpress_query('0ccd86184de94ca19c37cbb215b1f372')))
