#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : announcement
# @Time         : 2025/9/23 10:19
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.hash_utils import murmurhash
from meutils.schemas.oneapi import BASE_URL, GROUP_RATIO
from meutils.schemas.oneapi._types import ChannelInfo
from meutils.llm.clients import zhipuai_client
from json_repair import repair_json
headers = {
    'authorization': f'Bearer {os.getenv("CHATFIRE_ONEAPI_TOKEN")}',
    'new-api-user': '1',
    'rix-api-user': '1',
}


async def create_announcement():
    payload = {
        "title": "公告标题",
        "description": "公告描述",
        "content": "MARKDOWN格式正文",
        "tag": "重要,更新,紧急,系统,通知,维护,活动,优惠【不超过两个词】",

        # "type": "system_push",
        # "extra": "",
        # "status": "published",
        # "read_auth": "all"
    }
    if md_content := get_resolve_path("announcement.md", __file__).read_text():

        completion = await zhipuai_client.chat.completions.create(
            model="glm-4.5-flash",
            messages=[
                {"role": "system", "content": f"将MARKDOWN字符串转换为json格式的字符串，json格式为：{payload}"},
                {"role": "user", "content": f"MARKDOWN字符串：{md_content}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        payload = completion.choices[0].message.content
        logger.debug(payload)
        payload = repair_json(payload, return_objects=True)

    base_url = "https://api.chatfire.cn"
    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=30) as client:
        response = await client.post("/api/announcement/", json=payload)
        response.raise_for_status()

        data = response.json()
        logger.debug(bjson(data))
        return data


if __name__ == '__main__':
    payload = {
        "title": "公告标题",
        "description": "公告描述",
        "content": "# MARKDOWN",
        "tag": "重要,更新,紧急,系统,通知,维护,活动,优惠",
        # "type": "system_push",
        # "extra": "",
        # "status": "published",
        # "read_auth": "all"
    }
    arun(create_announcement())
