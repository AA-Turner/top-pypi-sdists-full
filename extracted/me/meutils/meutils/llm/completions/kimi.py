#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kimi
# @Time         : 2024/12/9 13:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import requests
import json

url = "https://kimi.moonshot.cn/api/chat/ctb5lpaflk1f1dda5mv0/completion/stream"

payload = json.dumps({
    "messages": [
        {
            "role": "user",
            "content": "hi"
        }
    ],
    "use_search": False,
    "extend": {
        "sidebar": True
    },
    "kimiplus_id": "kimi",
    "use_research": False,
    "use_math": False,
    "refs": [],
    "refs_file": []
})
headers = {
    'x-msh-session-id': '1729958401005741781',
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTY4NDk3NywiaWF0IjoxNzMxOTA4OTc3LCJqdGkiOiJjc3RkYXNmZDBwODBpaGtkNTY4ZyIsInR5cCI6ImFjY2VzcyIsImFwcF9pZCI6ImtpbWkiLCJzdWIiOiJja2kwOTRiM2Flc2xnbGo2Zm8zMCIsInNwYWNlX2lkIjoiY2tpMDk0YjNhZXNsZ2xqNmZvMmciLCJhYnN0cmFjdF91c2VyX2lkIjoiY2tpMDk0YjNhZXNsZ2xqNmZvMzAifQ.uhEQ3sB6SJLR_Duuu4w-WilRsvllI611flQ_uQoI5ufm_GWtLLJfHZ8rE9-RS2YtkprtYovvEf1U1E6ybcL1Jg',
    'x-msh-platform': 'web',
    'x-msh-device-id': '7311290930975344143',
    'R-Timezone': 'Asia/Shanghai',
    'X-Traffic-Id': 'cki094b3aeslglj6fo30',
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
