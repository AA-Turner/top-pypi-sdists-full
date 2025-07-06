#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : llm
# @Time         : 2025/6/4 13:33
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.schemas.openai_types import CompletionRequest
from meutils.llm.utils import oneturn2multiturn

from fal_client.client import AsyncClient, SyncClient, Status, FalClientError

models = "anthropic/claude-3.7-sonnet,anthropic/claude-3.5-sonnet, anthropic/claude-3-5-haiku, anthropic/claude-3-haiku, google/gemini-pro-1.5, google/gemini-flash-1.5, google/gemini-flash-1.5-8b, meta-llama/llama-3.2-1b-instruct, meta-llama/llama-3.2-3b-instruct, meta-llama/llama-3.1-8b-instruct, meta-llama/llama-3.1-70b-instruct, openai/gpt-4o-mini, openai/gpt-4o, deepseek/deepseek-r1"

async def create(
        request: CompletionRequest,
        api_key: Optional[str] = None,
):
    """
    Prompt length must be less than 5000 characters

    :param request:
    :param api_key:
    :return:
    """
    if (not request.stream and request.max_tokens and request.max_tokens < 11):
        yield " "
        return

    api_key = api_key and api_key.removeprefix("fal-")

    prompt = oneturn2multiturn(request.messages)

    arguments = {
        "model": request.model,
        "system_prompt": request.system_instruction,
        "prompt": prompt,
        "temperature": request.temperature,
        "reasoning": request.reasoning_effort is not None,
        "max_tokens": 1,
    }
    client = AsyncClient(key=api_key)

    if request.stream:
        yield ""

        stream = client.stream("fal-ai/any-llm", arguments=arguments)
        prefix = ""
        i = 0
        async for chunk in stream:
            _ = chunk.get("output")
            yield _.removeprefix(prefix)
            prefix = _
            i += 1
            if request.max_tokens and i > request.max_tokens:
                break

    else:
        response = await client.run("fal-ai/any-llm", arguments=arguments)
        # {'error': None, 'output': '1 + 1 = 2', 'partial': False, 'reasoning': None}
        if response.get("error"):
            logger.error(response)
        yield response.get("output")


if __name__ == '__main__':
    request = CompletionRequest(
        model="anthropic/claude-3.7-sonnet",
        messages=[
            # {"role": "user", "content": "1+1"},
            {"role": "user",
             "content": [{
                 "type": "text",
                 "text": "1+1"*10000
             }]
             },

        ],
        stream=True,
    )
    arun(create(request))
