#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : search
# @Time         : 2025/1/27 13:41
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 格式匹配
# https://github.com/deepseek-ai/DeepSeek-R1

from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI, chatfire_client, zhipuai_client, moonshot_client
from meutils.llm.openai_utils import to_openai_params
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, ChatCompletionRequest, CompletionUsage


class Completions(object):

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def create(self, request: ChatCompletionRequest):
        request.model = request.model.removesuffix("-search")

        if request.model.startswith("baichuan"):
            base_url = os.getenv("BAICHUAN_BASE_URL")
            api_key = self.api_key or os.getenv("BAICHUAN_API_KEY")

            request.tools = [
                {
                    "type": "web_search",
                    "web_search": {
                        "enable": True,
                        "search_mode": "performance_first"
                    }
                }
            ]
            data = to_openai_params(request)
            client = AsyncOpenAI(base_url=base_url, api_key=api_key)
            completion = await client.chat.completions.create(**data)
            return completion

        elif request.model.startswith(("moonshot", "kimi")):
            tool_call_name = "$web_search"
            request.tools = [
                {
                    "type": "builtin_function",  # <-- 我们使用 builtin_function 来表示 Kimi 内置工具，也用于区分普通 function
                    "function": {
                        "name": "$web_search",
                    },
                },
            ]

            data = to_openai_params(request)
            completion = await moonshot_client.chat.completions.create(**data)

            tool_call = completion.choices[0].message.tool_calls[0]
            tool_call_arguments = tool_call.function.arguments
            print(tool_call_arguments)

            request.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call_name,
                "content": tool_call_arguments,
            })
            logger.debug(request.messages)
            data = to_openai_params(request)
            logger.debug(data)
            completion = await moonshot_client.chat.completions.create(**data)
            return completion

        elif request.model.startswith("doubao"):
            base_url = os.getenv("DOUBAO_BASE_URL")
            api_key = self.api_key or os.getenv("DOUBAO_API_KEY")

            request.model = "bot-20250127143547-c8q8m"
            request.tools = [
                {
                    "type": "web_search",
                    "web_search": {
                        "enable": True,
                        "search_mode": "performance_first"
                    }
                }
            ]
            data = to_openai_params(request)
            client = AsyncOpenAI(base_url=base_url, api_key=api_key)

            completion = await client.chat.completions.create(**data)
            return completion

        elif request.model.startswith("search"):  # 智谱
            data = to_openai_params(request)

            search_completion = await zhipuai_client.chat.completions.create(**data)
            search_completion.model_dump_json(indent=4)


        else:
            # 搜索
            data = to_openai_params(request)
            data['model'] = "web-search-pro"
            data['stream'] = False
            search_completion = await zhipuai_client.chat.completions.create(**data)
            logger.debug(search_completion.model_dump_json(indent=4))  # todo: 返回详细信息
            # todo: chat搜索接口 搜索内容重排序 搜索聚合

            # 大模型
            request.messages.append(
                {
                    "role": "user",
                    "content": search_completion.model_dump_json(indent=4),
                }
            )

            data = to_openai_params(request)
            completion = await chatfire_client.chat.completions.create(**data)
            return completion


if __name__ == '__main__':
    request = ChatCompletionRequest(
        # model="baichuan4-turbo",
        # model="xx",
        # model="deepseek-r1",
        # model="deepseek-r1:1.5b",
        model="deepseek-r1:32b",

        # model="moonshot-v1-8k",
        # model="doubao",

        messages=[
            {"role": "user", "content": "《哪吒之魔童闹海》现在的票房是多少"}
        ],

        stream=False
    )

    arun(Completions().create(request))

    # async def test():
    #     for i in await Completions().create(request):
    #         print(i)
    #
    #
    # arun(test())
