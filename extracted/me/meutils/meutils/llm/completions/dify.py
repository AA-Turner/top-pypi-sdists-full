#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : completions
# @Time         : 2024/8/28 10:04
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json

from meutils.pipe import *
from meutils.notice.feishu import send_message as _send_message
from meutils.db.redis_db import redis_client, redis_aclient
from meutils.config_utils.lark_utils import aget_spreadsheet_values

from meutils.llm.openai_utils import to_openai_completion_params, token_encoder, token_encoder_with_cache
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, ChatCompletionRequest, CompletionUsage
from meutils.schemas.dify_types import BASE_URL, ChatCompletionChunkResponse
from openai import OpenAI, AsyncOpenAI, APIStatusError

send_message = partial(
    _send_message,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/e0db85db-0daf-4250-9131-a98d19b909a9",
    title=__name__
)


class Completions(object):

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def create(self, request: ChatCompletionRequest):
        payload = {
            "inputs": {},
            "query": request.last_content,
            "response_mode": "streaming",
            "conversation_id": "",
            "user": request.user or 'chatfire',
            "files": [
                {
                    "type": "image",
                    "transfer_method": "remote_url",
                    "url": "https://cloud.dify.ai/logo/logo-site.png"
                }
            ]
        }
        headers = {'Authorization': f'Bearer {self.api_key}'}
        async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=200) as client:
            async with client.stream(method="POST", url="/chat-messages", json=payload) as response:
                async for chunk in response.aiter_lines():
                    if chunk.startswith("data: {") and (chunk := chunk.strip("data:").strip()):
                        try:
                            chunk_resp = ChatCompletionChunkResponse.model_validate_json(chunk)
                            yield chunk_resp.answer

                            if chunk_resp.event not in {"message", "agent_message"}:  # debug
                                logger.debug(json.loads(chunk))

                        except Exception as e:
                            _ = f"{e}\n{chunk}"
                            logger.error(_)
                            send_message(_)


# data: {"event": "message", "task_id": "900bbd43-dc0b-4383-a372-aa6e6c414227", "id": "663c5084-a254-4040-8ad3-51f2a3c1a77c", "answer": "Hi", "created_at": 1705398420}\n\n
if __name__ == '__main__':
    c = Completions('app-1O2hPvpPf46cmiCjKqd2Dyx5')

    request = ChatCompletionRequest(messages=[{'role': 'user', 'content': '画条狗'}])


    # arun(c.create(request))

    async def main():
        async for i in c.create(request):
            print(i, end='')


    arun(main())
