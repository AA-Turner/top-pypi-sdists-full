#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : deepl
# @Time         : 2026/2/9 15:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import logging

from meutils.pipe import *
from openai import AsyncClient
from meutils.schemas.openai_types import CompletionRequest, chat_completion
from meutils.str_utils import parse_command_string

base_url = "http://172.93.108.217:1188/v1"
api_key = "helloxxx"


class Completions(object):

    def __init__(self, api_key: str):
        base_url, api_key = api_key.split("|")
        self.client = AsyncClient(
            base_url=base_url,
            api_key=api_key
        )

    async def create(self, request: CompletionRequest):
        target_lang = "ZH"
        params = {}
        if '_' in request.model:
            _, target_lang = request.model.split('_', maxsplit=1)

        else:
            params = parse_command_string(request.last_user_content)
            logger.debug(f"Parsed parameters: {params}")
            params['text'] = params.pop('prompt', request.last_user_content)

        payload = {
            "text": request.last_user_content,
            "source_lang": 'auto',
            "target_lang": target_lang,

            **params
        }

        response = await self.client.post(path="/translate", body=payload, cast_to=object)

        if request.response_format == "json":
            data = json.dumps(response, indent=4, ensure_ascii=False)
        else:
            data = response.get("data", "") or response.get("alternatives", [""])[0]
        logger.debug(bjson(response))

        yield data


if __name__ == '__main__':
    text = '中国人为啥爱吃农村大席'
    text = '中国人为啥爱吃农村大席 --target_lang EN'

    # text = [text] * 100
    base_url = "http://172.93.108.217:1188/v1"
    api_key = "helloxxx"
    api_key = f"{base_url}|{api_key}"
    model = "ZH"
    model = "deepl-zh"

    request = CompletionRequest(
        model=model,
        messages=[{"role": "user", "content": text}],
    )

    _ = arun(Completions(api_key=api_key).create(request))
