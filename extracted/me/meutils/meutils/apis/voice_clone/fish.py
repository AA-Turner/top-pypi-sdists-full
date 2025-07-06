#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2024/7/5 12:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo
# https://docs.fish.audio/api-reference/endpoint/openapi-v1/speech-to-text
# https://docs.fish.audio/text-to-speech/create-model
import httpx

from meutils.pipe import *
from meutils.schemas.task_types import Task
from meutils.schemas.openai_types import TTSRequest
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.notice.feishu import send_message as _send_message

from openai.types.file_object import FileObject
from fastapi import UploadFile

BASE_URL = "https://api.fish.audio"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/ZUyLsVyjMhtexRt3IB9ci9fUnWc?sheet=7ce4e3"

url = "https://api.fish.audio/model"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/f0475882-ad39-49d9-ad77-523c0e768e96"
)


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


async def create_task(request: TTSRequest):
    """
        await create_task(request, stream=True)
    :param request:
    :return:
    """
    token = await get_next_token_for_polling(feishu_url=FEISHU_URL)

    headers = {
        "authorization": f"Bearer {token}"
    }
    payload = {
        "type": "tts",
        "channel": "free",
        "stream": True,  # 区别？
        "model": request.voice,
        "parameters": {
            "text": request.input
        }
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post("/task", json=payload)
        if response.is_success:
            logger.debug(response.headers)

            task_id = response.headers.get("task-id")
            task_response = await client.get(f"/task/{task_id}")
            data = task_response.json()
            data['url'] = data['result']
            data['fileview'] = url2fileview(data['result'])
            return data

        response.raise_for_status()


async def create_file_for_openai(file: UploadFile):  # todo: 存储 redis
    token = await get_next_token_for_polling(feishu_url=FEISHU_URL)

    filename = file.filename or file.file.name
    model_info = await create_tts_model(token, file=(filename, file.file))

    if isinstance(model_info, dict):
        model_id = model_info.get("_id")
        file_id = model_id
        status = "processed"
    else:
        file_id = shortuuid.random()
        status = "error"

    file_object = FileObject.construct(
        id=file_id,

        filename=filename,  # result.get("file_name")
        bytes=file.size,

        created_at=int(time.time()),
        object='file',

        purpose="voice-clone",
        status=status,

        data=model_info
    )
    return file_object


async def create_tts_model(token, file, **kwargs):
    """
    {'_id': '9d10cdbea3954aa9b8fd992fd24b92a7',
     'author': {'_id': 'd71d7c63c52e4d70be72e3afdb7952ab',
                'avatar': '',
                'nickname': '313303303'},
     'cover_image': 'coverimage/9d10cdbea3954aa9b8fd992fd24b92a7',
     'created_at': '2024-07-05T05:30:32.020433Z',
     'description': '',
     'languages': ['zh'],
     'like_count': 0,
     'liked': False,
     'mark_count': 0,
     'marked': False,
     'samples_text': [],
     'shared_count': 0,
     'state': 'trained',
     'tags': [],
     'task_count': 0,
     'title': 'chatfire',
     'train_mode': 'fast',
     'type': 'tts',
     'updated_at': '2024-07-05T05:30:32.020407Z',
     'visibility': 'public'}
    """
    payload = {
        **kwargs
    }

    logger.debug(file)

    files = {
        'title': (None, 'chatfire-tts'),
        'description': (None, ''),
        'type': (None, 'tts'),
        'train_mode': (None, 'fast'),
        'visibility': (None, 'public'),  # private

        'voices': file,  # ('audio_name.mp3', file)
        'cover_image': open(get_resolve_path('cowboy-hat-face.webp', __file__), 'rb')

    }

    headers = {
        "authorization": f"Bearer {token}"
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post("/model", json=payload, files=files)
        # logger.debug(response.text)
        if response.is_success:
            _ = response.json()
            _['model_id'] = _['_id']
            return _
        else:
            return response.text


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZDcxZDdjNjNjNTJlNGQ3MGJlNzJlM2FmZGI3OTUyYWIiLCJleHAiOjE3MzAyODYwNjguNTMyMTA5NX0.GNeW2WLlBqyP6evNQFkXpqa0UYOg50_IwNO48DuJc04"
    # print(bjson(arun(get_model_list(token))))
    # file = open('/Users/betterme/Downloads/whisper-1719913495729-54f08dde5.wav.mp3.mp3', 'rb')

    # arun(get_model_list(token))
    # file = UploadFile(file)
    # pprint(arun(create_tts_model(token, file=(file.file.name, file.file))))
    # model = "9d10cdbea3954aa9b8fd992fd24b92a7"
    # # # task_id = "f5a94a3fb78646b8ab1c3606413ca9e0"
    # with timer():
    #     text = "文本转语音\n文本转语音\n文本转语音\n文本转语音\n"
    #     request = TTSRequest(input=text, model=model)
    #     arun(create_task(request))
    # open("xx.mp3", 'wb').write(f)

    # async def main():
    #     content = await create_task(request, stream=True)
    #     with open("xx.mp3", 'wb') as f:
    #         f.write(content)

    # arun(main())

    # pprint(arun(get_tts_task(token, task_id)))

    #
    # file = open('/Users/betterme/Downloads/whisper-1719913495729-54f08dde5.wav.mp3.mp3', 'rb')
    #
    # file = UploadFile(file)
    #
    # print(arun(upload_audio_for_tts_model(file=file)))

    # token = "5cf445234491429c9855d3fa666d49f6"

    # arun(check_token(token, for_api=True))

    #     text = "文本转语音\n文本转语音\n文本转语音\n文本转语音\n"


    arun(create_task(TTSRequest(input="你好", model="")))