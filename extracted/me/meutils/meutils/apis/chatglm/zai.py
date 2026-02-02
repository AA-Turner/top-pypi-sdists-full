#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : z.py
# @Time         : 2025/8/19 08:32
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo bug英文少空格


from meutils.pipe import *
from meutils.caches import rcache
from meutils.db.redis_db import redis_aclient

from openai import AsyncOpenAI
from meutils.llm.openai_utils import to_openai_params, create_chat_completion_chunk

from meutils.schemas.openai_types import CompletionRequest, chat_completion_chunk, chat_completion

from meutils.decorators.retry import retrying
from meutils.config_utils.lark_utils import get_next_token_for_polling

from fake_useragent import UserAgent

ua = UserAgent()

BASE_URL = "https://chat.z.ai/api"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=x3TJrE"

MODEL="glm-4.7"
class Completions(object):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def create(self, request: CompletionRequest):
        token = self.api_key or await get_next_token_for_polling(FEISHU_URL)

        chat_id = str(uuid.uuid4())
        payload = {
            "id": chat_id,
            "chat_id": chat_id,
            "model": request.model,

            "stream": True,

            "params": {},
            "features": {
                "image_generation": False,
                "web_search": False,
                "auto_web_search": False,
                "preview_mode": False,
                "flags": [],
                "features": [
                    {
                        "type": "mcp",
                        "server": "vibe-coding",
                        "status": "hidden"
                    },
                    {
                        "type": "mcp",
                        "server": "ppt-maker",
                        "status": "hidden"
                    },
                    {
                        "type": "mcp",
                        "server": "image-search",
                        "status": "hidden"
                    }
                ],
                "enable_thinking": request.enable_thinking or False
            },

            "background_tasks": {
                "title_generation": False,
                "tags_generation": False
            }
        }

        payload = {**request.model_dump(), **payload}

        data = to_openai_params(payload)

        # todo 代理
        params = {"timestamp": str(int(time.time()*1000)), "signature_timestamp": str(int(time.time()*1000)),}
        default_headers = {
            "X-FE-Version": "prod-fe-1.0.69",
            "X-Signature": "12fd867a781510c83c8a18d81f3a3a304e49c5e6c9cac9f004316a530b1bde1a",
        }

        client = AsyncOpenAI(base_url=BASE_URL, api_key=token, default_headers=default_headers, default_query=params)
        response = await client.chat.completions.create(**data)
        response = self.do_response(response, request.stream)

        # async for i in response:
        #     logger.debug(i)

        return response

    async def do_response(self, response, stream: bool):
        usage = None
        nostream_content = ""
        nostream_reasoning_content = ""
        chat_completion_chunk.model =MODEL
        async for i in response:
            # print(i)

            delta_content = (
                    i.data.get("delta_content", "").removeprefix(
                        '<details type="reasoning" done="false">\n<summary>Thinking…</summary>\n> ')
                    or i.data.get("edit_content", "").split("</details>\n")[-1]
            )

            if i.data.get("phase") == "thinking":
                nostream_reasoning_content += delta_content
                chat_completion_chunk.choices[0].delta.reasoning_content = delta_content

            elif i.data.get("phase") == "answer":
                nostream_content += delta_content
                chat_completion_chunk.choices[0].delta.content = delta_content

            else:
                logger.debug(bjson(i))

            if stream:
                yield chat_completion_chunk

            usage = usage or i.data.get("usage", "")

        if not stream:
            chat_completion.choices[0].message.content = nostream_content
            chat_completion.choices[0].message.reasoning_content = nostream_reasoning_content
            chat_completion.usage = usage
            chat_completion.model = MODEL
            yield chat_completion

    async def upload(self, request: CompletionRequest):  # todo
        files = [
            ('file', (
                'deepinfra.py',
                open('/Users/betterme/PycharmProjects/AI/MeUtils/meutils/apis/images/deepinfra.py', 'rb'),
                'application/octet-stream')
             )
        ]

        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=120) as client:
            response = await client.post("/v1/files", files=files)
            response.raise_for_status()
            return response.json()


if __name__ == '__main__':
    token = """
    eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjUxZmNjMWZmLWRlMGYtNDgyYi1hOTAzLTMyMGM0OGJhZTQ2MiIsImVtYWlsIjoiYjZ5bnI5bjlvQG1haWwueGl1dmkuY24ifQ.286d3lCg-p9QUHEBWusC2Oi_a3WgeKtlTcbs1tfXsbW2KatRNxlbtUIeDQBPY5u-Fc3uhoU5ao0DJ4Ww_9dXZw
    """.strip()

    request = CompletionRequest(
        model="GLM-4-6-API-V1",
        messages=[
            {
                "role": "system",
                "content": "你是gpt",

            },
            {
                "role": "user",
                # "content": [{"type": "text", "text": "周杰伦"}],
                # "content": "你是谁",
                "content": "are you ok?",

            }
        ],
        stream=True,

        enable_thinking=True

    )


    async def main():
        response = await Completions(token).create(request)
        async for i in response:
            print(i)


    arun(main())

    # from openai import OpenAI
    #
    # token = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImI0YThkMTI5LWY2YzgtNDM5Mi1iYzlhLWEyNjM1Nzg0ZDM5MyIsImVtYWlsIjoiemJqZ2NlZ2NsbkB0aXRrLnVrIn0.KyRWoGT2vdGN6nPUB5ctU2UkMMtW1XzxVc5KlyWZpIjPqhjHO3gBShFil9j0CG82bdQtA5nDWHIxqzvDcCp-sg"
    #
    # client = OpenAI(base_url="https://chat.z.ai/api/v1/files", api_key=token)

    # response = client.files.create(
    #     file=Path("x.py"),
    #     purpose='vision'
    # )
