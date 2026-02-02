#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ollama
# @Time         : 2025/9/26 09:02
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.llm.clients import OpenAI

models_mapping = {

    "kimi-k2-250711": "kimi-k2:1t",
    "kimi-k2-0711-preview": "kimi-k2:1t",

    "kimi-k2-250905": "kimi-k2:1t",
    "kimi-k2-0905-preview": "kimi-k2:1t",

    'qwen3-coder': 'qwen3-coder:480b',
    "qwen3-coder-480b-a35b-instruct": "qwen3-coder:480b",

    'deepseek-v3.1': 'deepseek-v3.1:671b',
    'deepseek-v3-1-250821': 'deepseek-v3.1:671b',

    'gpt-oss-120b': 'gpt-oss:120b',
    'gpt-oss-20b': 'gpt-oss:20b',

}


def get_models_mapping():
    client = OpenAI(

        base_url="https://ollama.com/v1",
    )

    models = client.models.list().data
    models = {
        m.id.replace(':', '-'): m.id for m in models
    }
    return {**models, **models_mapping}


if __name__ == '__main__':
    data = get_models_mapping()
    print(bjson(data))
    print(','.join(data))
