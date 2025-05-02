#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : files
# @Time         : 2025/1/3 15:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.io.openai_files import file_extract, guess_mime_type
from meutils.str_utils.json_utils import json_path
from meutils.str_utils.regular_expression import parse_url

from meutils.llm.clients import AsyncOpenAI, zhipuai_client
from meutils.llm.openai_utils import to_openai_params

from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, CompletionUsage


class Completions(object):

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def create(self, request: CompletionRequest):
        logger.debug(request.last_user_content)
        logger.debug(parse_url(request.last_assistant_content))

        if request.last_user_content.startswith("http"):  # 文件问答-单轮
            file_url, *texts = request.last_user_content.split(maxsplit=1) + ["总结下"]
            text = texts[0]

            file_content = await file_extract(file_url)

            request.messages = [
                {
                    'role': 'user',
                    'content': f"""{json.dumps(file_content, ensure_ascii=False)}\n\n{text}"""
                }
            ]
        elif image_urls := request.last_urls.get("image_url"):  # 长度为1
            url = image_urls[0]

            if guess_mime_type(url).startswith("image"):  # 图片问答

                request.model = "glm-4v-flash" if "image" not in request.model else request.model
                for i, message in enumerate(request.messages):
                    if message.get("role") == "user":
                        user_contents = message.get("content")
                        if isinstance(user_contents, list):
                            for i, content in enumerate(user_contents):
                                content_type = content.get("type")

                                if content_type == "image_url":
                                    image_url = content.get("image_url", "")
                                    if isinstance(image_url, dict):
                                        image_url = image_url.get("url", "")

                                    user_contents[i] = {"type": "image_url", "image_url": {"url": image_url}}

            else:  # 文件问答-多轮
                for i, message in enumerate(request.messages[::-1], 1):
                    if message.get("role") == "user":
                        texts = json_path(message, expr='$..text') or [""]
                        file_urls = json_path(message, expr='$..image_url') or [""]

                        # logger.debug(f"""{texts} \n\n {file_urls}""")

                        text, file_url = texts[-1], file_urls[-1]
                        if file_url in image_urls:
                            file_content = await file_extract(file_url)

                            message["content"] = f"""{json.dumps(file_content, ensure_ascii=False)}\n\n{text}"""

                            request.messages = request.messages[-i:]
                            break  # 截断：从最新的文件开始

        elif image_urls := parse_url(request.last_assistant_content):
            image_url = image_urls[-1]
            request.messages[-1]["content"] = [
                {"type": "text", "text": request.last_user_content},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]

        logger.debug(request.model_dump_json(indent=4))

        data = to_openai_params(request)

        if request.model.startswith("glm-4v-flash"):
            return await zhipuai_client.chat.completions.create(**data)

        return await AsyncOpenAI(api_key=self.api_key).chat.completions.create(**data)


# data: {"event": "message", "task_id": "900bbd43-dc0b-4383-a372-aa6e6c414227", "id": "663c5084-a254-4040-8ad3-51f2a3c1a77c", "answer": "Hi", "created_at": 1705398420}\n\n
if __name__ == '__main__':
    c = Completions()

    request = CompletionRequest(
        # model="qwen-turbo-2024-11-01",
        # model="claude-3-5-sonnet-20241022",
        model="deepsek-chat",

        messages=[
            # {
            #     'role': 'system',
            #     'content': '你是一个文件问答助手'
            # },
            # {
            #     'role': 'user',
            #     # 'content': {
            #     #     "type": "file_url",
            #     #     "file_url": {"url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf", "detai": "auto"}
            #     # },
            #     'content': [
            #         {
            #             "type": "text",
            #             "text": "这个文件讲了什么？"
            #         },
            #         # 多轮的时候要剔除
            #         {
            #             "type": "file_url",
            #             "file_url": {"url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf", "detai": "auto"}
            #         }
            #     ]
            # },

            {
                'role': 'user',
                # "content": '你好',
                "content": [
                    {"type": "text", "text": "https://oss.ffire.cc/files/kling_watermark.png 描述第一张图片"},

                    # {"type": "text", "text": "描述第一张图片"},
                    #
                    # {"type": "image_url", "image_url": "https://oss.ffire.cc/files/kling_watermark.png"},
                    #     # {"type": "image_url", "image_url": "https://oss.ffire.cc/files/nsfw.jpg"}
                    #
                ],

                # 'content': {
                #     "type": "file_url",
                #     "file_url": {"url": "https://mj101-1317487292.cos.ap-shanghai.myqcloud.com/ai/test.pdf", "detai": "auto"}
                # },
                # 'content': "https://oss.ffire.cc/files/%E6%8B%9B%E6%A0%87%E6%96%87%E4%BB%B6%E5%A4%87%E6%A1%88%E8%A1%A8%EF%BC%88%E7%AC%AC%E4%BA%8C%E6%AC%A1%EF%BC%89.pdf 这个文件讲了什么？",
                # 'content': "https://translate.google.com/?sl=zh-CN&tl=en&text=%E6%8F%90%E4%BE%9B%E6%96%B9&op=tr1anslate 这个文件讲了什么？",

                # "content": "https://oss.ffire.cc/files/百炼系列手机产品介绍.docx 总结下"
                # "content": "https://mj101-1317487292.cos.ap-shanghai.myqcloud.com/ai/test.pdf\n\n总结下"

                # "content": "https://admin.ilovechatgpt.top/file/lunIMYAIzhinengzhushouduishenghuodocx_14905733.docx 总结",
                # "content": "http://admin.ilovechatgpt.top/file/xinjianMicrosoftWordwendangdoc-9052714901036-bGSJLeKbqQdnIZZn.doc 111111234234",

            },
            #
            # {'role': 'assistant', 'content': "好的"},
            #
            # {
            #     'role': 'user',
            #     # "content": '描述第一张图片',
            #     "content": [
            #         {"type": "text", "text": "描述第一张图片"},
            #
            #         {"type": "image_url", "image_url": "https://oss.ffire.cc/files/nsfw.jpg"}
            #
            #     ],
            #
            # },
            # {
            #     'role': 'user',
            #     'content': [
            #         {
            #             "type": "text",
            #             "text": "总结下"
            #         },
            #
            #         {
            #             "type": "image_url",
            #             "image_url": "xx"
            #         }
            #     ]
            # },
            # {
            #     'role': 'user',
            #     'content': [
            #         {
            #             "type": "text",
            #             "text": "总结下"
            #         },
            #
            #         {
            #             "type": "image_url",
            #             "image_url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf"
            #         }
            #     ]
            # },
            # {
            #     'role': 'user',
            #     'content': [
            #         {
            #             "type": "text",
            #             "text": "总结下"
            #         },
            #
            #         {
            #             "type": "image_url",
            #             "image_url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf"
            #         }
            #     ]
            # },
            # {
            #     'role': 'assistant',
            #     'content': "你好"
            # },
            # {
            #     'role': 'user',
            #     'content': [
            #         {
            #             "type": "text",
            #             "text": "总结下"
            #         },
            #
            #         {
            #             "type": "image_url",
            #             "image_url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf"
            #         }
            #     ]
            # },
            # {
            #     'role': 'assistant',
            #     'content': "1"
            # },
            # {
            #     'role': 'user',
            #     'content': [
            #         {
            #             "type": "text",
            #             "text": "总结1"
            #         }
            #     ]
            # },
            # {
            #     'role': 'assistant',
            #     'content': "2"
            # },
            # {
            #     'role': 'user',
            #     'content': "总结2"
            # },
            #     'content': [
            #         {
            #             "type": "text",
            #             "text": "错了 继续回答"
            #         },
            #         # {
            #         #     "type": "file_url",
            #         #     "file_url": {"url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf", "detai": "auto"}
            #         # }
            #     ]
            # }
        ]

    )

    # [{'role': 'system',
    #   'content': 'undefined\n Current date: 2025-03-13'},
    #  {'role': 'user',
    #   'content': [{'type': 'text', 'text': '解读'},
    #               {'type': 'image_url',
    #                'image_url': 'https://ai.chatfire.cn/files/images/xx-1741850404348-339a12ba3.png'}]},
    #  {},
    #  {'role': 'user', 'content': '总结一下'}]

    arun(c.create(request))
