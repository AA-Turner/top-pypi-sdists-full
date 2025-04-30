#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : qwen
# @Time         : 2025/1/17 16:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""
 File "/usr/local/lib/python3.10/site-packages/meutils/llm/completions/qwenllm.py", line 47, in create
    yield response.choices[0].message.content
AttributeError: 'str' object has no attribute 'choices'

"""

from openai import AsyncOpenAI

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.io.files_utils import to_bytes, guess_mime_type
from meutils.caches import rcache

from meutils.llm.openai_utils import to_openai_params

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, CompletionUsage, \
    ChatCompletion

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=PP1PGr"

base_url = "https://chat.qwen.ai/api"

from fake_useragent import UserAgent

ua = UserAgent()
cookie = "_gcl_au=1.1.1784604298.1740443944;xlly_s=1;isg=BNHREY3fUiqB6r5JMj56XbBv4NtrPkWwIxqsYLNmGhi8WvWs-YwlgDHw_S68i93o;ssxmod_itna2=iqGxRDuQqWqxgDUxeKYI5q=xBDeMDWK07DzxC5750CDmxjKidKDUiN0bFP=WEj=A0DDkYi+rebDG+eNbK+Wx03aKKp5D/ijo3qEN9C1DyEq+CpSWKry0Bfx4khh0iWP5=wYflEkDv5FNc=0OeAHPkhiPHZGzQtya2oP44PFWnxe7P4q+KCPQr7AwYBoAD4f4zfKGb9gz0Y9w8IywD871wFkhYQfIbODkHaAWqnOhnpAv5ucGctdXFF5pP3QaxNpa=BFWtb0OEaH2F3n6FVLGF57jiHDSFO0GaYlBMzFak07lYlGvuEyKSbENgXT=Y=ZUSmoZQtKn3SnjKfvO2Q2lfSnKOAvwo6LhDu7QRojcn64xfxDI3IUDSpSQbAc29c5LaLvGd5+A89Y0oTvgE3Yo/iDuYv67D5EbS7Dcid2QDr1Ko=L9BuEQNPEWRDK2lISAA3QUfiN9ef22Ie8jhifggQbQo4WxKmw42GxQt+e=y3aEQySbRtPXppvYALY7IEtyDHA5By4oeuZPdPxZZnAnB6lB7/yKdIYjp4naEAgA0gEDxbiG4nPBZIGoePVW4YeI7SOywCjwz7RIbQhGGOHmxYk4YD;acw_tc=364cd7fa3937f891464e5d5489be2d4483c02d92564368d25c7f3c79babb6b66;cna=KP9DIEqqyjUCATrw/+LjJV8F;SERVERCORSID=d9e2ccd165e2341396ecf2215ef69904|1741348489|1741348426;SERVERID=d9e2ccd165e2341396ecf2215ef69904|1741348489|1741348426;ssxmod_itna=iqGxRDuQqWqxgDUxeKYI5q=xBDeMDWK07DzxC5750CDmxjKidKDUiN0bFP=WEj=A0DDkYi+rmCDBL4qbDnqD80DQeDvYxk0I+aeKhDw3HF8YRw3gi00iR=r9jW=kIebftOZzO8V9YoD==hYDmeDUxD1GDDkgWeDxaPD5xDTDWeDGDD3t4DCCfYYD0RpiboIVxRhTABpDYPYPR4YDY56DAqEz4SpVaxXTDDzw4iaPf4vwDi8D7FRG0RpD7P6fmQDXaYDEmWmFk=Dv6Lh+QwI1/oYOT44c2toPO0KKPHPklixYYnDgWXe2q2/WD4WwOU5HzHtiYDG+e4rzRksD2DmAkGTCP+CmizaAtrDNsjYY0DZ7qLozAE5g75ZidqBzqxxKgxNisr0DLg14D;tfstk=gban2TDT-A9jiiwvpRuCD78JvBITJBgSO8L-e4HPbAk_J8IIel0zg-m-4MZLIYDZTUJraHRZZjHGOUS5VPcZwXrKYUkEqbDtZ3lEUb7ZEbGmUzKUrlTuG7adO4CIRWgSztBAkuVQO4GKaHgfMhoZG5JeUGnF-ASaMtBAkNKveXJFHJEXGQsiNAlEa0-FsflSG4lrU05iQbcX4pyrz1fiZbJezekE_VloN4kzU45g_AGo_bjxd2u87Oy34VqrOM4ttDD4TvVLTPJtYHNZIU8zSqME3wHMzUzit5I3Kq8FoArL4y3a8OJ-7SZTLf0crQcgm5uEt8_XR2P4_uo3rgdjFlVaDcq696Gg-S4oic7MQjm07y3QjtYx3lNzrcPCnnGT4SULqJB6zvE0_RmYWdLx7y238c0V4dKw0sqvPf5873tSYfGiH7xhDSTQvqXds1x4rDlsTRCGs3OqYfGiH1fM0OoE1XyO.;token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjMxMGNiZGFmLTM3NTQtNDYxYy1hM2ZmLTllYzgwMDUzMjljOSIsImV4cCI6MTc0Mzk0MDQzNX0.CoeqvnyiM2uzcT-ZzpMcBbjqyhqkr6A7AMxWTAzcS2Y;x-ap=ap-southeast-1"

thinking_budget_mapping = {
    "low": 1000,
    "medium": 8000,
    "high": 24000
}


@retrying()
async def to_file(file, api_key):
    qwen_client = AsyncOpenAI(
        base_url="https://all.chatfire.cn/qwen/v1",
        api_key=api_key,
        default_headers={
            'User-Agent': ua.random,
            'Cookie': cookie
        }
    )
    filename = Path(file).name if isinstance(file, str) else 'untitled'
    mime_type = guess_mime_type(file)
    file_bytes: bytes = await to_bytes(file)
    file = (filename, file_bytes, mime_type)
    file_object = await qwen_client.files.create(file=file, purpose="file-extract")
    logger.debug(file_object)
    return file_object


async def create(request: CompletionRequest, token: Optional[str] = None):  # ChatCompletionRequest 重构

    if request.temperature > 1:
        request.temperature = 1

    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True)

    logger.debug(token)

    client = AsyncOpenAI(
        base_url=base_url,
        api_key=token,
        default_headers={
            'User-Agent': ua.random,
            'Cookie': cookie
        }
    )
    # qwen结构
    model = request.model.lower()
    if any(i in model for i in ("search",)):
        request.model = "qwen-max-latest"
        request.messages[-1]['chat_type'] = "search"

    # 混合推理
    if (request.reasoning_effort
            or request.last_user_content.startswith("/think")
            or hasattr(request, "enable_thinking")
            or hasattr(request, "thinking_budget")
    ):
        feature_config = {"thinking_enabled": True, "output_schema": "phase"}
        feature_config["thinking_budget"] = thinking_budget_mapping.get(request.reasoning_effort, 1024)

        request.messages[-1]['feature_config'] = feature_config

    if any(i in model for i in ("qwq", "qvq", "think", "thinking")):
        request.model = "qwen-max-latest"
        request.messages[-1]['feature_config'] = {"thinking_enabled": True}

    if "omni" in model:
        request.max_tokens = 2048

    # 多模态: todo
    # if any(i in request.model.lower() for i in ("-vl", "qvq")):
    #     # await to_file
    last_message = request.messages[-1]
    logger.debug(last_message)

    if last_message.get("role") == "user":
        user_content = last_message.get("content")
        if isinstance(user_content, list):
            for i, content in enumerate(user_content):
                if content.get("type") == 'file_url':  # image_url file_url video_url
                    url = content.get(content.get("type")).get("url")
                    file_object = await to_file(url, token)

                    user_content[i] = {"type": "file", "file": file_object.id}

                elif content.get("type") == 'image_url':
                    url = content.get(content.get("type")).get("url")
                    file_object = await to_file(url, token)

                    user_content[i] = {"type": "image", "image": file_object.id}

        elif user_content.startswith("http"):
            file_url, user_content = user_content.split(maxsplit=1)

            user_content = [{"type": "text", "text": user_content}]

            file_object = await to_file(file_url, token)

            content_type = file_object.meta.get("content_type", "")
            if content_type.startswith("image"):
                user_content.append({"type": "image", "image": file_object.id})
            else:
                user_content.append({"type": "file", "file": file_object.id})

        request.messages[-1]['content'] = user_content

    # logger.debug(request)

    request.incremental_output = True  # 增量输出
    data = to_openai_params(request)

    # 流式转非流
    data['stream'] = True
    chunks = await client.chat.completions.create(**data)

    idx = 0
    nostream_content = ""
    nostream_reasoning_content = ""
    chunk = None
    usage = None
    async for chunk in chunks:
        if not chunk.choices: continue

        content = chunk.choices[0].delta.content or ""
        if hasattr(chunk.choices[0].delta, "phase") and chunk.choices[0].delta.phase == "think":
            chunk.choices[0].delta.content = ""
            chunk.choices[0].delta.reasoning_content = content
            nostream_reasoning_content += content
        nostream_content += chunk.choices[0].delta.content
        usage = chunk.usage or usage

        if request.stream:
            yield chunk

        idx += 1
        if idx == request.max_tokens:
            break

    if not request.stream:
        logger.debug(chunk)
        if hasattr(usage, "output_tokens_details"):
            usage.completion_tokens_details = usage.output_tokens_details
        if hasattr(usage, "input_tokens"):
            usage.prompt_tokens = usage.input_tokens
        if hasattr(usage, "output_tokens"):
            usage.completion_tokens = usage.output_tokens

        chat_completion.usage = usage
        chat_completion.choices[0].message.content = nostream_content
        chat_completion.choices[0].message.reasoning_content = nostream_reasoning_content

        yield chat_completion

        # if request.stream:
    #     # stream_options = {"include_usage": True}
    #     chunks = await client.chat.completions.create(**data)
    #
    #     idx = 0
    #     async for chunk in chunks:
    #         if not chunk.choices: continue
    #
    #         content = chunk.choices[0].delta.content or ""
    #         if hasattr(chunk.choices[0].delta, "phase") and chunk.choices[0].delta.phase == "think":
    #             chunk.choices[0].delta.content = ""
    #             chunk.choices[0].delta.reasoning_content = content
    #
    #         yield chunk
    #
    #         idx += 1
    #         if idx == request.max_tokens:
    #             break
    #
    # else:
    #     response = await client.chat.completions.create(**data)
    #     if not isinstance(response, str):
    #         logger.debug(response)
    #         yield response.choices[0].message.content  # isinstance(response, str)


if __name__ == '__main__':
    # [
    #     "qwen-plus-latest",
    #     "qvq-72b-preview",
    #     "qwq-32b-preview",
    #     "qwen2.5-coder-32b-instruct",
    #     "qwen-vl-max-latest",
    #     "qwen-turbo-latest",
    #     "qwen2.5-72b-instruct",
    #     "qwen2.5-32b-instruct"
    # ]

    user_content = [
        {
            "type": "text",
            "text": "一句话总结"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://fyb-pc-static.cdn.bcebos.com/static/asset/homepage@2x_daaf4f0f6cf971ed6d9329b30afdf438.png"
            }
        }
    ]

    user_content = "1+1"
    user_content = "/think 1+1"

    # user_content = [
    #     {
    #         "type": "text",
    #         "text": "总结下"
    #     },
    #     {
    #         "type": "file_url",
    #         "file_url": {
    #             "url": "https://oss.ffire.cc/files/AIGC.pdf"
    #         }
    #     }
    #
    # ]

    request = CompletionRequest(
        # model="qwen-turbo-2024-11-01",
        # model="qwen-max-latest",
        # model="qvq-max-2025-03-25",
        # model="qvq-72b-preview-0310",
        # model="qwen2.5-omni-7b",

        # model="qwen-max-latest-search",
        # model="qwq-max",
        # model="qwq-32b-preview",
        # model="qwq-max-search",

        # model="qwen2.5-vl-72b-instruct",

        # model="qwen-plus-latest",
        model="qwen3-235b-a22b",
        # model="qwen3-30b-a3b",
        # model="qwen3-32b",

        # max_tokens=1,
        max_tokens=None,

        messages=[
            {
                'role': 'user',
                # 'content': '今天南京天气',
                # 'content': "9.8 9.11哪个大",
                # 'content': 'https://oss.ffire.cc/files/AIGC.pdf 总结下',

                # "chat_type": "search",

                'content': user_content,

                # "content": [
                #     {
                #         "type": "text",
                #         "text": "总结下",
                #         "chat_type": "t2t",
                #         "feature_config": {
                #             "thinking_enabled": False
                #         }
                #     },
                #     {
                #         "type": "file",
                #         "file": "2d677df1-45b2-4f30-829f-0d42b2b07136"
                #     }
                # ]

                # "content": [
                #     {
                #         "type": "text",
                #         "text": "总结下",
                #         "chat_type": "t2t",
                #         "feature_config": {
                #             "thinking_enabled": False
                #         }
                #     },
                #     {
                #         "type": "file_url",
                #         "file_url": {
                #           "url": 'xxxxxxx'
                #         }
                #     }
                # ]
                # "content": [
                #     {
                #         "type": "text",
                #         "text": "总结下",
                #         # "chat_type": "t2t"
                #
                #     },
                # {
                #     "type": "image",
                #     "image": "703dabac-b0d9-4357-8a85-75b9456df1dd"
                # },
                # {
                #     "type": "image",
                #     "image": "https://oss.ffire.cc/files/kling_watermark.png"
                #
                # }
                # ]

            },

        ],
        # stream=True,

        # reasoning_effort="low",
        enable_thinking=True,
        thinking_budget=1024,
        # stream_options={"include_usage": True},

    )
    token = None

    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNzY1N2Y1LTgxN2ItNDg5Yi1iNjk4LWFhZjAyM2EwZTE4MyIsImV4cCI6MTc0NjI5NTAwNH0.D1uJN44NHiEt6URce4upbHvs7v73_Vd0V1s3T_JzclI"
    arun(create(request, token))
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNzY1N2Y1LTgxN2ItNDg5Yi1iNjk4LWFhZjAyM2EwZTE4MyIsImV4cCI6MTc0NjI5NTAwNH0.D1uJN44NHiEt6URce4upbHvs7v73_Vd0V1s3T_JzclI"

    # arun(to_file("https://oss.ffire.cc/files/kling_watermark.png", token))
