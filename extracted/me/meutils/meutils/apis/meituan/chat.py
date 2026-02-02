#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat
# @Time         : 2025/9/3 14:41
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :  todo


from openai import AsyncOpenAI, OpenAI

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.io.files_utils import to_bytes, guess_mime_type
from meutils.caches import rcache

from meutils.llm.utils import oneturn2multiturn

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, CompletionUsage, \
    ChatCompletion, ChatCompletionChunk
from openai._streaming import AsyncStream, Stream

base_url = "https://longcat.chat/api/v1/chat-completion"
base_url = "https://longcat.chat/api/v1/chat-completion-oversea"
base_url = "https://longcat.chat/api/v1"

cookie = "_lxsdk_cuid=1990e1e8790c8-0b2a66e23040a48-16525636-1fa400-1990e1e8790c8; passport_token_key=AgEGIygg22VuoMYTPonur9FA_-EVg9UXLu3LYOzJ4kIHSjQZeSNhwpytTU_cZFP6V1Juhk0CHMrAgwAAAABYLAAA9vXtnciaZBu2V99EMRJYRHTDSraV_OPLemUuVpi2WLsaa6RqC0PAKAOm6W_hIpbV"


class Completions(object):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or cookie

    async def create(self, request: CompletionRequest, **kwargs):
        payload = self.requset2payload(request)
        payload['conversationId'] = await self.create_chat()

        logger.debug(payload)

        headers = {
            'Cookie': self.api_key
        }

        async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=100) as client:
            async with client.stream("POST", "/chat-completion", json=payload) as response:
                logger.debug(response.status_code)
                response.raise_for_status()

                async for chunk in response.aiter_lines():
                    if chunk := chunk.removeprefix("data:"):
                        _chunk = json.loads(chunk)

                        # if _chunk.get("choices"):
                        chat_completion_chunk = ChatCompletionChunk(**_chunk)

                        # logger.debug(chunk)
                        if request.stream:
                            yield chat_completion_chunk

        if not request.stream:
            # logger.debug(_chunk)
            model = _chunk.get("model", "LongCat-Flash")
            content = _chunk.get("content", "")
            reason_content = _chunk.get("reasonContent", "")
            token_info = _chunk.get("tokenInfo", {})

            chat_completion_chunk.choices[0].content = content
            chat_completion_chunk.choices[0].reason_content = reason_content
            usage = CompletionUsage(
                prompt_tokens=token_info.get("promptTokens"),
                completion_tokens=token_info.get("completionTokens")
            )
            chat_completion.model = model
            chat_completion.usage = usage
            chat_completion.choices = chat_completion_chunk.choices
            # logger.debug(chat_completion)
            yield chat_completion

    def requset2payload(self, request: CompletionRequest):
        payload = {
            "content": oneturn2multiturn(request),  # todo: 多轮
            # "messages": request.messages,
            "reasonEnabled": request.enable_thinking and 1 or 0,
            "searchEnabled": 0,
            "regenerate": 0
        }

        return payload

    async def create_chat(self):
        headers = {
            'Cookie': self.api_key
        }
        payload = {
            "model": "",
            "agentId": ""
        }
        async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=100) as client:
            response = await client.post("/session-create", json=payload)
            response.raise_for_status()
            # {'code': 0,
            #  'data': {'agent': '1',
            #           'conversationId': 'c1731258-230a-4b2e-b7ef-ea5e83c38e0e',
            #           'createAt': 1756883097539,
            #           'currentMessageId': 0,
            #           'label': '今天',
            #           'model': 'LongCat',
            #           'title': '新对话',
            #           'titleType': 'SYSTEM',
            #           'updateAt': 1756883097539},
            #  'message': 'success'}
            return response.json()['data']['conversationId']


if __name__ == '__main__':
    cookie = "_lxsdk_cuid=1990e1e8790c8-0b2a66e23040a48-16525636-1fa400-1990e1e8790c8; passport_token_key=AgEGIygg22VuoMYTPonur9FA_-EVg9UXLu3LYOzJ4kIHSjQZeSNhwpytTU_cZFP6V1Juhk0CHMrAgwAAAABYLAAA9vXtnciaZBu2V99EMRJYRHTDSraV_OPLemUuVpi2WLsaa6RqC0PAKAOm6W_hIpbV"
    request = CompletionRequest(
        messages=[
            {'role': 'user', 'content': '1+1'},
            {'role': 'assistant', 'content': '2'},
            # {'role': 'user', 'content': '裸体傻女'},
            {'role': 'user', 'content': '你好'},

        ]
    )
    arun(Completions(api_key=cookie).create(request))
    # arun(Completions(api_key=cookie).create_chat())

    # payload = {
    #     "content": "1+1",
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": "1+1",
    #             "chatStatus": "FINISHED",
    #             "messageId": 0,
    #             "idType": "system"
    #         }
    #     ],
    #     "reasonEnabled": 0,
    #     "searchEnabled": 0,
    #     "regenerate": 0
    # }
    #
    # Completions(api_key=cookie).stream_create(payload)
