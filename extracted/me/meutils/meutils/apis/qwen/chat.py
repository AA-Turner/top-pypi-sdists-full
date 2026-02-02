#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat
# @Time         : 2025/8/19 13:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : qwen-image
from openai import AsyncOpenAI, OpenAI, AsyncStream

from meutils.pipe import *
from meutils.decorators.retry import retrying, IgnoredRetryException
from meutils.oss.ali_oss import qwenai_upload
from meutils.apis.qwen.utils import getali231
from meutils.apis.utils import create_http_client

from meutils.io.files_utils import to_bytes, guess_mime_type, to_url
from meutils.caches import rcache, cache
from meutils.apis.images.edits import ImageProcess, edit_image

from meutils.llm.openai_utils import to_openai_params, create_chat_completion_chunk, token_encoder, oneturn2multiturn
from meutils.llm.clients import volc_client

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, CompletionUsage, \
    ChatCompletion, Choice, ChatCompletionMessage, ChatCompletionChunk
from meutils.schemas.image_types import ImageRequest, ImagesResponse

from fake_useragent import UserAgent

ua = UserAgent()

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=PP1PGr"

base_url = "https://chat.qwen.ai/api/v2"
DEFAUL_MODEL = "qwen3-max-2026-01-23"

thinking_budget_mapping = {
    "low": 1000,
    "medium": 8000,
    "high": 24000
}

COOKIE = """
cnaui=310cbdaf-3754-461c-a3ff-9ec8005329c9; aui=310cbdaf-3754-461c-a3ff-9ec8005329c9; sca=aefac4ee; _bl_uid=48m6Ff3ekbLh43ujec8jl4m0e8y9; _qimei_uuid42=19a110a00211002b73b1c14fac8e92b3f3b989bc9a; _qimei_i_3=5ab95e83c40c54889292f9630ed571e4a1b8f7a5470d0685b28f795b73952838653733973989e2de91a3; _qimei_h38=47aeffd773b1c14fac8e92b303000001c19a11; cna=BEmGIPo32RwCATrw/+KoZcgr; x-ap=cn-hongkong; _gcl_au=1.1.475285651.1764204393; _c_WBKFRo=neaX9BPqDXm4fRXc0NO5D633PnxaPkQ7IhZj1uhP; _nb_ioWEgULi=; _qimei_fingerprint=efbb885a22f7d4e5589008c28bc8e7ba; acw_tc=0a03e59817652532017887407e144f21cca63f1e36e7a85d922482180c00e4; xlly_s=1; _qimei_i_1=62da7086920b058d97c3f93758d672b3f6eaf2a04153568bb6dd2b582593206c616336c63980b3ddd7aae0f5; token={TOKEN}; atpsida=1724abe1cdf368a18121c81f_1765254084_7; tfstk=gwVSCSOo_kF295ytFX72ctuqYncQAZ5ZPegLSydyJbh-AeZUWv3yaa2QhkrS2kahr2nLvkiUUt5arzcn9GzC_1zuoHGk5uOJwxQK82JRuYCde8_j9GSNgVxFD3cLz3IbixUxm2gpyDEKkq3tD43-JknxHV3w2XhLvZGxr2AKJXddMs3iDDhKpkUAl2oxyXhLvrQj-Xsy526Sqz_wOO92CUY7WmOp9SgAxc4WOBg4N46-fzofXGFXsYiTymOdjen-Jm3_MMxrxSaYwVrAgQGQk2Zsw-svNka8Ik0T2st-P8U_7xNhXBg0HuDqP-_pH0Ut2uM7CnQSx7r7OYVObIm8hSVIa-SW_DDL37DgaidS6R4raJEAJBnQH2Iy9Cos4w9BlAAIlc7flpv33guMXollEoD-o4MVlZt8KY3mlqbflpvneq0SPZ_X2Jf..; isg=BBAQxPW0TaRlah8qq_nLznlQ4Vhi2fQjUChC5QrhMGs-RbTvserAsxszHQ2llaz7; ssxmod_itna=1-iqGhD50IThkG8Dhx_xmuxWKUt_EoG7DzxC5KY0CDmxjKidDRDB40QRTNf_T=oN0NA1Arq739rA2tDlhTeDZDGIdDqx0orUKCG0Ue=YlDymI08WORU30YnerkdjHbdxjpDH4s=ly=yM/h5RdX1exGI_DG2DYoDCqDS0DD9ibeD4R3Dt4DIDAYDDxDWjeDBYabQDGpN2mTi=ew5wiRNxi3Q8WPQDitzxi5F=PcN=C4_wDDlFPGf8ePb2YrDbqDumKqa/eDLBPPExB6KxYppRlMXxBjh1QrOe6nT2iCrGOGMKimUQbexvGIotD5YD10yDGxNI0eQT40H4N0DBhOebhSb8S4DGbeerwlTeiQx_0CEk1=f1_BDfOi6Op_GKPoxhOxv2w075ZB5NADq2pNGsaA4QjYVYsnL44D; ssxmod_itna2=1-iqGhD50IThkG8Dhx_xmuxWKUt_EoG7DzxC5KY0CDmxjKidDRDB40QRTNf_T=oN0NA1Arq739rAhYDioRvY8ezD7P7FISqDsNKWOfi7TvQox=7qRb7fLoshp10Sxn/bdd6BjT/P=QSUzi=8jMGcGohfz74BFwvSRf=94qNYpMrcChUotD=9FqruR3uNgTWRI8DfbAxTaPWMCx2xzcW2_wbNak_URfiPeuxT5AhcQdUq_b235TQqepU4/_Drv66h1LhEOqrDkdn7_CGoHnp4OL=7CI=_wht8Ys0NXZ670CUbcLricIf7V_l0B_kxLY=U8PqyC0oZKcAKUC09jdnALfCInlp4ZtThA1gpigpeDbYDE0rP8lG3gX2Q6B0jihUVpRTPfVQGg2A7ijiPiNR0IpixoYMnRQt6oeKT/K5xAeznc7RPci2iweCv_60jmUcnGk6YXmEzzr9evnaxrgvEenu8tTb0DUNrcXx42EeY2Kr4ea2YIaOa1=5YaxfYAyDqn/U5rqXmrpto2WhPOm_o6jmDQpnjbQ4vPXYn3ELn6qz0P7DPc0GBnP_=KYYtYZHXDgE0GqQxM0jttPOHMHdIzAkn2qwK2sdMRnk_eIwbpK0DbtpmdKGAMbTGWxquzWLvInPY4WazCGnjE3Y_5Y44GzrYU1nws0PenD8Dxcv/xDPndD
""".strip()
COOKIE = """
cnaui=310cbdaf-3754-461c-a3ff-9ec8005329c9; aui=310cbdaf-3754-461c-a3ff-9ec8005329c9; sca=aefac4ee; _bl_uid=48m6Ff3ekbLh43ujec8jl4m0e8y9; _qimei_uuid42=19a110a00211002b73b1c14fac8e92b3f3b989bc9a; _qimei_i_3=5ab95e83c40c54889292f9630ed571e4a1b8f7a5470d0685b28f795b73952838653733973989e2de91a3; _qimei_h38=47aeffd773b1c14fac8e92b303000001c19a11; cna=BEmGIPo32RwCATrw/+KoZcgr; x-ap=cn-hongkong; _gcl_au=1.1.475285651.1764204393; _c_WBKFRo=neaX9BPqDXm4fRXc0NO5D633PnxaPkQ7IhZj1uhP; _nb_ioWEgULi=; _qimei_fingerprint=efbb885a22f7d4e5589008c28bc8e7ba; xlly_s=1; acw_tc=0a03e59517654336148102039e0f3d06a8e95437aad91af9db9b8c3319d4e6; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjMxMGNiZGFmLTM3NTQtNDYxYy1hM2ZmLTllYzgwMDUzMjljOSIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzUwNjYwODczLCJleHAiOjE3NjYwMzkzNDJ9.prufhjxnPTIYRgVBw7kigw_gAFvZCEvNOpLalrFmaoA; _qimei_i_1=4cc42d86920b058d97c3f93758d672b3f6eaf2a04153568bb6dd2b582593206c616336c63980b3ddd7a7dffa; atpsida=811e76b4648ff8be7c0b20c2_1765434545_5; tfstk=guLZRht0KZvBJ8eI5pQq8ZrwWObO7ZkSSE6fiIAc1OXiBE_Vi9R4ChOXiZuVKKBMciXg0wvR_EsGor23u91kfjnvsW0HF1jMljnYKwvVsoYsBxI36eJzlPMtXI4VlZDSF4gW6cQAoY9Y-2YbB1CajqscjMbOGPAL403W6CFHvIx264gqxLhPntvcjM0ha940Ilvm-yXdMs2GiPcet9B3SP4GsBXhasrGoZvcKX5AK1bcjKAnTsBhnfUesI4FNGcpZ_0Jay_cbTAGLzRpR1X_XCWUXlTeYGWoP9z0oe5wOcJNrP0PKhtD5wYiK-_HwH9GTau4g6-ytNfwH4UOSQAHmG8qc7BvYBx5YHFs668waE5Px2yhag8H5NKEUz6kvIYVxCHz26tDNFt2CvUcC3RHLgTQdz_H7d8GYajPn-CnCX8vb-qVj6CFFXlEQLsbTJTxzNrYDMbRTTG11oEAjT1FFXlUDoIhn6WS111..; isg=BLu7RO5kVvjd4WTLjIDAf1ZZSpklEM8Sj7GZBK14pLrQDNruNuMgYg0KJqxCLCcK; ssxmod_itna=1-iqGhD50IThkG8Dhx_xmuxWKUt_EoG7DzxC5KY0CDmxjKidDRDB40QRTNf_T=oNqnKlGF__0erMBeDlhTeDZDGIdDqx0orUKCG0Ue=YlD5uo08WORU30YnerkdjH4dx6gNF4s=ly=yM/xl8LLeexGI_DG2DYoDCqDS0DD99EdD4R3Dt4DIDAYDDxDWjeDBYabQDGpN2mTi=ew5wiRNxi3Q8WPQDitzxi5F=PcN=C4_wDDlFPGf8ePb2YrDbqDumKqa/eDLBPPExB6KxYppRlMXxBjh1QrOe6nT2iCrGOGgKimUGgDr0k48I0xBDxY4/KDQB2e3TN0v4N0DBhOAxVbTHfAYDDWnLi5gx_D_PRCEk1=f1_G_aYNfCiYExnoQdBQYO5ZB5xg5aGYPSxaA4o7DUlx5rsaiDD; ssxmod_itna2=1-iqGhD50IThkG8Dhx_xmuxWKUt_EoG7DzxC5KY0CDmxjKidDRDB40QRTNf_T=oNqnKlGF__0erMYDAe1GFPrVfD7P7NASj4D/_c7fL4TTR1RmX0QNKlyxTgZGMq4sNYz4HKsvmiQQUnl8=cIDKZSTL5I322lfjq1O_geRt6FYinQLh4GqREIqIxUup33nf5v7DfFGbYoDdXKm3nCLhKYdbyA3YU0jfKTGGxnSG4wO2MbA=HGcXOdCXqfQiCAeK4beR4y=RvNmAEBqA1iZf1IMG3be6vosd5rH14vf4AYGi7/id4Rs48YiLZ7d4GEAY447imjwzlwGYP_mDez0ojqq3D
""".strip()

umid_token = "T2gAhz4xYX0DdfGNwEIDsGX7PH7M6HMzmVLuxU9GwmDC7eQoKVzlMA_a9uUjPIRw2II="
bx_ua = "231!4J3304mUX8p+jmkvUA3apMEjUq/YvqY2leOxacSC80vTPuB9lMZY9mRWFzrwLEV0PmcfY4rL2yQQzv4epFzCDXCN39IsbtzKjZV3BwK/R5DDDxuDiKaulHZWSpMXZKNwEGeLDZWdu3zSO4SgWJLtk5br+R4ag259rqHbr17eiw4tpiDr47wde+me8qgDK+CT+RuXSpWH8c8OIxzZEAOFjEoE76Ok+I8GUPyFoypr+MnepADqk+I9xGdFCQLMlFlCok+++4mWYi++6b84o76B8U0Dj+ozEKqDG2rm4t9MrvgtgXIYQwAu3lCMYfisytaPYYUDNlhIcaXjA+jrU6dPhInJI3WusfxgRpCGRtq4MijVtaBnRi5LCOtTTAwyMfiXncBRsMvw3PuKCX7t5Ozt3UWB+uzqpa8NXtWzh0/3ugbcJ3X2C5CkThlWhjK8KtOpRrrRR1TEoUdMnypR3bJx+kS63seebwMFRPCeCAc2wQya8pW9A98HrEr6kKixeuOY0sMNkEZeSuQmva1kK93fN4drsr6HqOsWuI4n+0RaIdnp37buCmUxmdl6zxRrKAaGnwWbTgC42QxRBl/xZW0194W+tlH6zI5q8tNN2nuDeXG64QVsfKPjUqnil3NeyxhswfMYfJspynQHRy4Ro2IKzS1qp5Sn664L3BYBPJghtk1tO960+rUUK5gi1clTAmNEq4z5mH2k1+i89rudmX/iM+ajTb5vxadAGACVm42SYNK+oHjGUsaGoTXZFFaC7gARcfbvLmAzLUlLM7T864FRsMUcoxU7udf3Dq79HYjSboQW+vphPA9z+pD5wO3wwr9zi3oMB9SLJqw2nl3cwu7HMcqCe+Jk2LTOyradhEmUMzm92e3I3a2C+Y8tV7/xtIKb8bgWFVdZ1uGQEiSP7LoL2JGZJ5d73vV5iUWPnbTS8VaG8Z0GlgMBDQe5LjiztrfoQWnsipk9PZu3mRMWGOsRnc1iEzpz9Yrepegq5vnmXUtSf9/JBRAH6JWU5UCDDj/DmeemNa2L10+vVrajz7iuygnadAaqJjrLkoPo6jS47rvSaLcTmhH/nq22zkSQ9SOBV5+E5ofP03T0eI8ueeT8SCqqnF56D8f1GehQbsLnc3Mt2d0R2PnZfDMXJqmixmaUenf98tXr0wJkw/n5UeufdsWjlhkvUr25+kvv9DFvaUUy8MxqqJfWYNZecwI9iaQrm4XBSZ4WGEKY+D6rO49n/DlHzS/Hl3TQP8c9Dj7tZlbGU1zUGJmjxz7K3B0LJQV4xIEbUMNIN/5Jn6L+gJFrJInpQcVsD/lJkDKp5GPzWYq9iKcP7vbTMPt3MvDWL9fMTXkNUYHAfbyq3Z3T/99SR/ps5fuVfIw2vEgV9LiHqj4VrYlr8m8ZRyuWo566t+Cet/BBFdy2ujaair8E8tB2E8lWtT7CdWpAsUfZDe93tWIiPGRb4zR0G4dkA422B9ehwMYM2/hfl/pRpOCMdZ8dgAhZCjH2g5XMrFphIeKhwJMe6dBrqS97c+iQmVlkqXrqkZWjvdJTLToa6/WYbFYfJj+Jzh92wiR99GUtyuLT6TonLHynzj8Smz+Z90YHZaZsU56UJN2tw4+uDkiZ9WDXWBjiBcXf6uTIjIGFaaDF2ms675t+qBM8h3SGyIx9"

headers = {
    # 'bx-ua': bx_ua,
    # 'bx-umidtoken': umid_token,
    # 'bx-v': '2.5.31',
    # 'source': 'web',
    # 'timezone': datetime.datetime.now().strftime('%a %b %d %Y %H:%M:%S GMT%z'),
    # 'x-request-id': str(uuid.uuid4()),
    # 'x-accel-buffering': 'no',
    # 'content-type': 'application/json; charset=UTF-8',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}


class Completions(object):
    def __init__(self, api_key: Optional[str] = None, default_model: Optional[str] = None,
                 http_url: Optional[Any] = None):
        self.api_key = api_key
        self.default_model = default_model or DEFAUL_MODEL

        self.http_url = http_url

    @retrying(ignored_exception_types=IgnoredRetryException)
    async def generate(self, request: ImageRequest, **kwargs):

        if request.image and not request.image[-1].startswith("http"):
            request.image = await to_url(request.image, content_type="image/png")

        if isinstance(request.image, str):
            request.image = [request.image]

        _ = CompletionRequest(
            model="qwen-image",
            stream=True,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{request.prompt} --resolution 4K"},

                        *[
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": url
                                }
                            }
                            for url in request.image or []
                        ]
                    ],

                }
            ],
            size=request.aspect_ratio or "1:1"
        )
        try:
            async for chunk in await self.create(_):
                logger.debug(chunk)
                if chunk.choices and (url := chunk.choices[0].delta.content):
                    if request.response_format == "oss_url":
                        request = ImageProcess(model="clarity", image=url)
                        url = await edit_image(request)

                    return ImagesResponse(data=[{"url": url}])

        except Exception as e:
            logger.error(e)  # your request has been blocked
            if "Token has expired" in str(e) or "insufficient" in str(e):
                return
            elif 'your request has been blocked' in str(e):
                raise Exception("request retry")

            raise Exception(
                f"qwen-image error: Please check the prompt or image \n\n{e}")  # An error occurred during streaming

    async def create(self, request: CompletionRequest, cookie: Optional[str] = None, **kwargs):
        if request.tools:  # 兜底
            request.model = "doubao-seed-1-8-251215"
            data = to_openai_params(request)

            return await volc_client.chat.completions.create(**data)

        api_key = self.api_key or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True)

        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
            default_headers={
                'x-request-id': str(uuid.uuid4()),
                'timezone': datetime.datetime.now().strftime('%a %b %d %Y %H:%M:%S GMT%z'),

                'bx-ua': await self.get_bx_ua(),

                "Referer": "https://chat.qwen.ai/",  #######
                # "Referer": "https://chat.qwen.ai/c/ff93a681-e570-4aad-80d4-c68a5c34bd33", #######

                'User-Agent': ua.random,
                'Cookie': cookie or COOKIE.format(TOKEN=api_key),
                **headers,
                **kwargs
            },
            http_client=await create_http_client(self.http_url)

        )

        chat_id = await self.create_new_chat()

        if request.model.endswith("-thinking") or request.enable_thinking:
            request.model = request.model.removesuffix("-thinking")
            thinking_enabled = True
            thinking_budget = request.thinking_budget or 1024
        else:
            thinking_enabled = False
            thinking_budget = request.thinking_budget

        model = request.model

        payload = {
            "chat_id": chat_id,
            "stream": request.stream,
            "incremental_output": True,
            "chat_mode": "normal",
            "model": model,
            "messages": [  # todo 多轮对话： 多轮转单轮
                {
                    "role": "user",
                    # "content": request.last_user_content,

                    "content": oneturn2multiturn(request.messages),

                    "user_action": "chat",
                    "files": [],
                    # "models": [
                    #     DEFAUL_MODEL
                    # ],
                    "chat_type": "t2t",
                    # "chat_type": "t2i",
                    # "chat_type": "image_edit",

                    "sub_chat_type": "t2t",

                    "feature_config": {
                        "thinking_enabled": thinking_enabled,
                        "output_schema": "phase",
                        "thinking_budget": thinking_budget,
                        "research_mode": "normal"
                    },
                    # "extra": {
                    #     "meta": {
                    #         "subChatType": "t2t"
                    #     }
                    # }
                }
            ],
            "size": request.size if hasattr(request, "size") else "1:1"
        }

        if request.model.startswith("qwen-image"):
            payload['model'] = self.default_model
            payload["messages"][0]["chat_type"] = "t2i"
            payload["messages"][0]["sub_chat_type"] = "t2i"
            payload["messages"][0]["content"] = request.last_user_content

            # logger.debug(request.last_urls)
            if image_urls := request.last_urls.get("image_url"):
                # if not image_urls[0].startswith("http"):
                #     logger.debug("图片转url")
                #     image_urls = await to_url(image_urls, content_type="image/png")

                payload["messages"][0]["chat_type"] = "image_edit"
                payload["messages"][0]["files"] = [
                    {
                        "type": "image",
                        "name": "example.png",
                        "file_type": "image",
                        "showType": "image",
                        "file_class": "vision",
                        "url": url  # todo 阿里对象存储
                    }
                    for url in image_urls
                ]
        elif request.model.endswith("-search"):
            payload['model'] = request.model.removesuffix("-search")
            payload["chat_id"] = chat_id
            payload["messages"][0]["chat_type"] = "search"
            # payload["messages"][0]["feature_config"]["search_version"] = "v2"
            payload["messages"][0]["sub_chat_type"] = "search"

            payload["messages"][0]["extra"] = {
                "meta": {
                    "subChatType": "search"
                }}

            # logger.debug(bjson(payload))


        elif request.last_urls:  # 通用

            files = []
            for k in ["image_url", "audio_url", "video_url", "file_url"]:
                files += [
                    {
                        # "name": "name",
                        "type": k.removesuffix("_url"),
                        "url": url
                    }
                    for url in request.last_urls.get(k, [])
                ]

            payload["messages"][0]["files"] = files

        data = to_openai_params(payload)
        data["stream"] = True  # 强制开启 stream
        logger.debug(bjson(data))
        response = await self.client.chat.completions.create(**data, extra_query={"chat_id": chat_id})
        # response = self.do_response(response)
        logger.debug(response)

        if isinstance(response, AsyncStream):  # todo
            if request.model.startswith("qwen-image"):  # 中转后 测试首行是否报错
                return response

            return self.stream(request, response)

            # web_search 模式下, 会返回 phase="web_search" 的 delta
            # async def gen():
            #     chunk: ChatCompletionChunk
            #     async for chunk in response:  # ChatCompletionChunk
            #         logger.debug(chunk)
            #         if chunk.choices and (delta := chunk.choices[0].delta):
            #             if hasattr(delta, "phase") and (phase := delta.phase):  # phase =="web_search"
            #                 if hasattr(delta, "extra") and (info := delta.extra.get("web_search_info")):  # todo 其他 info
            #                     logger.debug(bjson(info))
            #
            # return await gen()

        # else:

        # # 缺少 reasoning_content 与 usage
        # logger.debug(response)
        #
        # if hasattr(response, "data") and (choices := response.data.get("choices")):
        #     response = response.model_construct(id=chat_id, choices=choices)
        #     logger.debug(response)
        # # “”“    completion_tokens = len(token_encoder.encode(str(response.choices[0].message.content)))
        # # AttributeError: 'str' object has no attribute 'choices'”""
        # prompt_tokens = len(token_encoder.encode(str(request.messages)))
        # completion_tokens = len(token_encoder.encode(str(response.choices[0].message.content)))
        #
        # # logger.debug(len(token_encoder.encode(str(response.choices[0].message.content))))
        #
        # usage = {
        #     "prompt_tokens": prompt_tokens,
        #     "completion_tokens": completion_tokens,
        #     "total_tokens": prompt_tokens + completion_tokens
        # }
        # response.usage = usage
        # return response

    async def stream(self, request, chunks):
        idx = 0
        nostream_content = ""
        nostream_reasoning_content = ""
        chunk = None
        usage = None
        chunk_id = f"chatcmpl-{shortuuid.random()}"

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
            chunk.id = chunk_id

            if hasattr(chunk.choices[0].delta, "status") and chunk.choices[0].delta.status == "finished":
                chunk.choices[0].finish_reason = "stop"

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

    async def create_new_chat(self):  # todo 预建
        payload = {
            # "title": "新建对话",
            # "models": [self.default_model],
            # "chat_mode": "normal",
            # "chat_type": "t2i",
            # "timestamp": time.time() * 1000 // 1
        }
        response = await self.client.post('/chats/new', body=payload, cast_to=object)

        logger.debug(response)

        if chat_id := response['data'].get('id'):
            return chat_id
        else:
            logger.error(response)
            raise IgnoredRetryException("insufficient")

    @cache(ttl=120)
    async def get_bx_ua(self):
        return getali231()

    @property
    def models(self):
        headers = {
            'User-Agent': ua.random,
            # 'Cookie': cookie or COOKIE
        }
        response = httpx.get("https://chat.qwen.ai/api/models", headers=headers)
        # logger.debug(response.text)

        data = response.json()["data"]
        #
        return [m["id"] for m in data]


if __name__ == '__main__':
    headers = {
        "bx-ua": "231!nkv35kmUiUB+joGkK5zhZ48FEl2ZWfPwIPF92lBLek2KxVW/XJ2EwruCiDOX5Px4EXqM9RGySMPcO1CD+z/kCY6oY8GLFOeZtpxnBGP9LA9kRyBuF/QHVK0qN6FQhN/PKY/oRXyNDCIlSxVeXj2EjVPcrJGHB+kITVfVRijdTuCxVaGidQzu3ko00Q/oyE+jauHhUHfb1GxGHkE+++3+qCS4+ItVNA6PPj7so+r+ZGPfiw7kMbD1EpZipnjcQW+n1UQMLjt0GypRcCK3glYYtR+7EfvYqwxEAskf/uZyjmCES+1FSvILqLDGKbUpIgB+acfu6lcZvBbkvwSESMdGn0QDL/Fay+55Hf26siZ68mMxdySU60DW6w1R5nU9pav32s4W6ehXRw/7v5pxQ6kGjuIwR/t+FAU8+HjmY8pn5qidQfNHUzcuB/riYFxlkJrqYHzwU/v1d+M8fHizgrftUcfDbDP/rGNZwltgFR0Qv4mKP62Pkt4b8HEnWc14dWomQWQDUBMWwngt18TesPRNBC+BvjLgiUCoikqAIWQlWhqv6hX3faioWrUsRnxLFgKY3OQbfP5IE+BbE8OC1RNVnLrljDJp4ZfcgDJ7SMAzFdLMpSZ+MriGXpXwyGXNiA+xxMZNAZrXv40UhJ5sZ0CNG5vHEMAOnbh4AwBfp2pEo4trgBqoWWFcm/uk1rRsRy0lotDw0DPsMa2u7OkXz+GAnVYHAmo8vXKjN+RHJo9gDeEQT2YNAAZkkCFyFbTBU3O6ZS9TooO4MhKTiTFUvyfkrHU7QUCN6b7TRknxNpkf9Bvmx3RTziOwAwZFoQ2bt8/UQ6mUPP2BjqDCDQnPE9AWTwXr1Ob7YrU8b8l0KLFG/HqmpbAvJVemnqBdyuOJwHQ25MjE3W4/80D07BSsofX/wkd+kLG++iPO7cGuNcQp/6uT92vj3KanZ5pcyYNCJmUwD1cEZVAsuBfIx8SDL2BeyZlgthccaHx9Q5GD3mqyPiWexs4qt5y+vOPaQNZlGfJ936CmOB/O8VhIii0ONcFg33CsaoZcRF8THOiOhdAxlo9ZcEhA+stWLZZG0RxeFeuQ0+LW7ImvF59wkOlPhGBZ5b9t2zZf//Gn6QIm/Bcra1ZZGI+VFpu0qX/2k2dQ9r9VHafgbhElgmWpqVuhasngwhUXqYMXRfNJVkUChxRoQuLEkiEcAqKcDXbK3QojWpRxPDoWvaVDY2cniYdoO9OKpseCP2qDbfKDCAPXX5lFMEOSl0Nyj2k3YzdaVG0g/2BFciExE40pjgEBUIBB5EY9NZwJmHv+HKpgHJ2LS0fX5cIlJCl1e6Jl0d0KQnVgiFcTtK/xz1WjMpTDd+h7ztjBxur5EJ1w7NtLWQvQcIDWYjMfrEL3LBp+9qXpD3RbDax+eAy2kyDiT3hxlJAPbK0+JdeAMGEf8iz2szOcUS1fxzC8zKqKVsmNe0/EVBxf+uE0gCqQIBUvl13WmA5aHlHKRS/ujaoee/NddOOb8exUXt4yCuPcDBnDF9LbVQ89+rDhq1F3rvbXOJ9ONprghKr+KRYjfgG8l+==",

        "bx-umidtoken": "T2gARtMfY1eEmcrMcFe-FYv9NM_oZlpLsSK0LNE-n5PYEvGM1oYBV9duC5Ngq7Ldjnc="
    }
    # print(Completions().models)
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjMxMGNiZGFmLTM3NTQtNDYxYy1hM2ZmLTllYzgwMDUzMjljOSIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzUwNjYwODczLCJleHAiOjE3NjYwMzg0MzF9.k3tuvE6yqAgeZyPFsYqWuQVhEIy-zk3PXRYFdxnEgZY"
    # api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjMxMGNiZGFmLTM3NTQtNDYxYy1hM2ZmLTllYzgwMDUzMjljOSIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzUwNjYwODczLCJleHAiOjE3NjYwNDAxNzh9.vkQ2a0hyJqLUN_CISRTy51G7KJEc4JcFU8WRmJWV2YA"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjUxN2I0YzM2LTFlODEtNDdlNy05MzlkLWM0MmQ2NWUwMTc4YSIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzUwNjYwODczLCJleHAiOjE3NjcwODQ0NTB9.4Kjq9HU6vWQBXswWycBukaO5xLofcJRl9syoF3mFUfQ"
    # content = [
    #     {"type": "text", "text": "南京今天天气"},
    # ]
    #
    # content = [
    #     {"type": "text", "text": "a dog"},
    # ]
    #
    # content = [
    #     {"type": "text", "text": "a dog"},
    # ]

    url = "https://datawin-space.oss-cn-beijing.aliyuncs.com/test2/xyzsxf_02-001.mp4"

    # url =  "https://qwen-webui-prod.oss-accelerate.aliyuncs.com/310cbdaf-3754-461c-a3ff-9ec8005329c9/f9ddea84-af55-4390-9ad6-0693e8881ed6_xyzsxf_02-001.mp4?x-oss-security-token=CAIS0AJ1q6Ft5B2yfSjIr5rBDeDGg7YVj7Gbe0TC1Wo3Zftci42ZsDz2IHhMf3RvBeAbs%2Fs1lWBZ7vwflrN6SJtIXleCZtF94plR7QKoZ73Zocur7LAJksVMl%2Fd0w0WpsvXJasDVEfn%2FGJ70GX2m%2BwZ3xbzlD0bAO3WuLZyOj7N%2Bc90TRXPWRDFaBdBQVGAAwY1gQhm3D%2Fu2NQPwiWf9FVdhvhEG6Vly8qOi2MaRmHG85R%2FYsrZN%2BNmgecP%2FNpE3bMwiCYyPsbYoJvab4kl58ANX8ap6tqtA9Arcs8uVa1sruE3eaLeLro0ycVAjN%2FhrQ%2FQZtpn1lvl1ofeWkJznAJW0o2rsz001LaPXI6uscIvBXr5R%2FrZvZK%2FMOwn3AZMctRoyYFM1NglTmhzo1g8fwuTEg9gL62J%2BIYkDi95Okml8Ccvdq%2FkKJC0DloHijwMz0urxuU4agAGLXaoi5VZfNjf0YaFT7bZxl01ur%2Bljqz%2FgQFOi8UoGfU0gGvOf5F1T6XaN5HfoLeVA%2BIq9euwJ0E5rPxtCCWBxpzC4UgTApoPfcLZuzgMzcJYvtKzMfHczSVDCwEUhFqkJbISs8hsAO7R4DRauDVAeSgK8MD%2FlWCKl%2FfNXKbrNTyAA&x-oss-date=20251020T065510Z&x-oss-expires=300&x-oss-signature-version=OSS4-HMAC-SHA256&x-oss-credential=STS.NYtFZrni48spybs1jbitpdH2R%2F20251020%2Fap-southeast-1%2Foss%2Faliyun_v4_request&x-oss-signature=b3bf8af1327e626f2402a2ca6d9f937bb35773f71d1efa104b762e8179458f24"

    content = [
        {"type": "text", "text": """
        # 身份
你是一个高精度的【视频内容转录员】。

# 核心任务
你的唯一任务是：以【时间戳】为单位，逐字逐句、逐个动作地记录视频中的所有视听信息。你必须像法庭书记员一样，做到100%的客观和精确。

# 输出格式 (必须严格遵守)
使用以下格式，为每个独立事件创建新的一行：
[HH:MM:SS] [类别]: [内容]

# “类别”包括：
- **[台词]**: 记录人物说的每一句话。如果能识别说话人，格式为 `[台词-人名]`. 如果不能，格式为 `[台词-男/女]`.
- **[画面]**: 描述场景、环境、人物外貌、表情和关键物品。
- **[动作]**: 描述人物的所有具体动作。
- **[音效]**: 记录所有非对话的声音，如(敲门声), (汽车鸣笛)。

# 绝对禁止
- 禁止进行任何总结、分析或评论。
- 禁止使用任何剧本格式。
- 禁止省略任何细节。
- 你的所有输出都必须是简体中文。
        """},
        # {
        #     "type": "video_url",
        #     "video_url": {
        #         "url": url
        #     }}
    ]

    # content = [
    #     {"type": "text", "text": "a dog" * 10000 + "\n\n一共多少个词"},
    # ]

    # content = [
    #     {"type": "text", "text": "一句话总结"},
    #
    #     {
    #         "type": "video_url",
    #         "video_url": {
    #             "url": "https://lmdbk.com/5.mp4",
    #         }
    #     },
    #
    # ]
    # ['qwen3-max', 'qwen3-vl-plus', 'qwen3-coder-plus', 'qwen3-omni-flash']

    from meutils.io.files_utils import to_base64

    request = CompletionRequest(
        # model="qwen3-235b-a22b",
        # model="qwen3-max",
        # model="qwen3-max-2025-10-30-thinking",
        model="qwen3-max-2025-10-30",
        # model="qwen3-max-2025-10-30-search",

        # model="qwen3-vl-plus",
        # model="qwen3-coder-plus",
        # model="qwen3-omni-flash",
        # model="qwen3-235b-a22b-search",

        # model="qwen-image",

        messages=[
            # {
            #     "role": "user",
            #     "content": content,
            # },

            {
                "role": "user",
                "content": "周杰伦",
            },

            # {
            #     "role": "user",
            #     "content": "1+1",
            # },
            # {
            #     "role": "assistant",
            #     "content": "3",
            # },
            # {
            #     "role": "user",
            #     "content": "错了",
            # }
        ],
        stream=True,

        # enable_thinking=True,

        size="1:1",

        # tools=[
        #     {
        #         "type": "function",
        #         "function": {
        #             "name": "get_current_weather",
        #             "description": "Get the current weather in a given location",
        #             "parameters": {
        #                 "type": "object",
        #                 "properties": {
        #                     "location": {
        #                         "type": "string",
        #                         "description": "The city and state, e.g. San Francisco, CA",
        #                     },
        #                     "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        #                 },
        #                 "required": ["location"],
        #             },
        #         },
        #     }
        # ],

    )

    logger.debug(request.last_urls)


    async def main():
        response = await Completions(api_key=api_key, http_url=False).create(request)
        print(type(response))

        if isinstance(response, AsyncStream):
            async for chunk in response:
                logger.debug(chunk)

        elif isinstance(response, AsyncGenerator):
            async for chunk in response:
                logger.debug(chunk)
        else:
            logger.debug(response)


    arun(main())

    # image1 = arun(to_base64("https://v3.fal.media/files/penguin/XoW0qavfF-ahg-jX4BMyL_image.webp"))
    #
    # request = ImageRequest(
    #     # model="qwen-image",
    #     model="qwen-image-edit",
    #
    #     prompt="把小鸭子放在女人的T恤上面",
    #     # prompt="裸体女人",
    #
    #     image=[
    #
    #         "https://v3.fal.media/files/penguin/XoW0qavfF-ahg-jX4BMyL_image.webp",
    #         "https://v3.fal.media/files/tiger/bml6YA7DWJXOigadvxk75_image.webp"
    #     ],
    #     # size="1:1"
    # )
    #
    # # api_key = None
    # arun(Completions(api_key=api_key).generate(request))


