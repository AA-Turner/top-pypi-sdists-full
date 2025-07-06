#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : search_music
# @Time         : 2024/5/10 08:36
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://www.yyssq.cn/

from meutils.pipe import *


def search_music(
        query,
        filter_value="name",
        type_value: str = "netease",
        page_value: int = 1
):
    url = "https://www.yyssq.cn/"
    data = {
        "input": query,
        "filter": filter_value,
        "type": type_value,
        "page": page_value
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = httpx.post(url, data=data, headers=headers)
    if response.status_code != 200: response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    # 搜索
    pprint(search_music("夏天")["data"][:2])
