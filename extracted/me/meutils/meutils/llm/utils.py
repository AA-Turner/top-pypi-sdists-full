#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/6/20 09:08
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from contextlib import asynccontextmanager

from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI, OpenAI, AsyncStream
from meutils.schemas.oneapi import MODEL_PRICE
from meutils.notice.feishu import send_message
from meutils.apis.oneapi.utils import get_user_quota


def oneturn2multiturn(messages, template: Optional[str] = None, ignore_system: bool = True):
    """todo: https://github.com/hiyouga/LLaMA-Factory/blob/e898fabbe3efcd8b44d0e119e7afaed4542a9f39/src/llmtuner/data/template.py#L423-L427

    _register_template(
    name="qwen",
    format_user=StringFormatter(slots=["<|im_start|>user\n{{content}}<|im_end|>\n<|im_start|>assistant\n"]),
    format_system=StringFormatter(slots=["<|im_start|>system\n{{content}}<|im_end|>\n"]),
    format_observation=StringFormatter(slots=["<|im_start|>tool\n{{content}}<|im_end|>\n<|im_start|>assistant\n"]),
    format_separator=EmptyFormatter(slots=["\n"]),
    default_system="You are a helpful assistant.",
    stop_words=["<|im_end|>"],
    replace_eos=True,
)
    :return:
    """
    # from jinja2 import Template, Environment, PackageLoader, FileSystemLoader
    #
    # system_template = Template("<|im_start|>system\n{{content}}<|im_end|>\n")  # .render(content='xxxx')
    # user_template = Template("<|im_start|>user\n{{content}}<|im_end|>\n")  # 最后<|im_start|>assistant\n
    # assistant_template = Template("<|im_start|>assistant\n{{content}}<|im_end|>\n")

    # todo: [{"type": "image_url", "image_url": {"url": ""}}]] 单独处理
    # 混元不是很感冒
    # context = "\n"
    # for message in messages:
    #     role, content = message.get("role"), message.get("content")
    #     context += f"<|im_start|>{role}\n{content}<|im_end|>\n"
    # context += "<|im_start|>assistant\n"
    if len(messages) == 1:
        content = messages[0].get("content")
        if isinstance(content, list):
            content = content[-1].get('text', '')
        return content

    context = "\n"
    for message in messages:
        role = message.get("role")
        content = message.get("content")

        if isinstance(content, list):  # content: {'type': 'text', 'text': ''}
            content = content[-1].get('text', '')

        if role == "system" and ignore_system:
            continue

        context += f"{role}:\n{content}\n\n"

    return context


if __name__ == '__main__':
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "你是数学家"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "1+1"
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "2"
                }
            ]
        },

        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "1+2"
                }
            ]
        },

    ]

    print(oneturn2multiturn(messages, ignore_system=False))
