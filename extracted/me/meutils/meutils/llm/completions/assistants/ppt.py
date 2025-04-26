#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ppt
# @Time         : 2025/3/19 09:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.llm.openai_utils import to_openai_params
from meutils.llm.clients import AsyncOpenAI
from meutils.str_utils.regular_expression import parse_url

from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, CompletionUsage


class Completions(object):

    def __init__(self,
                 base_url: Optional[str] = None,
                 api_key: Optional[str] = None
                 ):
        base_url = base_url or "https://all.chatfire.cn/glm/v1"

        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)

    async def create(self, request: CompletionRequest):
        if request.last_user_content.startswith(("http",)):
            file_url, text = request.last_user_content.split(maxsplit=1)

            request.messages = [
                {
                    'role': 'user',
                    'content': [
                        {
                            "type": "text",
                            "text": text
                        },

                        {
                            "type": "file",  # 不标准
                            "file_url": {
                                "url": file_url
                            }
                        }
                    ]
                }
            ]

        logger.debug(request)

        data = to_openai_params(request)
        return await self.client.chat.completions.create(**data)


if __name__ == '__main__':
    data = {
        "model": "65d2f07bb2c10188f885bd89",
        "messages": [
            {
                "role": "user",

                "content": "https://s3.ffire.cc/cdn/20250403/6MxhHmxeX7Z7WYMb8QWqfp_ppt 基于文件做个ppt"
                # "content": [
                #     {
                #         "type": "file",
                #         "file_url": {
                #             "url": "https://mj101-1317487292.cos.ap-shanghai.myqcloud.com/ai/test.pdf"
                #         }
                #     },
                #     {
                #         "type": "text",
                #         # "text": "基于内容写个ppt给我"
                #         "text": "生成PPT"
                #     }
                # ]
            }
        ],
        # "stream": false
    }

    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzNmE4NmM1Yzc2Y2Q0MTcyYTE5NGYxMjQwZTgyMmIwOSIsImV4cCI6MTc1NjExMzEzNywibmJmIjoxNzQwNTYxMTM3LCJpYXQiOjE3NDA1NjExMzcsImp0aSI6IjBhMmFkMDQzNTA1ZDQwOWNiYWJhYTY2NzIwNTgyYWUxIiwidWlkIjoiNjQ0YTNkMGNiYTI1ODVlOTA0NjAzOWRiIiwidHlwZSI6InJlZnJlc2gifQ.gH5iiXhsrI2qpgP_dRobdtoImVhGF7Aby3SKvKIHO0E"

    c = Completions(api_key=api_key)

    request = CompletionRequest(**data)

    arun(c.create(request))
