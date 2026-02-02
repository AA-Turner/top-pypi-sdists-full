#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : sophnet
# @Time         : 2025/6/4 16:16
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI

from meutils.llm.check_utils import check_token_for_sophnet as check_token

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, CompletionUsage, \
    ChatCompletion

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=lxJ27j"

base_url = "https://www.sophnet.com/api/open-apis/v1"


async def create(request: CompletionRequest, token: Optional[str] = None):
    """最终是非流"""
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True, check_token=check_token)

    client = AsyncOpenAI(base_url=base_url, api_key=token)

    if not request.stream:
        logger.debug("伪非流")

        data = request.model_dump(exclude_none=True)
        data['stream'] = True

        chunks = await client.chat.completions.create(**data)

        chunk = None
        async for chunk in chunks:
            if chunk.choices:
                _ = chunk.choices[0].delta.content or ""
                chat_completion.choices[0].message.content += _
                # logger.debug(_)
        if hasattr(chunk, "usage"):
            chat_completion.usage = chunk.usage

        logger.debug(chat_completion)
        return chat_completion
    else:
        return client.chat.completions.create(**request.model_dump(exclude_none=True))


if __name__ == '__main__':
    request = CompletionRequest(
        model="DeepSeek-v3",
        messages=[{"role": "user", "content": "hi"}],
        stream=True,
    )

    arun(create(request))
