#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat_all
# @Time         : 2025/3/4 13:25
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from openai import AsyncOpenAI

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.io.files_utils import to_bytes
from meutils.io.openai_files import file_extract, guess_mime_type
from meutils.str_utils.json_utils import json_path
from meutils.apis.search import metaso
# from meutils.apis.chatglm import glm_video_api

from meutils.llm.clients import chatfire_client, zhipuai_client, AsyncOpenAI
from meutils.llm.openai_utils import to_openai_params

from meutils.schemas.openai_types import ChatCompletionRequest
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, ImageRequest

from fake_useragent import UserAgent

ua = UserAgent()

"""
todo: ppt

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
        request.model = request.model.removesuffix("-all").removesuffix("-plus")  ### 避免死循环

        if request.last_user_content.startswith(("画",)):  # 画画
            return await self.create_images(request)  # str

        # ppt 视频生成
        # elif request.last_user_content.startswith(("联网", "搜索", "在线搜索", "在线查询")):  # 画画
        #     return metaso.create(request)
        # elif request.last_user_content.startswith(("视频",)):  # 视频生成

        elif request.last_user_content.startswith(("联网", "搜索", "在线搜索", "在线查询")):  # 画画
            return metaso.create(request)

        elif request.last_user_content.startswith(("http",)):

            file_url, *texts = request.last_user_content.split(maxsplit=1) + ["总结下"]  # application/octet-stream
            text = texts[0]

            if guess_mime_type(file_url).startswith("image"):  # 识图
                request.model = "glm-4v-flash"
                request.messages = [
                    {
                        'role': 'user',
                        'content': [
                            {
                                "type": "text",
                                "text": text
                            },

                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": file_url
                                }
                            }
                        ]
                    }
                ]
                data = to_openai_params(request)
                return await zhipuai_client.chat.completions.create(**data)

            elif guess_mime_type(file_url).startswith(("video", "audio")):  # 音频 视频
                request.model = "gemini"  # 果果
                request.messages = [
                    {
                        'role': 'user',
                        'content': [
                            {
                                "type": "text",
                                "text": text
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": file_url
                                }
                            }
                        ]
                    }
                ]
                data = to_openai_params(request)
                return await self.client.chat.completions.create(**data)

            else:
                # logger.debug(f"file_url: {file_url}")
                file_content = await file_extract(file_url)  # 文件问答-单轮

                logger.debug(file_content)

                request.messages = [
                    {
                        'role': 'user',
                        'content': f"""{json.dumps(file_content, ensure_ascii=False)}\n\n{text}"""
                    }
                ]
                # logger.debug(request)
                data = to_openai_params(request)
                return await self.client.chat.completions.create(**data)

        if image_urls := request.last_urls.get("image_url"):  # 识图
            request.model = "glm-4v-flash"
            data = to_openai_params(request)
            return await zhipuai_client.chat.completions.create(**data)

        elif file_urls := request.last_urls.get("file_url"):
            return await self.chat_files(request)

        # todo 标准格式的audio_url video_url

        data = to_openai_params(request)
        return await self.client.chat.completions.create(**data)

    async def chat_files(self, request: CompletionRequest):  # 多轮
        for i, message in enumerate(request.messages[::-1], 1):
            if message.get("role") == "user":
                texts = json_path(message, expr='$..text') or [""]
                file_urls = json_path(message, expr='$..file_url.url') or [""]

                logger.debug(f"""{texts} \n\n {file_urls}""")

                text, file_url = texts[-1], file_urls[-1]
                if file_url in request.last_urls.get("file_url", []):
                    file_content = await file_extract(file_url)

                    message["content"] = f"""{json.dumps(file_content, ensure_ascii=False)}\n\n{text}"""

                    request.messages = request.messages[-i:]
                    break  # 截断：从最新的文件开始

        data = to_openai_params(request)
        return await self.client.chat.completions.create(**data)

    async def create_images(self, request: CompletionRequest):

        response = await zhipuai_client.images.generate(
            model="cogview-3-flash",
            prompt=request.last_user_content,
            n=1
        )
        image_url = response.data[0].url
        tool_desc = """> images.generate\n\n"""
        tool_desc += f"![{request.last_user_content}]({image_url})"
        if not request.stream:
            chat_completion.choices[0].message.content = tool_desc
            return chat_completion
        return tool_desc

    # chat_completion_chunk

    # async def create_videos(self, request: CompletionRequest):
    #
    #     request = ImageRequest(prompt=request.last_user_content)
    #
    #     response = await glm_video_api.generate(request)
    #     image_url = response.data[0].url
    #     tool_desc = """> images.generate\n\n"""
    #     return tool_desc + f"![{request.last_user_content}]({image_url})"


if __name__ == '__main__':
    c = Completions()

    request = CompletionRequest(
        # model="qwen-turbo-2024-11-01",
        # model="claude-3-5-sonnet-20241022",
        model="gpt-4o-mini",

        messages=[{
            'role': 'user',
            'content': [
                {
                    "type": "text",
                    # "text": "总结下"
                    "text": "https://app.yinxiang.com/fx/8b8bba1e-b254-40ff-81e1-fa3427429efe 总结下",

                    # "text": "https://app.yinxiang.com/fx/8b8bba1e-b254-40ff-81e1-fa3427429efe"

                },

                # {
                #     "type": "file_url",
                #     "file_url": {
                #         "url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf"
                #     }
                # }
            ]
        }])

    arun(c.create(request))
