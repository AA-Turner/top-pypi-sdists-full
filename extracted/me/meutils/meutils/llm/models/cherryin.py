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

}


def get_models_mapping(startswith: str=""):
    client = OpenAI(
        api_key=os.getenv("CHERRYIN_API_KEY"),
        base_url=os.getenv("CHERRYIN_BASE_URL"),
    )

    models = client.models.list().data
    models = {
        m.id.removeprefix("Pro/").split('/', maxsplit=1)[-1].lower().strip("(free)"): m.id.removeprefix("Pro/") for m in models
        if any(i in m.id.lower() for i in {"stable-diffusion", "free"})
    }
    if startswith:
        models = {k: v for k, v in models.items() if k.startswith(startswith)}
        return models

    return {**models, **models_mapping}


if __name__ == '__main__':
    startswith = ""
    # startswith = "ling"

    data = get_models_mapping(startswith)
    print(bjson(data))
    print(','.join(data))
