#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : xx
# @Time         : 2024/11/15 09:19
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

# ResponseT = TypeVar(
#     "ResponseT",
#     bound=Union[
#         object,
#         str,
#         None,
#         "BaseModel",
#         List[Any],
#         Dict[str, Any],
#         Response,
#         ModelBuilderProtocol,
#         "APIResponse[Any]",
#         "AsyncAPIResponse[Any]",
#         "HttpxBinaryResponseContent",
#     ],
# )

payload = {
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
}

from openai import OpenAI

client = OpenAI(
    base_url="https://kimi.moonshot.cn",
    api_key="eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTY4NDk3NywiaWF0IjoxNzMxOTA4OTc3LCJqdGkiOiJjc3RkYXNmZDBwODBpaGtkNTY4ZyIsInR5cCI6ImFjY2VzcyIsImFwcF9pZCI6ImtpbWkiLCJzdWIiOiJja2kwOTRiM2Flc2xnbGo2Zm8zMCIsInNwYWNlX2lkIjoiY2tpMDk0YjNhZXNsZ2xqNmZvMmciLCJhYnN0cmFjdF91c2VyX2lkIjoiY2tpMDk0YjNhZXNsZ2xqNmZvMzAifQ.uhEQ3sB6SJLR_Duuu4w-WilRsvllI611flQ_uQoI5ufm_GWtLLJfHZ8rE9-RS2YtkprtYovvEf1U1E6ybcL1Jg"
)
# "https://kimi.moonshot.cn/api/chat/ctb5lpaflk1f1dda5mv0/completion/stream"
resp = client.post(
    "/api/chat/ctb5lpaflk1f1dda5mv0/completion/stream",
    cast_to=object,
    body=payload,
    stream=True
)

