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
import time

from openai import AsyncOpenAI

from meutils.pipe import *
from meutils.decorators.retry import retrying
# from meutils.oss.ali_oss import qwenai_upload
from meutils.io.files_utils import to_bytes, guess_mime_type
from meutils.caches import rcache

from meutils.llm.openai_utils import to_openai_params

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, CompletionUsage, \
    ChatCompletion

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=PP1PGr"

base_url = "https://chat.qwen.ai/api"

DEFAUL_MODEL = "qwen3-max"

from fake_useragent import UserAgent

ua = UserAgent()

thinking_budget_mapping = {
    "low": 1024,
    "medium": 8 * 1024,
    "high": 81920
}

COOKIE = """
_gcl_au=1.1.1093269050.1756349377;xlly_s=1;_bl_uid=LXmp28z7dwezpmyejeXL9wh6U1Rb;cnaui=310cbdaf-3754-461c-a3ff-9ec8005329c9;isg=BCQknTSrEFaWtGtm_x0nSvW89SQWvUgnEt_awT5Fz--w6cezYs52t7gDqUFxMYB_;ssxmod_itna2=1-iqGhD50IThkG8Dhx_xmuxWKUt_EoG7DzxC5KY0CDmxjKidDRDB40QRTnf_Ti=qaeGrMwxrDPxD3r5iY80q7DFg0WeDBk4uAn8mY3vKFTl7S9o7EaoSeXnAOPBSok57ccC4rhgutjg2_8D7jk_lChKSSdfMbm2lKAUlRwIqjSxeNld4tMGxFev6zkUel_6LR_foIGQa5L4PuCGa6dUqvwISCODQh2TC6wQ1Hu=Ll=W4=W6s1E_V8Dr_1gDECghksL8zvQHiPI60ChnPodSvFnHjE2iXzGDdE_I5876eQ03cEzaFsA48KQLReNjiPp1I0EfN=5a=dziPIxXxcpup5zmGM2L48PYjAqiUxrwVQDY4vN=Ni_pu6pxOYEBNL7YA6RPcRy7Ak=Y5PPbZRAi242ulCDx3oZCGH2YE6p3lD4gPIOKMWX6AbmhYLrcMeXcYdjzGgaYEDq4DUtKP/1jf=vXt=MQXoZ23BWlE5h06cjceY_Bxw3AH3KeBaxT4pHEt19QSlaO20G9DfDq7Wf3BvV=5X/BYd54Y44nUHOfH_fV2mHKNz0W4lxjWDjY9H3m00I3cOIf3C6q7Y_CNx1sG1nwsiDUA34QDtsC8jw1YD;sca=aefac4ee;acw_tc=0a03e54a17574902359765651e1e9cf9780667ec2a2cefacce63a0b954bb63;atpsida=7e2e4dcfcd1c4a4530dd3395_1757490275_2;aui=310cbdaf-3754-461c-a3ff-9ec8005329c9;cna=KP9DIEqqyjUCATrw/+LjJV8F;ssxmod_itna=1-iqGhD50IThkG8Dhx_xmuxWKUt_EoG7DzxC5KY0CDmxjKidDRDB40QRTnf_Ti=qaeGrMwxrDyxGXoNexiNDAg40iDCbmLx5Yjdrq4NFtrojKaIjL4Q43rj9_8m0tnY/qmUTMU6Rljs7s66tqGI_DG2DYoDCqDS0DD99OdD4_3Dt4DIDAYDDxDWIeDB4ZrQDGPtLQut5eqKwBrtxi3QWWPQDiUCxivW56Wt5C_GwDDliPGfWepi20iDbqDuzKqaBeDLRPpvxB=PxYPmjmkUxBQGHniO/WWb2BkrGOGBKim6mTeM0O_qBGGhfyDGxNI0eYT44YxS4VQYQjytGBFDDWgL4_AzKl_TYx_7CIq13b1_BDCgtIQi_GK=DKoBddAQ2wmlBx/DYfjGeAzNA4aDhLlxtlzaiDD;tfstk=geyx-Dg4-gKxmZY2DPflIb1e9VjuX_qVPrrBIV0D1zU85rs2IlGD5dU-rirmhZz8VyUp5diXCbw8-cTbnog6NdUtyi8XG1y-XPUwhK1V7utSbmnbWlSqfVa_WVVcZ9q40Ak1-lBhKo8RmR1gkd9XVGitjCsoG1PJiYM1-wXoYFbWuAaGVPsqNugrXctjCPOWFD0ScEOb54GSADYjCAa12YiZcKi6GfZ5Fm0S5AM_5us-j4ijCAa_VgnZs7QtPngMBSZPyLNC_OpMI8nxMVpikdIljmcxRogRRwwJ3j3Qc4p18hgjf4iLFN8m78E7hD45EKHTVcUKh7QWHPEbTPoQlTLjDSZLxbeNRdnzNrloD7I6NqZIlrhY9Usx7-4YBjyC-Lubw8ytn7bvKVl_Z-lUna9xdWrmn5a5fdgTNcsPDJ2LcuTnJcAf2gdw_jirJjsq62sn5Go--iB9_ClP403h2wOw_jir22jA-CRZag5..;token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjMxMGNiZGFmLTM3NTQtNDYxYy1hM2ZmLTllYzgwMDUzMjljOSIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzUwNjYwODczLCJleHAiOjE3NTgwOTUwMzd9.JdVvyPkln2HcGm6ib0FKaF1qQ87lG1nf70oezhYZ2Jg;x-ap=cn-hongkong
""".strip()


@retrying()
async def to_file(file, api_key, cookie: Optional[str] = None):
    qwen_client = AsyncOpenAI(
        base_url="https://all.chatfire.cn/qwen/v1",
        api_key=api_key,
        default_headers={
            'User-Agent': ua.random,
            'Cookie': cookie or COOKIE
        }
    )
    filename = Path(file).name if isinstance(file, str) else 'untitled'
    mime_type = guess_mime_type(file)
    file_bytes: bytes = await to_bytes(file)
    file = (filename, file_bytes, mime_type)
    file_object = await qwen_client.files.create(file=file, purpose="file-extract")
    logger.debug(file_object)
    return file_object


async def create(request: CompletionRequest, token: Optional[str] = None, cookie: Optional[str] = None):
    cookie = cookie or COOKIE

    if request.temperature > 1:
        request.temperature = 1

    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True)

    logger.debug(token)

    default_query = None

    client = AsyncOpenAI(
        base_url=base_url,
        api_key=token,
        default_headers={
            'User-Agent': ua.random,
            'Cookie': cookie,
        },

        default_query=default_query
    )
    # qwen结构
    model = request.model.lower()
    if any(i in model for i in ("research",)):  # 遇到错误 任意切换
        request.model = DEFAUL_MODEL
        request.messages[-1]['chat_type'] = "deep_research"

    elif any(i in model for i in {"search", }):
        request.model = DEFAUL_MODEL
        request.messages[-1]['chat_type'] = "search"
        request.messages[-1]['feature_config'] = {
            "thinking_enabled": False,
            "output_schema": "phase",
            "search_version": "v2"
        }
        request.messages[-1]['extra'] = {
            "meta": {
                "subChatType": "search"
            }
        }
        request.messages[-1]['sub_chat_type'] = "search"

    # 混合推理
    if (request.reasoning_effort
            or request.last_user_content.startswith("/think")
            or request.enable_thinking
            or request.thinking_budget
            or any(i in model for i in ("qwq", "qvq", "think", "thinking"))
    ):
        # logger.debug(request)

        if "qwen-plus-2025-09-11" in model:
            request.model = "qwen-plus-2025-09-11"
        elif "qwen3-vl-plus" in model:
            request.model = "qwen3-vl-plus"
        else:
            request.model = DEFAUL_MODEL

        feature_config = {"thinking_enabled": True, "output_schema": "phase"}
        feature_config["thinking_budget"] = thinking_budget_mapping.get(request.reasoning_effort, 1024)
        request.messages[-1]['feature_config'] = feature_config

    # 适配thinking

    if "omni" in model:
        request.max_tokens = 13684

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
                    file_object = await to_file(url, token, cookie)

                    user_content[i] = {"type": "file", "file": file_object.id}


                elif content.get("type") == 'image_url':
                    url = content.get(content.get("type")).get("url")
                    file_object = await to_file(url, token, cookie)

                    user_content[i] = {"type": "image", "image": file_object.id}

                elif content.get("type") == 'input_audio':
                    url = content.get(content.get("type")).get("data")
                    file_object = await to_file(url, token, cookie)

                    user_content[i] = {"type": "audio", "file": file_object.id}

                    logger.debug(bjson(user_content))

        elif user_content.startswith("http"):
            file_url, user_content = user_content.split(maxsplit=1)

            user_content = [{"type": "text", "text": user_content}]

            file_object = await to_file(file_url, token, cookie)

            content_type = file_object.meta.get("content_type", "")
            if content_type.startswith("image"):
                user_content.append({"type": "image", "image": file_object.id})
            else:
                user_content.append({"type": "file", "file": file_object.id})

        request.messages[-1]['content'] = user_content

    logger.debug(request)

    request.incremental_output = True  # 增量输出
    data = to_openai_params(request)

    logger.debug(data)

    # 流式转非流
    data['stream'] = True
    chunks = await client.chat.completions.create(**data)

    idx = 0
    nostream_content = ""
    nostream_reasoning_content = ""
    chunk = None
    usage = None
    async for chunk in chunks:
        # logger.debug(chunk) # search 结构不一样

        if not chunk.choices: continue

        content = chunk.choices[0].delta.content or ""
        if hasattr(chunk.choices[0].delta, "phase") and chunk.choices[0].delta.phase == "think":
            chunk.choices[0].delta.content = ""
            chunk.choices[0].delta.reasoning_content = content
            nostream_reasoning_content += content

        # logger.debug(chunk.choices[0].delta.content)
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
            "text": "总结下"
        },
        # {
        #     "type": "file_url",
        #     "file_url": {
        #         # "url": "https://fyb-pc-static.cdn.bcebos.com/static/asset/homepage@2x_daaf4f0f6cf971ed6d9329b30afdf438.png"
        #         "url": "https://lmdbk.com/5.mp4"
        #     }
        # }
    ]

    # user_content = "主体文字'诸事皆顺'，超粗笔画、流畅飘逸、有飞白效果的狂野奔放草书字体，鎏金质感且有熔金流动感和泼溅金箔效果，黑色带细微噪点肌理背景，英文'GOOD LUCK'浅金色或灰白色，有淡淡的道家符文点缀,书法字体海报场景，传统书法与现代设计融合风格,特写,神秘奢华充满能量,焦点清晰，对比强烈"
    # {
    #     "type": "image_url",
    #     "image_url": {
    #         "url": "https://fyb-pc-static.cdn.bcebos.com/static/asset/homepage@2x_daaf4f0f6cf971ed6d9329b30afdf438.png"
    #     }
    # }

    # user_content = "1+1"
    # user_content = "/think 1+1"

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

    # user_content = [
    #     {
    #         "type": "input_audio",
    #         "input_audio": {
    #             "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
    #             "format": "wav",
    #         },
    #     },
    #     {"type": "text", "text": "总结一下内容"},
    # ]

    request = CompletionRequest(
        model="qwen3-max",

        # model="qwen3-235b-a22b-thinking-2507",
        # model="qwen3-max-preview",
        # model="qwen3-max-preview-search",
        # model="qwen3-omni-flash",
        # model="qwen3-vl-plus",  # todo 视频增强
        # model="qwen3-coder-plus",
        # model="qwen3-vl-plus-thinking",

        # model="qwen-plus-2025-09-11", # qwen3-next-80b-a3b
        # model="qwen-plus-2025-09-11-thinking",  # qwen3-next-80b-a3b

        # model="qwen-turbo-2024-11-01",
        # model="qwen-max-latest",
        # model="qvq-max-2025-03-25",
        # model="qvq-72b-preview-0310",
        # model="qwen2.5-omni-7b",
        # model="qwen-image",
        # model="qwen-plus",

        # model="qwen-max-latest-search",
        # model="qwq-max",
        # model="qwq-32b-preview",
        # model="qwq-max-search",

        # model="qwen2.5-vl-72b-instruct",

        # model="qwen-plus-latest",
        # model="qwen3-235b-a22b",
        # model="qwen3-30b-a3b",
        # model="qwen3-32b",

        # model="qwen-omni-turbo-0119",

        # max_tokens=1,
        # max_tokens=100,

        messages=[
            # {
            #     'role': 'user',
            #     'content': '1+1',
            # },
            # {
            #     'role': 'assistant',
            #     'content': '3',
            # },
            {
                'role': 'user',
                # 'content': '周杰伦近况',
                # 'content': "9.8 9.11哪个大",
                # 'content': 'https://oss.ffire.cc/files/AIGC.pdf 总结下',
                # 'content': 'https://lmdbk.com/5.mp4 总结下',

                # 'content': '南京今天天气如何',

                'content': user_content,
                # 'content': "错了",

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
        # stream=False,
        # stream=True,

        # reasoning_effort="low",
        # enable_thinking=True,
        # thinking_budget=1024,
        # stream_options={"include_usage": True},

    )
    token = None

    token = """
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjMxMGNiZGFmLTM3NTQtNDYxYy1hM2ZmLTllYzgwMDUzMjljOSIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzUwNjYwODczLCJleHAiOjE3NjUxODM4NDh9.iPGfvYsq6wA2XqoGBpfY5n7isM5taNGvSiQ7SawS4q8
    """.strip()

    arun(create(request, token))

    # arun(to_file("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav", token))

    # arun(create_new_chat(token))
