#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : zhipu_智能体
# @Time         : 2024/12/30 17:34
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://bigmodel.cn/dev/api/intelligent-agent-model/assistantapi

from meutils.pipe import *
from meutils.llm.openai_utils import to_openai_params
from meutils.llm.clients import AsyncOpenAI, zhipuai_sdk_client
from meutils.str_utils.regular_expression import parse_url

from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, CompletionUsage


class Completions(object):

    def __init__(self,
                 base_url: Optional[str] = None,
                 api_key: Optional[str] = None
                 ):
        pass

    async def create(self, request: CompletionRequest):
        # attachments = [{"file_id": "chatglm4/3db10f79-a952-4987-83d2-cf0cfd5d5530.pdf"}]

        chunks = zhipuai_sdk_client.assistant.conversation(
            assistant_id=request.model,

            model="glm-4-assistant",
            messages=request.messages,
            stream=True,
            attachments=None,
            metadata=None
        )

        references = {}
        for chunk in chunks:
            # logger.debug(chunk)
            delta = chunk.choices[0].delta

            if hasattr(delta, "tool_calls") and delta.tool_calls:
                logger.debug(delta.tool_calls)

                tool_call = delta.tool_calls[0].model_dump()
                tool_type = tool_call.get("type", "")  # drawing_tool code_interpreter web_browser retrieval
                outputs = tool_call.get(tool_type, {}).get("outputs") or []
                # references += outputs

                references.setdefault(tool_type, []).extend(outputs)

                if not outputs:
                    yield f"\n\n```json\n{delta.model_dump_json(indent=4, exclude_none=True)}\n```\n\n"
                logger.debug(references)

                continue

            if hasattr(delta, "content"):
                if references:
                    for i in self.references2content(references):
                        yield i
                    references = {}
                # logger.debug(delta.content)
                yield delta.content

            else:
                logger.debug(delta)

            # if references: # 搜索
            #     urls = [f"[^{i}]: [{ref['title']}]({ref['link']})\n" for i, ref in enumerate(references, 1)]
            #
            #     for url in urls:
            #         yield url
            #
            #     references = []
            #
            # delta = chat_completion_chunk.choices[0].delta.model_construct(**delta.model_dump())
            # chat_completion_chunk.choices[0].delta = delta
            # yield chat_completion_chunk

    def references2content(self, references):
        """drawing_tool code_interpreter web_browser retrieval"""
        if outputs := references.get("web_browser"):
            for i, ref in enumerate(outputs, 1):
                # yield f"[^{i}]: [{ref['title']}]({ref['link']})\n"
                yield f"[{ref['title']}]({ref['link']})\n"

        elif outputs := references.get("drawing_tool"):
            for i, ref in enumerate(outputs, 1):
                yield f"![{i}]({ref['image']})\n"

        yield "\n"

    async def _create(self, request: CompletionRequest):
        if request.last_user_content.startswith(("http",)):
            file_url, text = request.last_user_content.split(maxsplit=1)

            request.messages = [
                {
                    'role': 'user',
                    'content': [
                        {
                            "type": "text",
                            "text": text
                        },

                        {
                            "type": "file",  # 不标准
                            "file_url": {
                                "url": file_url
                            }
                        }
                    ]
                }
            ]

        logger.debug(request)

        data = to_openai_params(request)
        return await self.client.chat.completions.create(**data)


if __name__ == '__main__':
    assistant_id = "65940acff94777010aa6b796"
    # assistant_id = "65d2f07bb2c10188f885bd89"
    # assistant_id="65a265419d72d299a9230616",
    # assistant_id="659d051a5f14eb8ce1235b96",
    # assistant_id="65d2f07bb2c10188f885bd89",

    # assistant_id="659e54b1b8006379b4b2abd6",
    # conversation_id=None,  # 多轮：从messages获取
    # conversation_id="67dd1317d7c8fe4c9efe459a",
    request = CompletionRequest(
        model=assistant_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        # "text": "画条狗 输出两张图片",
                        # "text": "南京天气如何",
                        # "text": "https://sfile.chatglm.cn/chatglm4/3db10f79-a952-4987-83d2-cf0cfd5d5530.pdf 总结这个文件",

                        "text": "https://sfile.chatglm.cn/chatglm4/3db10f79-a952-4987-83d2-cf0cfd5d5530.pdf 基于这个文件做个ppt"

                        # "text": "周杰伦 【最新动态、相关信息或新闻】",
                        # "text": "生成PPT"
                    }]
            }
        ],

        # messages=[
        #     {
        #         "role": "user",
        #         "content": [
        #             {
        #                 "type": "text",
        #                 "text": "基于这个内容做个ppt"
        #             },
        #             {
        #                 "type": "file",
        #                 "file": [
        #                     {
        #                         "file_id": "chatglm4/3db10f79-a952-4987-83d2-cf0cfd5d5530.pdf",
        #                         "file_url": "https://sfile.chatglm.cn/chatglm4/3db10f79-a952-4987-83d2-cf0cfd5d5530.pdf",
        #                         "file_name": "附件.大模型在合规管理工作中的应用.pdf",
        #                         "file_size": 2571523,
        #                         "order": 0,
        #                         "maxReadPercent": 0,
        #                         "cover_images": [],
        #                         "url": "https://sfile.chatglm.cn/chatglm4/3db10f79-a952-4987-83d2-cf0cfd5d5530.pdf"
        #                     }
        #                 ]
        #             }
        #         ]
        #     }
        # ]
    )

    arun(Completions().create(request))
    # 输入 输出
    # input
    # {
    #     "assistant_id": "65d2f07bb2c10188f885bd89",
    #     "conversation_id": "67d932d5e579c3ded42aa80e",
    #     "meta_data": {
    #         "if_plus_model": false,
    #         "is_test": false,
    #         "input_question_type": "xxxx",
    #         "channel": "",
    #         "draft_id": "",
    #         "quote_log_id": "",
    #         "platform": "pc"
    #     },
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": [
    #                 {
    #                     "type": "text",
    #                     "text": "基于这个内容做个ppt"
    #                 },
    #                 {
    #                     "type": "file",
    #                     "file": [
    #                         {
    #                             "file_id": "chatglm4/3db10f79-a952-4987-83d2-cf0cfd5d5530.pdf",
    #                             "file_url": "https://sfile.chatglm.cn/chatglm4/3db10f79-a952-4987-83d2-cf0cfd5d5530.pdf",
    #                             "file_name": "附件.大模型在合规管理工作中的应用.pdf",
    #                             "file_size": 2571523,
    #                             "order": 0,
    #                             "maxReadPercent": 0,
    #                             "cover_images": [],
    #                             "url": "https://sfile.chatglm.cn/chatglm4/3db10f79-a952-4987-83d2-cf0cfd5d5530.pdf"
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     ]
    # }
