#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : deepinfra
# @Time         : 2024/11/26 13:57
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from openai import AsyncOpenAI

from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI
from meutils.llm.openai_utils import to_openai_params
from meutils.io.files_utils import to_url

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.schemas.openai_types import STTRequest, TTSRequest

from meutils.schemas.gitee_types import FEISHU_URL, BASE_URL


async def text_to_speech(request: TTSRequest, api_key: Optional[str] = None):
    api_key = api_key or await get_next_token_for_polling(FEISHU_URL)

    data = to_openai_params(request)

    extra_body = request.metadata or {}
    if request.instructions:
        extra_body['instruct_text'] = request.instructions

    if audio := extra_body.get('prompt_audio_url'):
        extra_body['prompt_wav_url'] = audio

    data['extra_body'] = extra_body

    logger.debug(bjson(data))

    client = AsyncOpenAI(base_url=BASE_URL, api_key=api_key)
    response = await client.audio.speech.create(**data)

    if request.response_format == "url":
        url = await to_url(response.content, filename=f'{shortuuid.random()}.mp3')
        return {"url": url}

    return response


if __name__ == '__main__':
    model = "GLM-TTS"
    model = 'IndexTTS-2'
    data = {
        "model": model,
        "input": "根据 prompt audio url克隆音色",
        "response_format": "url",

        "metadata": {
            "prompt_audio_url": "https://gitee.com/gitee-ai/moark-assets/raw/master/jay_prompt.wav",
            "prompt_text": "对我来讲是一种荣幸，但是也是压力蛮大的。不过我觉得是一种呃很好的一个挑战。"
        }
    }

    request = TTSRequest(**data)

    print(request)

    arun(text_to_speech(request))
    # print(MODELS.values())

# from openai import OpenAI
# client = OpenAI()
# response = client.audio.speech.create(
# 	input="我知道自己不是一个人在战斗，有大家的支持和协作，我相信我们一定能一起把事情做好。他的爱像秋天的阳光，看似清冷，却总能在我最需要的时候给予温暖",
# 	model="IndexTTS-2",
# 	extra_body={
# 		"prompt_audio_url": "https://gitee.com/gitee-ai/moark-assets/raw/master/jay_prompt.wav",
# 		"prompt_text": "对我来讲是一种荣幸，但是也是压力蛮大的。不过我觉得是一种呃很好的一个挑战。",
# 		"emo_text": "你吓死我了！你是鬼吗？",
# 		"use_emo_text": True,
# 	},
# 	voice="alloy",
# )
