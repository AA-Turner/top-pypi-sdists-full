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

        "group": "default,openai,china,chatfire,enterprise",  # ','.join(GROUP_RATIO),
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

    payload = {
        # "id": 7493,
        "type": 8,
        # "key": "AIzaSyCXWV19FRM4XX0KHmpR9lYUz9i1wxQTYUg",
        "openai_organization": "",
        "test_model": "",
        "status": 1,
        "name": "gemini",
        "weight": 0,
        # "created_time": 1745554162,
        # "test_time": 1745554168,
        # "response_time": 575,
        "base_url": "https://g.chatfire.cn/v1beta/openai/chat/completions",
        # "other": "",
        # "balance": 0,
        # "balance_updated_time": 0,
        "models": "gemini-1.0-pro-vision-latest,gemini-pro-vision,gemini-1.5-pro-latest,gemini-1.5-pro-001,gemini-1.5-pro-002,gemini-1.5-pro,gemini-1.5-flash-latest,gemini-1.5-flash-001,gemini-1.5-flash-001-tuning,gemini-1.5-flash,gemini-1.5-flash-002,gemini-1.5-flash-8b,gemini-1.5-flash-8b-001,gemini-1.5-flash-8b-latest,gemini-1.5-flash-8b-exp-0827,gemini-1.5-flash-8b-exp-0924,gemini-2.5-pro-exp-03-25,gemini-2.5-pro-preview-03-25,gemini-2.5-flash-preview-04-17,gemini-2.0-flash-exp,gemini-2.0-flash,gemini-2.0-flash-001,gemini-2.0-flash-exp-image-generation,gemini-2.0-flash-lite-001,gemini-2.0-flash-lite,gemini-2.0-flash-lite-preview-02-05,gemini-2.0-flash-lite-preview,gemini-2.0-pro-exp,gemini-2.0-pro-exp-02-05,gemini-2.0-flash-thinking-exp-01-21,gemini-2.0-flash-thinking-exp,gemini-2.0-flash-thinking-exp-1219,learnlm-1.5-pro-experimental,learnlm-2.0-flash-experimental,gemma-3-1b-it,gemma-3-4b-it,gemma-3-12b-it,gemma-3-27b-it,gemini-2.0-flash-live-001",
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
        "group": "default,gemini,gemini-pro",
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

    FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=kfKGzt"

    tokens = arun(get_series(FEISHU_URL))
    # arun(create_or_update_channel(tokens[:1]))
    arun(create_or_update_channel(tokens))

    # arun(delete_channel(range(10000, 20000)))
