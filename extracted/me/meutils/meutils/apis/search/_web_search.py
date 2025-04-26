#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : zhipu
# @Time         : 2025/2/19 20:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.str_utils.json_utils import json_path
from meutils.llm.clients import zhipuai_sdk_client, zhipuai_client

from meutils.llm.openai_utils import to_openai_params
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, \
    ChatCompletionRequest


class Completions(object):

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def create(self, request: ChatCompletionRequest, search_result2md: bool = False):
        pass

    # async def _create(self, request: ChatCompletionRequest, search_result2md: bool = False):
    #     request.stream = False
    #     request.model = "web-search-pro"
    #     request.messages = [{
    #         "role": "user",
    #         "content": request.last_content,
    #     }]
    #     data = to_openai_params(request)
    #
    #     search_completion = await zhipuai_client.chat.completions.create(**data)
    #     logger.debug(search_completion.model_dump_json(indent=4))
    #
    #     if results := json_path(search_completion, '$..[keywords,query,search_result]'):
    #         data = dict(zip(["keywords", "query", "search_result"], results))
    #         if search_result2md:
    #             global df
    #
    #             df = pd.DataFrame(data["search_result"])
    #
    #             df['title'] = [f"[{k}]({v})" for k, v in zip(df['title'], df['link'])]
    #             df['media'] = [f"![{k}]({v})" for k, v in zip(df['media'], df['icon'])]
    #
    #             df = df[['title', 'media']]
    #             df.index += 1
    #             # {df_.to_markdown(index=False).replace('|:-', '|-').replace('-:|', '-|')}
    #             data["search_result"] = df.to_markdown()
    #         return data

    async def search(self, q: str):
        zhipuai_sdk_client.assistant.conversation(
            model="web-search-pro",
        )

        # {
        #     "role": "user",
        #     "content": search_completion.model_dump_json(indent=4),
        # }


if __name__ == '__main__':
    model = "web-search-pro"
    # model = "tencent-search"

    request = ChatCompletionRequest(
        # model="baichuan4-turbo",
        # model="xx",
        # model="deepseek-r1",
        # model="deepseek-r1:1.5b",
        model=model,

        # model="moonshot-v1-8k",
        # model="doubao",

        messages=[
            {"role": "user", "content": "《哪吒之魔童闹海》现在的票房是多少"}
        ],

        stream=True
    )
    arun(Completions().create(request, search_result2md=True))
