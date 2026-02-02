#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openrouter
# @Time         : 2025/8/28 08:59
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from meutils.llm.clients import OpenAI

models_mapping = {
    "deepseek-v3.1": "deepseek/deepseek-chat-v3.1:free",
    "kimi-k2-250711": "moonshotai/kimi-k2:free",
    "deepseek-r1-250528": "deepseek/deepseek-r1-0528:free",

}


def get_models_mapping():
    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url=os.getenv("OPENROUTER_BASE_URL"),
    )

    models = client.models.list().data
    models = {
        m.id.lower().split('/', maxsplit=1)[-1].removesuffix(":free"): m.id
        for m in models
        if m.id.lower().endswith(':free')
    }
    return {**models, **models_mapping}


if __name__ == '__main__':
    data = get_models_mapping()
    print(bjson(data))
    print(','.join(data))
