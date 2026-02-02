#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : siliconflow
# @Time         : 2025/8/15 20:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.llm.clients import OpenAI

models_mapping = {
    "kimi-k2-turbo-preview": "kimi-k2-0711-preview",
    "moonshot-v1-8k": "kimi-k2-0711-preview",
    "moonshot-v1-32k": "kimi-k2-0711-preview",
    "moonshot-v1-128k": "kimi-k2-0711-preview",

}


def get_models_mapping():
    client = OpenAI(
        api_key=os.getenv("MOONSHOT_API_KEY"),
        base_url=os.getenv("MOONSHOT_BASE_URL"),
    )

    models = client.models.list().data
    models = {
        m.id.removeprefix("Pro/").split('/', maxsplit=1)[-1].lower(): m.id.removeprefix("Pro/") for m in models
    }
    return {**models, **models_mapping}


if __name__ == '__main__':
    data = get_models_mapping()
    print(bjson(data))
    print(','.join(data))
