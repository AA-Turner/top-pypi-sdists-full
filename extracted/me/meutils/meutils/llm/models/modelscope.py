#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : modelscope
# @Time         : 2025/8/22 22:47
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :



from meutils.pipe import *
from openai import OpenAI

models_mapping = {
    "flux-kontext-dev": "MusePublic/FLUX.1-Kontext-Dev",
    # "flux-kontext-dev": "black-forest-labs/FLUX.1-Kontext-dev",

    "flux.1-krea-dev": "black-forest-labs/FLUX.1-Krea-dev",

    "kimi-k2-0711-preview": "moonshotai/Kimi-K2-Instruct",
    "kimi-k2-250711": "moonshotai/Kimi-K2-Instruct",
    "kimi-k2-0905-preview": "moonshotai/Kimi-K2-Instruct-0905",
    "kimi-k2-250905": "moonshotai/Kimi-K2-Instruct-0905",

    "majicflus_v1": "MAILAND/majicflus_v1",
    "deepseek-reasoner": "deepseek-ai/DeepSeek-R1-0528",

    "deepseek-r1": "deepseek-ai/DeepSeek-R1-0528",
    "deepseek-r1-0528": "deepseek-ai/DeepSeek-R1-0528",
    "deepseek-r1-250528": "deepseek-ai/DeepSeek-R1-0528",
    "deepseek-chat": "deepseek-ai/DeepSeek-V3",
    "deepseek-v3": "deepseek-ai/DeepSeek-V3",
    "deepseek-v3-0324": "deepseek-ai/DeepSeek-V3",
    "deepseek-v3-250324": "deepseek-ai/DeepSeek-V3",
    "deepseek-v3-1-250821": "deepseek-ai/DeepSeek-V3.1",

    "deepseek-r1-distill-qwen-14b": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
    "deepseek-r1-distill-qwen-32b": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "deepseek-r1-distill-llama-70b": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
    "qwen2.5-coder-32b-instruct": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "qwen2.5-coder-14b-instruct": "Qwen/Qwen2.5-Coder-14B-Instruct",
    "qwen2.5-coder-7b-instruct": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "qwen2.5-72b-instruct": "Qwen/Qwen2.5-72B-Instruct",
    "qwen2.5-32b-instruct": "Qwen/Qwen2.5-32B-Instruct",
    "qwen2.5-14b-instruct": "Qwen/Qwen2.5-14B-Instruct",
    "qwen2.5-7b-instruct": "Qwen/Qwen2.5-7B-Instruct",
    "qwq-32b-preview": "Qwen/QwQ-32B-Preview",
    "qvq-72b-preview": "Qwen/QVQ-72B-Preview",
    "qwen2-vl-7b-instruct": "Qwen/Qwen2-VL-7B-Instruct",
    "qwen2.5-14b-instruct-1m": "Qwen/Qwen2.5-14B-Instruct-1M",
    "qwen2.5-7b-instruct-1m": "Qwen/Qwen2.5-7B-Instruct-1M",
    "qwen2.5-vl-3b-instruct": "Qwen/Qwen2.5-VL-3B-Instruct",
    "qwen2.5-vl-7b-instruct": "Qwen/Qwen2.5-VL-7B-Instruct",
    "qwen2.5-vl-72b-instruct": "Qwen/Qwen2.5-VL-72B-Instruct",
    "qwq-32b": "Qwen/QwQ-32B",
    "qwen2.5-vl-32b-instruct": "Qwen/Qwen2.5-VL-32B-Instruct",
    "qwen3-0.6b": "Qwen/Qwen3-0.6B",
    "qwen3-1.7b": "Qwen/Qwen3-1.7B",
    "qwen3-4b": "Qwen/Qwen3-4B",
    "qwen3-14b": "Qwen/Qwen3-14B",
    "qwen3-30b-a3b": "Qwen/Qwen3-30B-A3B",
    "qwen3-32b": "Qwen/Qwen3-32B",
    "qwen3-235b-a22b": "Qwen/Qwen3-235B-A22B",
    "qwen3-coder-480b-a35b-instruct": "Qwen/Qwen3-Coder-480B-A35B-Instruct",
    "qwen3-235b-a22b-instruct-2507": "Qwen/Qwen3-235B-A22B-Instruct-2507",

    "qwen3-vl-plus": "Qwen/Qwen3-VL-235B-A22B-Instruct",
    "qwen3-vl-235b-a22b": "Qwen/Qwen3-VL-235B-A22B-Instruct",

}


def get_models_mapping():
    client = OpenAI(
        api_key=os.getenv("MODELSCOPE_API_KEY"),
        # api_key="0e11d36f-2eb3-4c47-a1b4-e4be4e365a68",
        base_url=os.getenv("MODELSCOPE_BASE_URL"),
    )

    models = client.models.list().data
    models = {
        m.id.split('/', maxsplit=1)[-1].lower(): m.id for m in models

        if any(i.lower() not in m.id.lower() for i in {"qwen-image", 'Kimi-K2'})
    }
    # logger.debug(models)
    return {**models, **models_mapping}


if __name__ == '__main__':
    models = get_models_mapping()
    print(bjson(models))
    print(','.join(models))
