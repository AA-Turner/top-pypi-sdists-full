#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat
# @Time         : 2025/4/10 16:06
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from meutils.io.files_utils import to_base64
from meutils.llm.clients import AsyncOpenAI, zhipuai_client
from meutils.llm.openai_utils import to_openai_params

from meutils.schemas.openai_types import CompletionRequest

from meutils.apis.proxy.kdlapi import get_one_proxy


class Completions(object):

    def __init__(
            self,
            base_url: Optional[str] = None,
            api_key: Optional[str] = None,
            http_client: Optional[httpx.AsyncClient] = None
    ):
        self.base_url = base_url
        self.api_key = api_key

        self.client = AsyncOpenAI(base_url=self.base_url, api_key=self.api_key, http_client=http_client)

    async def create(self, request: CompletionRequest):

        ###########################################################################
        # 开启视觉模型
        if not any(i in request.model for i in ["vl", 'vision']) and (urls := request.last_urls.get("image_url")):
            # logger.debug(request)
            if request.model.startswith(("gemini",)):

                if urls[-1].startswith("http"):
                    base64_list = await to_base64(urls, content_type="image/png")
                else:
                    base64_list = urls  # 仅支持base64 todo: tokens怎么计算的

                request.messages = [
                    {
                        'role': 'user',
                        'content': [
                            {
                                'type': 'text',
                                'text': request.last_user_content
                            },
                            *[
                                {
                                    'type': 'image_url',
                                    'image_url': {
                                        'url': base64_data
                                    }
                                }
                                for base64_data in base64_list
                            ]

                        ]
                    }
                ]
            else:
                request.model = "glm-4v-flash"
                request.max_tokens = None
                self.client = zhipuai_client

        elif "deepseek-r" in request.model:
            request.separate_reasoning = True
        ###########################################################################

        data = to_openai_params(request)
        if 'gemini' in request.model:
            data.pop("seed", None)
            data.pop("presence_penalty", None)
            data.pop("frequency_penalty", None)
            data.pop("extra_body", None)

            if not request.reasoning_effort:  # 默认关闭思考
                data['reasoning_effort'] = "none"

            if "thinking" in request.model:
                data['model'] = data['model'].removesuffix("-thinking")  # 开启思考
                data['reasoning_effort'] = 'low'

        logger.debug(data)
        return await self.client.chat.completions.create(**data)


if __name__ == '__main__':
    # 测试 token 1800

    request = CompletionRequest(
        # model="gemini-2.0-flash",
        model="glm-4-flash",
        # model="deepseek/deepseek-r1-turbo",

        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "你是一个数学助手，擅长解决复杂的数学问题。"
                    }
                ]
            },
            # {"role": "user", "content": "你好"},
            {"role": "user", "content": [
                {
                    "type": "text",
                    "text": "解释下"
                },
                {
                    "image_url": {
                        # "detail": "auto",
                        "url": "https://osshk.share704.com/file/upload/2025/04/14/1911575959253815296.jpg"
                    },
                    "type": "image_url"
                }
            ]}
        ],
        stream=False,
        max_tokens=None,
    )
    # arun(Completions().create(request))
    # d = {
    #     "model": "gemini-2.5-pro-exp-03-25",
    #     "messages": [
    #         {
    #             "content": [
    #                 {
    #                     "text": "The following is an open-ended problem from an International Math competition. Please calculate the answer according to the given requirements and the information provided. Please use LaTeX format to represent the variables and formulas used in the solution process and results. Please end your solution with \"So the final answer is \boxed{multiple answers connected with commas}(unit).\" and give the result explicitly, note that the unit of the answer should not be included in \boxed{}.\nConsider the following system of equations in which all logarithms have base 10:\n\n$$\n\begin{aligned}\n(\log x)(\log y)-3 \log 5 y-\log 8 x & =a \\n(\log y)(\log z)-4 \log 5 y-\log 16 z & =b \\n(\log z)(\log x)-4 \log 8 x-3 \log 625 z & =c\n\end{aligned}\n$$\nIf $a=-4, b=4$, and $c=-18$, solve the system of equations.",
    #                     "type": "text"
    #                 },
    #                 {
    #                     "image_url": {
    #                         "detail": "low",
    #                         "url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCABAAEADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD//2Q=="
    #                     },
    #                     "type": "image_url"
    #                 }
    #             ],
    #             "role": "user"
    #         }
    #     ],
    #     "stream": False,
    #     "top_p": 0.7,
    #     "temperature": 0.7,
    #     "n": 1
    # }

    d = {
        "model": "gemini-2.5-pro-exp-03-25",
        # "model": "gemini-2.5-flash-preview-04-17",
        # "model": "gemini-2.5-pro-exp-03-25-thinking",

        "messages": [
            {
                "content": [
                    {
                        "text": "9个8如何加减乘除运直得到1000",
                        "type": "text"
                    },

                ],
                "role": "user"
            }
        ],
        "stream": False,
        "top_p": 0.7,
        "temperature": 0.7,
        "n": 1,
        "reasoning_effort": None
    }
    api_key = os.getenv("GOOGLE_API_KEY")
    base_url = os.getenv("GOOGLE_BASE_URL")
    arun(Completions(api_key=api_key, base_url=base_url).create(request.construct(**d)))

    # request = CompletionRequest(
    #     # model="gemini-2.0-flash",
    #     # model="glm-4-flash",
    #     model="deepseek/deepseek-r1-turbo",
    #
    #     messages=[
    #
    #         {"role": "user", "content": "你好"},
    #
    #     ],
    #     stream=False,
    #     max_tokens=None,
    # )
    # api_key = "sk_LLktDFVC7GNqcGgVoxO1rA70_YHCM_2vaQz2dfwy9tY"
    # base_url = "https://api.ppinfra.com/v3/openai"
    # arun(Completions(api_key=api_key, base_url=base_url).create(request))
