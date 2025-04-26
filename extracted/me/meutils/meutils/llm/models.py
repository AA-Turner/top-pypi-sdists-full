#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : models
# @Time         : 2025/4/14 11:09
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from meutils.llm.clients import OpenAI, AsyncOpenAI


async def check_token(api_key):
    try:
        client = AsyncOpenAI(
            base_url=os.getenv("OPENROUTER_BASE_URL"),
            api_key=api_key,
        )
        r = await client.chat.completions.create(
            messages=[{'role': 'user', 'content': 'hi'}],
            model="google/gemma-3-1b-it:free",
            max_tokens=1,
            stream=False
        )
        logger.debug(r)
        return True

    except Exception as e:
        logger.error(e)
        return False


async def check_token_for_together(api_key):
    model = "meta-llama/Llama-Vision-Free"
    try:
        client = AsyncOpenAI(
            base_url=os.getenv("TOGETHER_BASE_URL"),
            api_key=api_key,
        )
        r = await client.chat.completions.create(
            messages=[{'role': 'user', 'content': 'hi'}],
            model=model,
            max_tokens=1,
            stream=False
        )
        logger.debug(r)
        return True

    except Exception as e:
        logger.error(e)
        return False


def get_openrouter_models():
    models = OpenAI(base_url=os.getenv("OPENROUTER_BASE_URL"), api_key='xx').models.list()

    data = {}
    for model in models.data:
        if model.id.lower().endswith(':free'):
            _model = model.id.lower().removesuffix(":free").split('/')[-1]
            data[_model] = f"""{_model}=={model.id}"""

    print(data | xjoin(","))
    return data


def get_together_models():
    client = OpenAI(base_url=os.getenv("TOGETHER_BASE_URL"), api_key=os.getenv("TOGETHER_API_KEY"))
    models = client.get("models", cast_to=object)
    # logger.debug(bjson(models))

    data = {}
    for model in models:
        if model['id'].lower().endswith('-free'):
            _model = model['id'].lower().removesuffix("-free").split('/')[-1]
            data[_model] = f"""{_model}=={model['id']}"""

    print(data | xjoin(","))
    return data


if __name__ == '__main__':
    from meutils.config_utils.lark_utils import get_series

    # print(bjson(get_openrouter_models()))
    # print(bjson(get_together_models()))

    # arun(check_token("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"))

    # tokens = arun(get_series("https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=gGFIXb"))
    #
    # r = []
    # for i in tokens:
    #     if not arun(check_token(i)):
    #         print(i)
    #         r.append(i)

    feishu_url = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=tEsIyw"

    tokens = arun(get_series(feishu_url))

    r = []
    rr = []
    for i in tokens:
        if not arun(check_token_for_together(i)):
            print(i)
            r.append(i)
        else:
            rr.append(i)

    # arun(check_token_for_together("1581bb1c605501c96569cf9a24aafa7361752697a23475cdf8f2c3fe8a488292"))
