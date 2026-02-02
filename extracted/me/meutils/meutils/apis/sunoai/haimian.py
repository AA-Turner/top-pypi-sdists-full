#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : haimian
# @Time         : 2024/8/2 15:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json

from meutils.pipe import *
from meutils.schemas.haimian_types import HaimianRequest, HaimianCustomRequest
from meutils.schemas.task_types import Task
from meutils.apis.proxy.ips import get_one_proxy

from meutils.decorators.retry import retrying
from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=ax1BQH"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)

# url = "https://www.haimian.com/jd/api/v1/generate/lyric2song?app_name=goat&aid=588628&app_id=588628&app_version=1.0.0.397&channel=online&region=CN&device_platform=web&msToken=hXy3dUqC1FoEKSDhn7h9el2p5Iegrf86G-71wZAL10-HEZxjZWHZdb2iZCsMomcIymhvKkFNFlj6SW0q6M6x-mw3P2UPKMHp73nUYMouCfpdo-_0paLZlgj9XCjCAA%3D%3D&a_bogus=QvW0BfwvDiVpDDmR5RoLfY3quOWwYdR50ajLMDgPEpBKOg39HMOl9exEoNs4RkbjN4%2FkIejjy4hbO3xprQQJ8Hwf7Wsx%2F2CZs640t-Pg-nSSs1feeLbQrsJx-kz5Feep5JV3EcvhqJKczbEk09Cn5iIlO6ZCcHgjxiSmtn3Fv-S%3D"

url = "https://www.haimian.com/jd/api/v1/generate/lyric2song"
BASE_URL = "https://www.haimian.com/jd/api/v1"


# www.haimian.com => "all.ffire.cc/haimian"

# {
#     "status_code": 10000008,
#     "status_info": {
#         "status_msg": "已超过每天音乐生成上限，请明天再试",
#         "ts": 0,
#         "log_id": ""
#     },
#     "data": null
# }

@retrying()
async def create_task(request: HaimianRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)

    headers = {
        'Cookie': token,
        # 'msToken': '7i-GsUjnIpzgFr47RfcSu-SHno90VQJNNq-G7UZuTGZkh6kG8WKiIPKRN6n3pp8YCVQhYQNbWq3mDk_FqEd8oCtiypv8tTQo6QBinmFRbRp3IcHPvX4mybl6zXK0QQ==',
        # 'fg_uid': 'RID20241125145034C2DBB2C389869EC7EFBD',

        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }
    params = {
        # 'app_name': 'goat',
        # 'aid': '588628',
        # 'app_id': '588628',
        # 'app_version': '1.0.0.731',
        # 'channel': 'online',
        # 'region': 'CN',
        # 'device_platform': 'web',
        # 'msToken': '7i-GsUjnIpzgFr47RfcSu-SHno90VQJNNq-G7UZuTGZkh6kG8WKiIPKRN6n3pp8YCVQhYQNbWq3mDk_FqEd8oCtiypv8tTQo6QBinmFRbRp3IcHPvX4mybl6zXK0QQ==',
        # 'a_bogus': 'mXWZQ5gvDiVkhDEm5A5LfY3quu1gY0tr0ajLMDgPB%2FxY-y39HMP09exYtXz4TyEjNG%2FpIejjy4hbT3KkrQQrMZwf9WhE%2F2ApsDSDeM32soDys1feejusnUhimkU-taBB-k1UrO7hqvKcKbup09Cj4vIAP6ZeaHgjxiSmtn3FvlL%3D'
    }
    payload = request.model_dump()
    # proxies = await get_one_proxy()
    proxies = {
        # 'http://': 'http://154.12.35.201:38443', 'https://': 'http://154.12.35.201:38443'
    }
    logger.debug(proxies)
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30,
                                 proxies=proxies) as client:
        response = await client.post(f"/generate/lyric2song/", params=params, json=payload)

        response.raise_for_status()
        logger.info(response.text)
        logger.info(response.status_code)

        data = response.json()['data']
        task_ids = jsonpath.jsonpath(data, "$..tasks..task_id")
        return Task(id=f"haimian-{task_ids | xjoin(',')}", data=data, system_fingerprint=token)


async def get_task(task_id, token):
    task_id = task_id.split("-")[-1]
    params = [('task_ids', task_id) for task_id in task_id.split(',')]

    headers = {
        'Cookie': token,
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.get("/generate/tasks/info", params=params)
        if response.is_success:
            return response.json()


@alru_cache(ttl=30)
@retrying()
async def generate_lyrics(prompt: str = "写一首夏日晚风的思念的歌", token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)

    payload = {
        "input": prompt,
        "type": 0
    }
    headers = {
        'Cookie': token,
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.post("/generate/lyric_tool_stream", json=payload)
        if response.is_success:
            return json_repair.repair_json(response.text, return_objects=True)
        # response: httpx.Response
        # async with client.stream("POST", "/generate/lyric_tool_stream", json=payload) as response:
        #     async for i in response.aiter_lines():
        #         print(i)


if __name__ == '__main__':
    token = None
    request = HaimianRequest(
        prompt="古风歌曲，男生唱的，乐器：古筝、箫、二胡、木鱼、鼓。\n演唱风格：空灵婉转、情感投入。\n歌词高级的古风感，整体构造成仙气飘飘的感觉乐器：琵琶、笛、扬琴、编钟。\n演唱风格：柔情细腻、悠远绵长。",
        batch_size=3
    )
    arun(create_task(request, token))

    # task_id = "haimian-WlAPDQggva"
    # token = arun(get_next_token_for_polling(FEISHU_URL))
    # arun(get_task(task_id, token))

    # arun(generate_lyrics())
