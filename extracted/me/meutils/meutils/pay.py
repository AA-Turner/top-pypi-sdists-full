#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : pay
# @Time         : 2024/4/29 16:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *



headers = {
    "Cookie": os.getenv("PAY_COOKIE"),
    "Content-Type": "application/x-www-form-urlencoded"
}

payload = {
    # "sitename": "",
    "trade_no": 2024042915220175845,
}

# print(httpx.post("https://zf.96ym.cn/User/Order/Callback", headers=headers, data=payload).text)


# df = pd.read_html("https://zf.96ym.cn/User/Order/Index", storage_options=headers)[0]
# df = df.query(f"`状态`!='已完成' and `商品名称`!='测试通道' and `创建时间 支付时间`>'{str(datetime.datetime.now())[:10]} 00:00:00'")
#
# print(df)

# """
# import httpx; httpx.post("https://zf.96ym.cn/User/Order/Callback", headers=headers, data=payload).text
#
# """

