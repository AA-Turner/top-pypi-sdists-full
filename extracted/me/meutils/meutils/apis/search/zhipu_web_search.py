#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : web_search
# @Time         : 2025/3/18 20:15
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.caches import rcache

from meutils.async_utils import sync_to_async

from meutils.llm.clients import zhipuai_sdk_client
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, ChatCompletionChunk


def convert_citations(text):
    """
    # 示例使用
    text = "这是一段包含【1†source】和【2†source】的文本"
    result = convert_citations(text)
    print(result)  # 输出: 这是一段包含[^1]和[^2]的文本
    :param text:
    :return:
    """
    # 匹配【数字†source】格式的引用
    pattern = r'【(\d+)†source】'

    # 替换为[^数字]格式
    converted = re.sub(pattern, r'[^\1]', text)

    return converted


class Completions(object):

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    # @rcache(noself=True, ttl=15 * 60)
    @sync_to_async
    def query(self, q: str):
        data = list(self.create(q))
        return {"data": data}

    def create(self, request: Union[CompletionRequest, str]):

        q = request.last_user_content if isinstance(request, CompletionRequest) else request
        q = f"{q} 【最新动态、相关信息或新闻】"

        chunks = zhipuai_sdk_client.assistant.conversation(

            assistant_id="659e54b1b8006379b4b2abd6",  # 搜索智能体
            conversation_id=None,
            model="glm-4-assistant",  # assistant-ppt
            messages=[
                {
                    "role": "user",
                    "content": [{
                        "type": "text",
                        # "text": "北京未来七天气温，做个折线图",
                        # "text": "画条狗"
                        "text": q,

                    }]
                }
            ],
            stream=True,
            attachments=None,
            metadata=None
        )

        references = []
        for chunk in chunks:
            # logger.debug(chunk)

            delta = chunk.choices[0].delta
            if hasattr(delta, "tool_calls") and delta.tool_calls:
                tool_call = delta.tool_calls[0].model_dump()
                # logger.debug(tool_call)
                tool_type = tool_call.get("type", "")  # web_browser
                references += tool_call.get(tool_type, {}).get("outputs") or []  # title link content

                # logger.debug(f"references: {references}")
                continue

            if isinstance(request, CompletionRequest):
                if references:
                    urls = [f"[^{i}]: [{ref['title']}]({ref['link']})\n" for i, ref in enumerate(references, 1)]

                    for url in urls:
                        yield url

                    references = []

                delta = chat_completion_chunk.choices[0].delta.model_construct(**delta.model_dump())
                chat_completion_chunk.choices[0].delta = delta
                yield chat_completion_chunk

            else:
                yield references
                break


if __name__ == '__main__':
    request = CompletionRequest(
        # model="baichuan4-turbo",
        # model="xx",
        # model="deepseek-r1",
        # model="deepseek-r1:1.5b",
        model="model",

        # model="moonshot-v1-8k",
        # model="doubao",

        messages=[
            {"role": "user", "content": "周杰伦"}
        ],

        stream=True
    )
    print(Completions().create(request))
    # arun(Completions().query(request.last_user_content))
