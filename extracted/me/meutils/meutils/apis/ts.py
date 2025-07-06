#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ts
# @Time         : 2024/4/29 10:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : translators
import os

import httpx

from meutils.pipe import *

import translators as ts

print(ts.translators_pool)

'niutrans'

# r = ts.translate_text(
#     query_text='你好',
#     translator='niutrans',
#     to_language='en',
#     apikey='f77c833dc48cf93e1e85bea2d6f17459'
#     # **kwargs: ApiKwargsType,
# )


if __name__ == '__main__':
    headers = {
        "Cookie": os.getenv("PAY_COOKIE"),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        # "sitename": "",
        "trade_no": 2024042915220175845,
    }

    # print(httpx.post("https://zf.96ym.cn/User/Order/Callback", headers=headers, data=payload).text)
    # html = httpx.get("https://zf.96ym.cn/User/Order/Index", headers=headers).text
    # # print(html)
    #
    # print(pd.read_html(html)[0].query("状态!='已完成' and 商品名称!='测试通道'"))

    df = pd.read_html("https://zf.96ym.cn/User/Order/Index", storage_options=headers)[0]
    df = df.query(f"`状态`!='已完成' and `商品名称`!='测试通道' and `创建时间 支付时间`>'{str(datetime.datetime.now())[:10]} 00:00:00'")

    print(df)

    # """
    # import httpx; httpx.post("https://zf.96ym.cn/User/Order/Callback", headers=headers, data=payload).text
    #
    # """




