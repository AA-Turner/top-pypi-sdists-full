#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : channel
# @Time         : 2024/10/9 18:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.schemas.oneapi import BASE_URL, GROUP_RATIO

headers = {
    'authorization': f'Bearer {os.getenv("CHATFIRE_ONEAPI_TOKEN")}',
    'new-api-user': '1',
    'rix-api-user': '1',
}


async def edit_channel(models, token: Optional[str] = None):
    token = token or os.environ.get("CHATFIRE_ONEAPI_TOKEN")

    models = ','.join(filter(lambda model: model.startswith(("api", "official-api", "ppu", "kling-v")), models))
    models += ",suno-v3"

    payload = {
        "id": 289,
        "type": 1,
        "key": "",
        "openai_organization": "",
        "test_model": "ppu",
        "status": 1,
        "name": "按次收费ppu",
        "weight": 0,
        "created_time": 1717038002,
        "test_time": 1728212103,
        "response_time": 9,
        "base_url": "https://ppu.chatfire.cn",
        "other": "",
        "balance": 0,
        "balance_updated_time": 1726793323,
        "models": models,
        "used_quota": 4220352321,
        "model_mapping": "",
        "status_code_mapping": "",
        "priority": 1,
        "auto_ban": 0,
        "other_info": "",

        "group": "default,openai,chatfire,enterprise",  # ','.join(GROUP_RATIO),
        "groups": ['default']
    }
    headers = {
        'authorization': f'Bearer {token}',
        'rix-api-user': '1'
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.put("/api/channel/", json=payload)
        response.raise_for_status()
        logger.debug(bjson(response.json()))

        payload['id'] = 280
        payload['name'] = '按次收费ppu-cc'
        payload['priority'] = 0
        payload['base_url'] = 'https://ppu.chatfire.cc'

        response = await client.put("/api/channel/", json=payload)
        response.raise_for_status()
        logger.debug(bjson(response.json()))


# todo: 分批
async def create_or_update_channel(api_key, base_url: Optional[str] = "https://api.ffire.cc"):
    if isinstance(api_key, list):
        api_keys = api_key | xgroup(128)  # [[],]
    else:
        api_keys = [[api_key]]

    models = "gemini-1.0-pro-vision-latest,gemini-pro-vision,gemini-1.5-pro-latest,gemini-1.5-pro-001,gemini-1.5-pro-002,gemini-1.5-pro,gemini-1.5-flash-latest,gemini-1.5-flash-001,gemini-1.5-flash-001-tuning,gemini-1.5-flash,gemini-1.5-flash-002,gemini-1.5-flash-8b,gemini-1.5-flash-8b-001,gemini-1.5-flash-8b-latest,gemini-1.5-flash-8b-exp-0827,gemini-1.5-flash-8b-exp-0924,gemini-2.5-pro-exp-03-25,gemini-2.5-pro-preview-03-25,gemini-2.5-flash-preview-04-17,gemini-2.0-flash-exp,gemini-2.0-flash,gemini-2.0-flash-001,gemini-2.0-flash-exp-image-generation,gemini-2.0-flash-lite-001,gemini-2.0-flash-lite,gemini-2.0-flash-lite-preview-02-05,gemini-2.0-flash-lite-preview,gemini-2.0-pro-exp,gemini-2.0-pro-exp-02-05,gemini-2.0-flash-thinking-exp-01-21,gemini-2.0-flash-thinking-exp,gemini-2.0-flash-thinking-exp-1219,learnlm-1.5-pro-experimental,learnlm-2.0-flash-experimental,gemma-3-1b-it,gemma-3-4b-it,gemma-3-12b-it,gemma-3-27b-it,gemini-2.0-flash-live-001"
    nothinking_models = 'gemini-2.5-pro-exp-03-25-nothinking,gemini-2.5-pro-preview-03-25-nothinking,gemini-2.5-flash-preview-04-17-nothinking,gemini-2.0-flash-thinking-exp-01-21-nothinking,gemini-2.0-flash-thinking-exp-nothinking,gemini-2.0-flash-thinking-exp-1219-nothinking'
    models = f"{models},{nothinking_models}"

    payload = {
        # "id": 7493,
        "type": 24,# gemini
        # "key": "AIzaSyCXWV19FRM4XX0KHmpR9lYUz9i1wxQTYUg",
        "openai_organization": "",
        "test_model": "",
        "status": 1,
        "name": "gemini",
        "weight": 0,
        # "created_time": 1745554162,
        # "test_time": 1745554168,
        # "response_time": 575,
        # "base_url": "https://g.chatfire.cn/v1beta/openai/chat/completions",
        # "other": "",
        # "balance": 0,
        # "balance_updated_time": 0,
        "models": models,
        # "used_quota": 0,
        "model_mapping": """{"gemini-2.5-pro-preview-03-25": "gemini-2.5-pro-exp-03-25"}""",
        # "status_code_mapping": "",
        # "priority": 0,
        # "auto_ban": 1,
        # "other_info": "",
        # "settings": "",
        "tag": "gemini",
        # "setting": None,
        # "param_override": "\n {\n \"seed\": null,\n \"frequency_penalty\": null,\n \"presence_penalty\": null,\n \"max_tokens\": null\n }\n ",
        "group": "default",
        "groups": [
            "default"
        ]
    }

    for api_key in tqdm(api_keys):
        payload['key'] = '\n'.join(api_key)
        # logger.debug(payload)
        async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=100) as client:
            response = await client.post("/api/channel/", json=payload)
            response.raise_for_status()
            logger.debug(response.json())


async def delete_channel(id, base_url: Optional[str] = "https://api.ffire.cc"):
    ids = id
    if isinstance(id, str):
        ids = [id]

    for _ids in tqdm(ids | xgroup(256)):
        payload = {
            "ids": list(_ids)
        }
        async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=100) as client:
            response = await client.post(f"/api/channel/batch", json=payload)
            response.raise_for_status()
            logger.debug(response.json())


if __name__ == '__main__':
    from meutils.config_utils.lark_utils import get_series

    # models = "gemini-1.0-pro-vision-latest,gemini-pro-vision,gemini-1.5-pro-latest,gemini-1.5-pro-001,gemini-1.5-pro-002,gemini-1.5-pro,gemini-1.5-flash-latest,gemini-1.5-flash-001,gemini-1.5-flash-001-tuning,gemini-1.5-flash,gemini-1.5-flash-002,gemini-1.5-flash-8b,gemini-1.5-flash-8b-001,gemini-1.5-flash-8b-latest,gemini-1.5-flash-8b-exp-0827,gemini-1.5-flash-8b-exp-0924,gemini-2.5-pro-exp-03-25,gemini-2.5-pro-preview-03-25,gemini-2.5-flash-preview-04-17,gemini-2.0-flash-exp,gemini-2.0-flash,gemini-2.0-flash-001,gemini-2.0-flash-exp-image-generation,gemini-2.0-flash-lite-001,gemini-2.0-flash-lite,gemini-2.0-flash-lite-preview-02-05,gemini-2.0-flash-lite-preview,gemini-2.0-pro-exp,gemini-2.0-pro-exp-02-05,gemini-2.0-flash-thinking-exp-01-21,gemini-2.0-flash-thinking-exp,gemini-2.0-flash-thinking-exp-1219,learnlm-1.5-pro-experimental,learnlm-2.0-flash-experimental,gemma-3-1b-it,gemma-3-4b-it,gemma-3-12b-it,gemma-3-27b-it,gemini-2.0-flash-live-001"
    # nothinking_models = [f"{model}-nothinking" for model in models.split(',') if
    #                      (model.startswith('gemini-2.5') or "thinking" in model)] | xjoin(',')
    #
    # nothinking_models = 'gemini-2.5-pro-exp-03-25-nothinking,gemini-2.5-pro-preview-03-25-nothinking,gemini-2.5-flash-preview-04-17-nothinking,gemini-2.0-flash-thinking-exp-01-21-nothinking,gemini-2.0-flash-thinking-exp-nothinking,gemini-2.0-flash-thinking-exp-1219-nothinking'

    # gemini
    FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=kfKGzt"
    #
    # base_url = "https://api.ffire.cc"
    base_url = "https://usa.chatfire.cn"
    #
    tokens = arun(get_series(FEISHU_URL))
    arun(create_or_update_channel(tokens, base_url))
    # arun(create_or_update_channel(tokens))
    # # arun(delete_channel(range(10000, 20000)))


"""
API_KEY=6c255307-7b4d-4be8-984b-5440a3e867eb
curl --location --request POST 'https://api.ffire.cc/api/channel/' \
--header 'new-api-user: 1' \
--header 'Authorization: Bearer 20ff7099a62f441287f47c86431a7f12' \
--header 'User-Agent: Apifox/1.0.0 (https://apifox.com)' \
--header 'content-type: application/json' \
--data-raw '{
    "type": 8,
    "key": "${API_KEY}",
    "openai_organization": "",
    "test_model": "",
    "status": 1,
    "name": "火山-超刷",
    "weight": 0,
    "created_time": 1746166915,
    "test_time": 1746156171,
    "response_time": 878,
    "base_url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "other": "",
    "balance": 0,
    "balance_updated_time": 0,
    "models": "doubao-1.5-vision-pro-250328,deepseek-v3,deepseek-v3-0324,deepseek-v3-250324,deepseek-v3-8k,deepseek-v3-128k,deepseek-chat,deepseek-chat-8k,deepseek-chat-64k,deepseek-chat-164k,deepseek-chat:function,deepseek-vl2,deepseek-ai/deepseek-vl2,deepseek-r1,deepseek-r1-8k,deepseek-reasoner,deepseek-reasoner-8k,deepseek-r1-250120,deepseek-search,deepseek-r1-search,deepseek-reasoner-search,deepseek-r1-think,deepseek-reasoner-think,deepseek-r1-plus,deepseek-r1:1.5b,deepseek-r1-lite,deepseek-r1-distill-qwen-1.5b,deepseek-r1:7b,deepseek-r1-distill-qwen-7b,deepseek-r1:8b,deepseek-r1-distill-llama-8b,deepseek-r1:14b,deepseek-r1-distill-qwen-14b,deepseek-r1:32b,deepseek-r1-distill-qwen-32b,deepseek-r1:70b,deepseek-r1-distill-llama-70b,deepseek-r1-metasearch,doubao-1-5-pro-32k,doubao-1-5-pro-32k-250115,doubao-1-5-pro-256k,doubao-1-5-pro-256k-250115,doubao-1-5-vision-pro-32k,doubao-1-5-vision-pro-32k-250115,doubao-lite-128k,doubao-lite-32k,doubao-lite-32k-character,doubao-lite-4k,doubao-1.5-lite-32k,doubao-pro-4k,doubao-pro-32k,doubao-pro-32k-character,doubao-pro-128k,doubao-pro-256k,doubao-1.5-pro-32k,doubao-1.5-pro-256k,doubao-1.5-vision-pro-32k,doubao-vision-lite-32k,doubao-vision-pro-32k,doubao-1-5-pro-thinking,doubao-1-5-vision-thinking,doubao-1-5-thinking-pro-250415,doubao-1-5-thinking-pro-vision,doubao-1-5-thinking-pro-vision-250415,doubao-1-5-thinking-pro-m-250415,moonshot-v1-8k,moonshot-v1-32k,moonshot-v1-128k",
    "group": "default,deepseek,volcengine",
    "used_quota": 0,
    "model_mapping": "{\n  \"deepseek-r1\": \"deepseek-r1-250120\",\n  \"deepseek-reasoner\": \"deepseek-r1-250120\",\n  \"deepseek-v3-0324\": \"deepseek-v3-250324\",\n  \"deepseek-v3\": \"deepseek-v3-250324\",\n  \"deepseek-chat\": \"deepseek-v3-250324\",\n  \"doubao-1-5-vision-pro-32k\": \"doubao-1-5-vision-pro-32k-250115\",\n  \"doubao-1.5-vision-pro-32k\": \"doubao-1-5-vision-pro-32k-250115\",\n  \"doubao-pro-32k\": \"doubao-1-5-pro-32k-250115\",\n  \"doubao-pro-256k\": \"doubao-1-5-pro-256k-250115\",\n  \"doubao-1.5-lite-32k\": \"doubao-1-5-lite-32k-250115\",\n  \"doubao-lite-4k\": \"doubao-1-5-lite-32k-250115\",\n  \"doubao-lite-32k\": \"doubao-1-5-lite-32k-250115\",\n  \"doubao-lite-128k\": \"doubao-lite-128k-240828\",\n  \"doubao-pro-128k\": \"doubao-1-5-pro-256k-250115\",\n  \"doubao-1.5-lite\": \"doubao-1-5-lite-32k-250115\",\n  \"doubao-vision-lite-32k\": \"doubao-vision-lite-32k-241015\",\n  \"doubao-vision-pro-32k\": \"doubao-1-5-vision-pro-32k-250115\",\n  \"doubao-1.5-pro-32k\": \"doubao-1-5-pro-32k-250115\",\n  \"doubao-1.5-pro-256k\": \"doubao-1-5-pro-256k-250115\",\n  \"doubao-1-5-thinking-pro\": \"doubao-1-5-thinking-pro-250415\",\n  \"doubao-1-5-thinking-pro-vision\": \"doubao-1-5-thinking-pro-vision-250415\"\n}",
    "status_code_mapping": "",
    "priority": 999,
    "auto_ban": 1,
    "other_info": "",
    "settings": "",
    "tag": "火山",
    "setting": null,
    "param_override": null,
    "groups": [
        "default",
        "deepseek",
        "volcengine"
    ]
}'
"""