#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : deepx
# @Time         : 2025/3/20 08:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""
deep + claude

"""

from openai import AsyncOpenAI

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.io.files_utils import to_bytes
from meutils.io.openai_files import file_extract, guess_mime_type
from meutils.str_utils.json_utils import json_path
from meutils.apis.search import metaso

from meutils.llm.clients import chatfire_client, zhipuai_client, AsyncOpenAI
from meutils.llm.openai_utils import to_openai_params

from meutils.schemas.openai_types import ChatCompletionRequest
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, ImageRequest

"""
delta = chunk.choices[0].delta
| │ └ []
| └ ChatCompletionChunk(id='02174299556532927e9140493fc1cd076b4fe1b883ff101a83257', choices=[], created=1742995565, model='deep-d...
|
"""
class Completions(object):

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key=api_key)

    async def create(self, request: CompletionRequest):
        """
        :param request:
        :return:
        """
        data = to_openai_params(request)
        data['model'] = 'deepseek-reasoner'
        data['max_tokens'] = 1  # 火山 支持max_tokens=1输出思维链
        if request.stream:
            reasoning_content = ""
            completions = await chatfire_client.chat.completions.create(**data)
            async for chunk in completions:
                if chunk.choices:  # 自定义没问题，todo:openai通道报错
                    # logger.debug(chunk)
                    yield chunk
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "reasoning_content"):
                        reasoning_content += delta.reasoning_content
                else:
                    logger.error(chunk)

            request.messages = [
                {
                    'role': 'user',
                    'content': f"""<think>\n\n{reasoning_content}\n\n</think>\n\n{request.last_user_content}"""
                }
            ]
            logger.debug(request)
            data = to_openai_params(request)
            async for chunk in await self.client.chat.completions.create(**data):
                # logger.debug(chunk)
                yield chunk
        else:
            reasoning_content = ""
            completions = await chatfire_client.chat.completions.create(**data)
            message = completions.choices[0].message
            if hasattr(message, "reasoning_content"):
                reasoning_content += message.reasoning_content

            request.messages = [
                {
                    'role': 'user',
                    'content': f"""<think>\n\n{reasoning_content}\n\n</think>\n\n\n{request.last_user_content}"""
                }
            ]
            data = to_openai_params(request)
            _completions = await self.client.chat.completions.create(**data)
            completions.choices[0].message.content = _completions.choices[0].message.content
            yield completions

    async def screate(self, request: CompletionRequest):
        pass


if __name__ == '__main__':
    c = Completions()

    request = CompletionRequest(
        # model="qwen-turbo-2024-11-01",
        # model="claude-3-5-sonnet-20241022",
        model="deepseek-chat",
        stream=True,

        messages=[{
            'role': 'user',
            'content': "1+1"
        }])

    arun(c.create(request))
