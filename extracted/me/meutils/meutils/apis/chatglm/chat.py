#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat
# @Time         : 2025/4/23 10:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.schemas.openai_types import CompletionRequest
from meutils.llm.clients import AsyncOpenAI
from meutils.caches import rcache
from meutils.schemas.chatglm_types import VideoRequest, Parameter, VIDEO_BASE_URL, EXAMPLES

from meutils.decorators.retry import retrying
from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.db.redis_db import redis_aclient

from fake_useragent import UserAgent

ua = UserAgent()

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=EOZuBW"
BASE_URL = "https://chatglm.cn/chatglm/backend-api"
"https://chatglm.cn/chatglm/backend-api/assistant/stream"


# {
#     "assistant_id": "65940acff94777010aa6b796",
#     "conversation_id": "",
#     "meta_data": {
#         "is_test": false,
#         "input_question_type": "xxxx",
#         "channel": "",
#         "draft_id": "",
#         "is_networking": false,
#         "chat_mode": "",
#         "quote_log_id": "",
#         "platform": "pc"
#     },
#     "messages": [
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "你是谁"
#                 }
#             ]
#         }
#     ]
# }

# {"id":"68084f7bef14104a4663f6a8","conversation_id":"68084f7bef14104a4663f6a7","assistant_id":"65940acff94777010aa6b796","parts":[],"created_at":"2025-04-23 10:24:59","status":"init","last_error":{},"meta_data":{"input_question_type":"xxxx","if_plus_model":false,"plus_model_available":true,"if_increase_push":false}}

class Completions(object):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def create(self, request: CompletionRequest):
        payload = {
            "assistant_id": request.model,
            "conversation_id": "",
            "meta_data": {
                "is_test": False,
                "input_question_type": "xxxx",
                "channel": "",
                "draft_id": "",
                "is_networking": False,
                "chat_mode": "",
                "quote_log_id": "",
                "platform": "pc"
            },
            "messages": request.messages
        }
        # client = AsyncOpenAI(base_url=BASE_URL, api_key=self.get_access_token())
        # response = await client.post(
        #     "/assistant/stream",
        #     cast_to=object,
        #     body=payload,
        #     stream=True,
        # )
        # for i in response:
        #     logger.debug(i)

        url = "https://chatglm.cn/chatglm/backend-api/assistant/stream"
        # response = self.httpx_client.post(url=url, json=payload)
        headers = {
            'Authorization': f"Bearer {self.get_access_token()}",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        async with httpx.AsyncClient(headers=headers).stream("POST", url=url, json=payload, timeout=200) as response:
            async for chunk in response.aiter_lines():
                logger.debug(chunk)

    @rcache(ttl=1 * 3600)
    async def get_access_token(self, token: Optional[str] = None):
        token = self.api_key or token or await get_next_token_for_polling(FEISHU_URL)

        response = await AsyncOpenAI(base_url=BASE_URL, api_key=token).post(
            "/v1/user/refresh",
            cast_to=object,
        )

        # logger.debug(response)

        return response.get("result", {}).get("accessToken")


if __name__ == '__main__':
    # arun(Completions().get_access_token())

    request = CompletionRequest(
        model="65940acff94777010aa6b796",
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": "你是谁"}],
            }
        ],
        stream=True,
    )

    arun(Completions().create(request))
