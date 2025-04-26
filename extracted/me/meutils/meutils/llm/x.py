import os

# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2025/1/7 17:31
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.llm.clients import zhipuai_client
from meutils.schemas.openai_types import _ChatCompletion

import requests
import uuid

api_key = os.getenv("ZHIPUAI_API_KEY")

msg = [
    {
        "role": "user",
        "content": "中国队奥运会拿了多少奖牌"
    }
]

tool = "web-search-pro"


async def run_v4_sync():
    url = "https://open.bigmodel.cn/api/paas/v4/tools"
    request_id = str(uuid.uuid4())
    data = {
        "request_id": request_id,
        "tool": tool,
        "stream": False,
        "messages": msg
    }

    # resp = requests.post(
    #     url,
    #     json=data,
    #     headers={'Authorization': api_key},
    #     timeout=300
    # )
    # print(resp.content.decode())

    resp = await zhipuai_client.post(
        "/tools",
        body={
            "request_id": str(uuid.uuid4()),
            "tool": tool,
            "stream": False,
            "messages": msg
        },
        cast_to=object
    )
    return resp


file_object = zhipuai_client.files.create(file=Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/llm/completions/rag/百炼系列手机产品介绍.docx"), purpose="file-extract")



if __name__ == '__main__':
    # r = arun(run_v4_sync())
    # arun(file_object)

    file_id = "1736243045_3771f3dfb394424885f24c3dc0583741"

    file_content = json.loads(zhipuai_client.files.content(file_id=file_id).content)["content"]

    file_content = json.loads(r.content)["content"]
