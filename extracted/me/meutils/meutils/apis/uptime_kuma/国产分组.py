#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 国产分组
# @Time         : 2024/11/26 16:09
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from meutils.schemas.openai_types import ChatCompletionRequest

from uptime_kuma_api import UptimeKumaApi, MonitorType

PAGE_NAME = "国产模型监控"
API_KEY = "sk-9MtwOUKXaAas1i0r3KNnsxBNKIrtQ07fY4hTbKso0ud6TY8j"
with UptimeKumaApi('https://status.chatfire.cn/') as api:
    _ = api.login('chatfire', 'chatfirechatfire!')

    # api.edit_monitor
    # print(api.get_monitors())
    #
    # api.delete_monitor(21)


    model = "doubao-pro-128k"
    model = "glm-4"

    result = api.add_monitor(
        type=MonitorType.HTTP,
        interval=5 * 60,  # 检测频率

        description=PAGE_NAME,
        name=model,

        method="POST",
        url="https://api.chatfire.cn/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        body={
            "model": model,
            "messages": [{"role": "user", "content": "hi"}],
            "max_tokens": 1
        },
    )

    # api.add_status_page(title=PAGE_NAME, slug=PAGE_NAME)
    # print(api.get_status_page('guochan'))

    api.save_status_page(
        slug="guochan",

        id=PAGE_NAME,
        title=PAGE_NAME,

        publicGroupList=[
            {
                'name': PAGE_NAME,
                'weight': 1,
                'monitorList': [
                    {
                        "id": result.get('monitorID')
                    }
                ]
            }
        ]
    )
