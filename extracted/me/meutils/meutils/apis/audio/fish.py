#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2024/7/5 12:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: # 雷军 "738d0cc1a3e9430a9de2b544a466a7fc" 增加模型映射表
# https://docs.fish.audio/api-reference/endpoint/openapi-v1/speech-to-text
# https://docs.fish.audio/text-to-speech/create-model
import shortuuid
# https://api.fish.audio/文档

from fish_audio_sdk import Session, TTSRequest, ASRRequest

from meutils.pipe import *
from meutils.io.files_utils import to_url_fal as to_url

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.notice.feishu import send_message as _send_message

BASE_URL = "https://api.fish.audio"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/ZUyLsVyjMhtexRt3IB9ci9fUnWc?sheet=7ce4e3"
FEISHU_URL_VIP = "https://xchatllm.feishu.cn/sheets/ZUyLsVyjMhtexRt3IB9ci9fUnWc?sheet=QLTif4"
FEISHU_URL_API = "https://xchatllm.feishu.cn/sheets/ZUyLsVyjMhtexRt3IB9ci9fUnWc?sheet=v5C5xa"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/f0475882-ad39-49d9-ad77-523c0e768e96"
)

COVER_IMAGE = get_resolve_path('../../data/cowboy-hat-face.webp', __file__).read_bytes()


async def check_token(token: str, for_api: bool = False):
    path = "api-credit" if for_api else "package"
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
            response = await client.get(f"/wallet/self/{path}")
            response.raise_for_status()
            data = response.json()

            # logger.debug(data)

            credit = data.get('credit') or data.get('balance', 0)
            logger.info(credit)

            return float(credit) > 0
    except Exception as e:
        logger.error(e)
        return False


async def get_model_list(token, **kwargs):  # 上传的音色
    params = {
        'self': True,
        'title': None,

        'page_size': 10,
        'page_number': 1,
        **kwargs
    }
    headers = {
        "authorization": f"Bearer {token}"
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        response = await client.get("/model", params=params)
        return response.is_success and response.json()


async def create_tts_model(title, voices: List[bytes], texts: Optional[List[str]] = None):
    session = Session(await get_next_token_for_polling(feishu_url=FEISHU_URL_API))  # 逆向token也兼容

    model = session.create_model(
        title=title,
        visibility="public",

        texts=texts,
        voices=voices,

        cover_image=COVER_IMAGE,
    )
    return model


async def create_tts(
        request: TTSRequest,
        token: Optional[str] = None,
        response_format: Optional[Literal["url",]] = None
):
    if len(request.text.encode()) < 500:
        token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL)
    else:
        token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL_VIP)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    payload = {
        "type": "tts",
        "channel": "free",
        "stream": True,
        "model": request.reference_id or "",  # 雷军 "738d0cc1a3e9430a9de2b544a466a7fc", # todo: 支持下 btyes
        "parameters": {
            "text": request.text
        },
        "format": request.format,
    }
    try:
        async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=300) as client:
            response = await client.post("/task", json=payload)
            response.raise_for_status()

            if response_format == "url":
                # logger.debug(response.headers)

                task_id = response.headers.get("task-id")
                task_response = await client.get(f"/task/{task_id}")
                data = task_response.json()
                data["result"] = await to_url(data["result"], filename=f'{shortuuid.random()}.mp3')  # 转存 翻墙的
                return data
            return response.content  # bytes

    except Exception as e:
        logger.error(e)
        session = Session(await get_next_token_for_polling(feishu_url=FEISHU_URL_API))
        files = session.tts(TTSRequest(**request.model_dump()))

        if response_format == "url":
            url = await to_url(b"".join(files), filename=f'{shortuuid.random()}.mp3')

            return {
                "_id": shortuuid.random(),
                "state": "finished",
                "type": "tts",
                "model": request.reference_id,
                "parameters": {
                    "text": request.text
                },
                "created_at": datetime.datetime.now().isoformat(),
                "deleted": False,
                "channel": "premium",
                "finished_at": datetime.datetime.now().isoformat(),
                "result": url,
                "generate_error": False
            }


# async def create_tts_model(token, voices: list, **kwargs):
#     """
#     {'_id': '9d10cdbea3954aa9b8fd992fd24b92a7',
#      'author': {'_id': 'd71d7c63c52e4d70be72e3afdb7952ab',
#                 'avatar': '',
#                 'nickname': '313303303'},
#      'cover_image': 'coverimage/9d10cdbea3954aa9b8fd992fd24b92a7',
#      'created_at': '2024-07-05T05:30:32.020433Z',
#      'description': '',
#      'languages': ['zh'],
#      'like_count': 0,
#      'liked': False,
#      'mark_count': 0,
#      'marked': False,
#      'samples_text': [],
#      'shared_count': 0,
#      'state': 'trained',
#      'tags': [],
#      'task_count': 0,
#      'title': 'chatfire',
#      'train_mode': 'fast',
#      'type': 'tts',
#      'updated_at': '2024-07-05T05:30:32.020407Z',
#      'visibility': 'public'}
#     """
#     payload = {
#         **kwargs
#     }
#
#     files = [
#         ("cover_image", get_resolve_path('cowboy-hat-face.webp', __file__).read_bytes())
#     ]
#
#     for voice in voices:
#         files.append(("voices", voice))  # bytes
#
#     data = [
#         ("visibility", "private"),
#         ("type", "tts"),
#         ("title", "Demo"),
#         ("train_mode", "fast"),
#         # Enhance audio quality will remove background noise
#         ("enhance_audio_quality", "true"),
#         # Texts are optional, but if you provide them, they must match the number of audio samples
#         ("texts", "text1"),
#         ("texts", "text2"),
#     ],
#
#     files = {
#         'title': (None, 'chatfire-tts'),
#         'description': (None, ''),
#         'type': (None, 'tts'),
#         'train_mode': (None, 'fast'),
#         'visibility': (None, 'public'),  # private
#
#         'voices': file,  # ('audio_name.mp3', file)
#         'cover_image': open(get_resolve_path('cowboy-hat-face.webp', __file__), 'rb')
#
#     }
#
#     headers = {
#         "authorization": f"Bearer {token}"
#     }
#     async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
#         response = await client.post("/model", json=payload, files=files)
#         # logger.debug(response.text)
#         if response.is_success:
#             _ = response.json()
#             _['model_id'] = _['_id']
#             return _
#         else:
#             return response.text


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZDcxZDdjNjNjNTJlNGQ3MGJlNzJlM2FmZGI3OTUyYWIiLCJleHAiOjE3MzAyODYwNjguNTMyMTA5NX0.GNeW2WLlBqyP6evNQFkXpqa0UYOg50_IwNO48DuJc04"
    # print(bjson(arun(get_model_list(token))))
    # file = open('/Users/betterme/Downloads/whisper-1719913495729-54f08dde5.wav.mp3.mp3', 'rb')

    # arun(create_tts_model(title="chatfire-tts", voices=[Path("x.mp3").read_bytes()]))

    # model="cf8ea9c2c9e947a6b9d0fccec68c9dbd"

    # token = "5cf445234491429c9855d3fa666d49f6"

    # arun(check_token(token, for_api=True))

    request = TTSRequest(text="语音克隆" * 20, reference_id="cf8ea9c2c9e947a6b9d0fccec68c9dbd")
    arun(create_tts(request, response_format="url"))
    # text = arun(create_tts(request))
    #
    # Path('x.mp3').write_bytes(text)

    # print(get_resolve_path('../../data/cowboy-hat-face.webp', __file__))
