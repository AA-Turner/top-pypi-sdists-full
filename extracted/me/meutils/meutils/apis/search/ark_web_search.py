#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ark
# @Time         : 2025/4/1 16:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.caches import rcache

from meutils.llm.clients import AsyncClient
from meutils.llm.openai_utils import to_openai_params

from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, ChatCompletionChunk


class Completions(object):

    def __init__(self, api_key: Optional[str] = None):
        self.client = AsyncClient(
            api_key=api_key or os.getenv('ARK_BOTS_API_KEY'),
            base_url="https://ark.cn-beijing.volces.com/api/v3/bots",
        )

    async def create(self, request: CompletionRequest):
        data = to_openai_params(request)
        return await self.client.chat.completions.create(**data)

    @rcache(noself=True, ttl=15 * 60)
    async def query(self, q: str):
        request = CompletionRequest(
            model="bot-20250401164325-s7945",  # todo

            messages=[
                {"role": "user", "content": q},
            ],
            temperature=0,
            max_tokens=10,
            stream=False,
        )
        completion = await self.create(request)
        logger.debug(completion)
        # print(completion.choices[0].message.content)

        data = {"data": []}
        if hasattr(completion, "references"):
            data['data'] = completion.references

        return data


if __name__ == '__main__':
    c = Completions(api_key=os.getenv('ARK_BOTS_API_KEY'))
    # s = c.create(CompletionRequest(
    #     model="bot-20250401164325-s7945",
    #     messages=[
    #         {"role": "user", "content": "今天南京天气如何？"},
    #     ],
    #     stream=True,
    # ))
    q = "今天有什么热点新闻？"
    q = "今日热点"

    # arun(c.query("今天南京天气如何？"))

    arun(c.query(q=q))
