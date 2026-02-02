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
from meutils.str_utils.json_utils import json_path
from meutils.hash_utils import murmurhash
from meutils.schemas.oneapi import BASE_URL, GROUP_RATIO
from meutils.schemas.oneapi._types import ChannelInfo
from meutils.schemas.db.oneapi_types import OneapiChannel

from meutils.db.orm import update_or_insert

headers = {
    'authorization': f'Bearer {os.getenv("CHATFIRE_ONEAPI_TOKEN")}',
    'new-api-user': '1',
    'rix-api-user': '1',
}

filter_kwargs = {
    # "key": "gpoH1z3G6nHovD8MY40i6xx5tsC1vbh7B3Aao2jmejYNoKhv",
    # "key": "610d41b8-0b6e-4fba-8439-f5178b733f3a",
    "id": 21249,
}


# async def update_channel(id: int, base_url: str):
#     arun(update_or_insert(OneapiChannel, filter_kwargs, update_fn))
#
#     filter_kwargs = {
#         "id": "1",
#     }
#
#     async def update_fn(data):
#         data.key = "k1\nk2\nk3"
#         return data
#
#     async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=30) as client:
#         response = await client.get(f"/api/channel/{id}")
#         response.raise_for_status()
#
#         data = response.json()
#         logger.debug(bjson(data))
#         return data


async def manage_multi_key(id: int, base_url: str, action: str = "enable_all_keys", **kwargs) -> ChannelInfo:
    # "disable_all_keys"
    payload = {
        "channel_id": id,
        "action": action,
        **kwargs
    }  #
    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=30) as client:
        response = await client.post("/api/channel/multi_key/manage", json=payload)
        response.raise_for_status()

        data = response.json()
        # logger.debug(bjson(data))
        return data


async def get_channel_keys(id: int, base_url: str, status: int = 1, page_size: int = 10240) -> ChannelInfo:
    payload = {"channel_id": id, "action": "get_key_status", "page": 1, "page_size": page_size, "status": status}

    data = await manage_multi_key(id=-1, base_url=base_url, **payload)

    if data := data['data']:
        return pd.DataFrame(data['keys'])


async def get_channel_info(id: int, base_url: str, response_format: Optional[str] = None):
    params = {"keyword": id}  # keyword=21222&group=&model=&id_sort=true&tag_mode=false&p=1&page_size=100

    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=30) as client:
        response = await client.get("/api/channel/search", params=params)
        response.raise_for_status()

        data = response.json()
        logger.debug(bjson(data))

        if (items := data.get("data", {}).get("items", [])) and (item := items[0]):
            if not response_format: return item

            if response_format == "status":  # multi_key_status
                return item.get("status") == 1  # status==1 是正常

            elif item.get("status") == 1 and not item.get("channel_info", {}).get("multi_key_status_list"):
                logger.debug(f"渠道 {id} 渠道全key正常")
                return True


async def edit_channel(models, token: Optional[str] = None):
    token = token or os.environ.get("CHATFIRE_ONEAPI_TOKEN")

    models = ','.join(filter(lambda model: model.startswith(("api", "official-api", "ppu", "kling-v")), models))
    models += ",suno-v3,indextts-1.5,cosyvoice2,step-audio-tts-3b,f5-tts"

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


async def exist_channel(
        request: ChannelInfo,

        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
):
    if request.id is None:
        return False
    base_url = base_url or "https://api.chatfire.cn"
    api_key = api_key or os.getenv("CHATFIRE_ONEAPI_TOKEN")

    headers = {
        'authorization': f'Bearer {api_key}',
        'new-api-user': '1',
        'rix-api-user': '1',
    }
    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=100) as client:
        if "api.chatfire.cn" in base_url:
            path = "/api/channel/"
            params = {"channel_id": request.id}
        else:
            path = "/api/channel/search"
            params = {"keyword": request.id}
        response = await client.get(path, params=params)
        response.raise_for_status()

        logger.debug(bjson(response.json()))

        if items := response.json()['data']['items']:
            _ = [item for item in items if item['id'] == request.id]
            # logger.debug(_)

            return _
        else:
            logger.debug(f"渠道不存在：{request.id}")
            return False


async def create_or_update_channel(
        request: ChannelInfo,

        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
):
    assert base_url, "base_url 不能为空"

    if request.id and isinstance(request.id, str):  # 批量更新
        ids = []
        if "," in request.id:
            ids = map(int, request.id.split(","))
        elif ':' in request.id:
            start, end = map(int, request.id.split(":"))
            ids = range(start, end)

        request_list = []
        for i, k in zip(ids, request.key.split()):  # api_key不为空, 如果id很多是否考虑复制 api_key不为空
            _request = request.copy()
            _request.id = i
            _request.key = k
            request_list.append(_request)

        tasks = [create_or_update_channel(r, base_url, api_key) for r in request_list]
        return await asyncio.gather(*tasks)

    method = "post"
    if await exist_channel(request, base_url, api_key):
        logger.debug(f"渠道已存在，跳过创建：{request.id}")
        method = "put"

    # 新创建的优先级低，保证旧key刷的时间更长
    request.priority = request.priority or int(1000 - (time.time() - time.time() // 1000 * 1000))

    api_key = api_key or os.getenv("CHATFIRE_ONEAPI_TOKEN")
    headers = {
        'authorization': f'Bearer {api_key}',
        'new-api-user': '1',
        'rix-api-user': '1',
    }
    payload = request.model_dump(exclude_none=True)
    if "api.chatfire.cn" not in base_url and method == "post":
        payload = {
            "mode": "single",
            "channel": payload
        }

    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=100) as client:
        response = await client.request(method, "/api/channel/", json=payload)
        # logger.debug(response.text)
        response.raise_for_status()

        data = response.json()
        logger.debug(bjson(data))
        if (data := data.get("data")) and data['channel_info']['is_multi_key']:
            await manage_multi_key(data['id'], base_url=base_url)

        return response.json()


async def create_or_update_channel_for_gemini(api_key, base_url: Optional[str] = "https://api.ffire.cc"):
    if isinstance(api_key, list):
        api_keys = api_key | xgroup(128)  # [[],]
    else:
        api_keys = [[api_key]]

    models = "gemini-2.5-flash-preview-05-20,gemini-1.5-flash-latest,gemini-1.5-flash-001,gemini-1.5-flash-001-tuning,gemini-1.5-flash,gemini-1.5-flash-002,gemini-1.5-flash-8b,gemini-1.5-flash-8b-001,gemini-1.5-flash-8b-latest,gemini-1.5-flash-8b-exp-0827,gemini-1.5-flash-8b-exp-0924,gemini-2.5-flash-preview-04-17,gemini-2.0-flash-exp,gemini-2.0-flash,gemini-2.0-flash-001,gemini-2.0-flash-exp-image-generation,gemini-2.0-flash-lite-001,gemini-2.0-flash-lite,gemini-2.0-flash-lite-preview-02-05,gemini-2.0-flash-lite-preview,gemini-2.0-flash-thinking-exp-01-21,gemini-2.0-flash-thinking-exp,gemini-2.0-flash-thinking-exp-1219,learnlm-2.0-flash-experimental,gemma-3-1b-it,gemma-3-4b-it,gemma-3-12b-it,gemma-3-27b-it,gemini-2.0-flash-live-001"
    nothinking_models = 'gemini-2.5-flash-preview-05-20-nothinking,gemini-2.5-flash-preview-04-17-nothinking,gemini-2.0-flash-thinking-exp-01-21-nothinking,gemini-2.0-flash-thinking-exp-nothinking,gemini-2.0-flash-thinking-exp-1219-nothinking'
    models = f"{models},{nothinking_models}"

    payload = {
        # "id": 7493,
        "type": 24,  # gemini
        # "key": "AIzaSyCXWV19FRM4XX0KHmpR9lYUz9i1wxQTYUg",
        "openai_organization": "",
        "test_model": "",
        "status": 1,
        "name": "gemini",

        "priority": murmurhash(api_key, bins=3),
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


async def update_channel(id: int, base_url: str, **kwargs):
    """只更新keys"""

    # key_mode: Optional[Literal['append', 'replace']] = None  # none是覆盖

    if channel_info := await get_channel_info(id, base_url):
        channel_info = {**channel_info, **kwargs}

        async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=100) as client:
            response = await client.request("PUT", "/api/channel/", json=channel_info)
            response.raise_for_status()

            return response.json()


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
    base_url = "https://api.ffire.cc"
    # base_url = "https://usa.chatfire.cn"
    base_url = "https://api.chatfire.cn"

    # tokens = arun(get_series(FEISHU_URL))  # [:5]
    # arun(create_or_update_channel(tokens, base_url))
    # arun(create_or_update_channel(tokens))
    # # arun(delete_channel(range(10000, 20000)))
    key = "KEY\nKEY2\nKEY2\nKEY2\nKEY2"
    # request = ChannelInfo(id = 1, name='xx', key=key)
    # request = ChannelInfo(id=21223, key=key, used_quota=0.001)
    request = ChannelInfo(id=29483, key=key, used_quota=0.001,
                          # key_mode="append"
                          )

    request = ChannelInfo(id=29499, key=key, type=45)

    # arun(create_or_update_channel(request, base_url=base_url))
    #
    # arun(exist_channel(request, base_url=base_url))

    # arun(get_channel_info(21222, base_url=base_url))
    # arun(get_channel_info(29495, base_url=base_url, response_format="status"))
    # arun(get_channel_info(29495, base_url=base_url, response_format="multi_key_status"))

    # arun(delete_channel(range(10015, 10032), base_url=base_url))

    # arun(manage_multi_key(29499, base_url=base_url))

    # arun(update_channel(21249, base_url=base_url, key=key, key_mode="append"))

    # payload = {"channel_id": 21385, "action": "get_key_status", "page": 1, "page_size": 1024, "status": 1}
    #
    # data = arun(manage_multi_key(21385, base_url=base_url, **payload))
    #
    # dff = pd.DataFrame(data['data']['keys'])

    df = arun(get_channel_keys(21385, base_url))
