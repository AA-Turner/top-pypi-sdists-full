#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : gemini
# @Time         : 2025/2/14 17:36
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.llm.openai_utils import to_openai_params
from meutils.llm.clients import AsyncOpenAI
from meutils.str_utils.regular_expression import parse_url
from meutils.io.files_utils import to_url, markdown_base64_to_url

from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, CompletionUsage

"""
image => file

      "type": "image_url",
      "image_url": {
          

"""


class Completions(object):

    def __init__(self,
                 base_url: Optional[str] = None,
                 api_key: Optional[str] = None
                 ):

        base_url = "https://api.aiguoguo199.com/v1"

        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    async def create(self, request: CompletionRequest):
        if request.model == "gemini-2.0-flash-exp-image-generation":
            return await self.images_create(request)

        urls = sum(request.last_urls.values(), [])
        for url in urls:
            request.messages[-1]["content"].append({"type": "image_url", "image_url": {"url": url}})

        data = to_openai_params(request)
        return await self.client.chat.completions.create(**data)

    async def images_create(self, request: CompletionRequest):

        if request.last_assistant_content and (urls := parse_url(request.last_assistant_content)):
            for message in request.messages[::-1]:
                if message.get("role") == "assistant":
                    message["content"] = [
                        {"type": "image_url", "image_url": {"url": url.removesuffix(")")}} for url in urls
                    ]

        if urls := parse_url(request.last_user_content):  # 修正提问格式， 兼容 url
            for message in request.messages[::-1]:
                if message.get("role") == "user":
                    message["content"] = [
                        {"type": "image_url", "image_url": {"url": url.removesuffix(")")}} for url in urls
                    ]
                    message["content"] += [{"type": "text", "text": request.last_user_content}]

        # 调用模型
        # logger.debug(request.model_dump_json(indent=4))

        data = to_openai_params(request)
        response = await self.client.chat.completions.create(**data)

        if request.stream:
            return self.stream_create(response)

        else:
            content = response.choices[0].message.content
            response.choices[0].message.content = await markdown_base64_to_url(content)  # base64 转 url

            if hasattr(response, "system_prompt"):
                del response.system_prompt

            return response

    async def stream_create(self, chunks):
        async for chunk in chunks:
            if hasattr(chunk, "system_prompt"):
                del chunk.system_prompt

            if (content := chunk.choices[0].delta.content) and content.startswith("!["):
                chunk.choices[0].delta.content = await markdown_base64_to_url(content)

                yield chunk
            else:
                yield chunk
            # logger.debug(str(chunk))


if __name__ == '__main__':
    url = "https://oss.ffire.cc/files/lipsync.mp3"
    url = "https://lmdbk.com/5.mp4"
    # url = "https://zj.lmdbk.com/tempVideos/c29b078f1fb75285a9a3362e1a39d1d2.mp4"
    content = [

        # {"type": "text", "text": "https://oss.ffire.cc/files/nsfw.jpg 移除右下角的水印"},

        {"type": "text", "text": "总结下"},
        # {"type": "image_url", "image_url": {"url": url}},

        {"type": "video_url", "video_url": {"url": url}}

    ]

    #
    request = CompletionRequest(
        # model="qwen-turbo-2024-11-01",
        model="gemini-2.0-flash",
        # model="gemini-2.0-flash-exp-image-generation",
        # model="qwen-plus-latest",

        messages=[
            {
                'role': 'user',

                'content': content
            },

        ],
        stream=False,
    )

    api_key = "sk-Q2XxJBh3KM7bTptL6e96E8596fC74426BaA87528867aA77b"

    arun(Completions(api_key=api_key).create(request))
