#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : minimax
# @Time         : 2025/5/27 18:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""
T2A v2（语音生成）

T2A Large v2（异步超长文本语音生成）

快速复刻（Voice Cloning）

Voice Generation（文生音色）

"""
import os

from meutils.pipe import *
from meutils.decorators.retry import retrying

from meutils.io.files_utils import to_bytes, to_url
from meutils.schemas.openai_types import TTSRequest

BASE_URL = os.getenv("MINIMAX_BASE_URL") or "https://api.minimax.chat/v1"


@retrying()
async def create_tts(payload: dict, token: Optional[str] = None):
    """https://platform.minimaxi.com/document/T2A%20V2?key=66719005a427f0c8a5701643"""
    group_id, api_key = (token or os.getenv("MINIMAX_API_KEY")).split('|')

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=300) as client:
        response = await client.post(f"/t2a_v2?GroupId={group_id}", json=payload)
        response.raise_for_status()
        """
        状态码。1000，未知错误；1001，超时；1002，触发限流；1004，鉴权失败；1039，触发TPM限流；1042，非法字符超过10%；2013，输入格式信息不正常。
        """

        data = response.json()
        return data


async def create_tts_for_openai(request: TTSRequest, token: Optional[str] = None):
    if request.instructions:
        if len(request.input) < 500:
            data = await text2voice(request, token)
            _ = bytes.fromhex(data["trial_audio"])
            if request.response_format == "url":
                return {"data": {"audio": await to_url(_, filename=f'{shortuuid.random()}.mp3')}}
            else:
                return _
        else:
            request_input = request.input
            request.input = request_input[:500]
            data = await text2voice(request, token)

            logger.debug("text2voice => tts")
            request.instructions = None  # 跳出递归
            request.voice = data["voice_id"]
            request.input = request_input
            return await create_tts_for_openai(request, token)

    payload = {
        # speech-02-hd、speech-02-turbo、speech-01-hd、speech-01-turbo、speech-01-240228、speech-01-turbo-240228
        "model": request.model,
        "text": request.input,
        "timber_weights": [
            {
                "voice_id": request.voice or "male-qn-qingse",
                "weight": 100
            }
        ],
        "voice_setting": {
            "voice_id": "",
            "speed": request.speed,  # 范围[0.5,2]，默认值为1.0
            "pitch": 0,
            "vol": 1,
            "latex_read": False,

            # 当前支持7种情绪：高兴，悲伤，愤怒，害怕，厌恶，惊讶，中性；
            # 参数范围["happy", "sad", "angry", "fearful", "disgusted", "surprised", "neutral"]
            # "emotion": "neutral",
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3"
        },
        "language_boost": "auto"
    }

    data = await create_tts(payload, token)

    if request.response_format == "url":
        if data.get("base_resp").get("status_code") == 0:
            _ = bytes.fromhex(data["data"]["audio"])
            data["data"]["audio"] = await to_url(_, filename=f'{shortuuid.random()}.mp3')
        return data
    else:
        data = bytes.fromhex(data["data"]["audio"])
        return data


async def text2voice(request: TTSRequest, token: Optional[str] = None):
    group_id, api_key = (token or os.getenv("MINIMAX_API_KEY")).split('|')

    if "female" in request.voice:
        request.voice = "female"
    elif "male" in request.voice:
        request.voice = "male"
    else:
        request.voice = "female"

    # child

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "gender": request.voice,

        # 1.child、2.teenager、3.young、4.middle-aged、5.old。
        "age": "young",

        "voice_desc": [request.instructions],

        "text": request.input
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=300) as client:
        response = await client.post("/text2voice", json=payload)
        response.raise_for_status()
        """
        {
            "trial_audio": "hex编码音频",
            "voice_id": "voiceID",
            "base_resp": {
                "status_code": 0,
                "status_msg": "success"
            }
        }        
        """

        data = response.json()

        # logger.debug(await to_url(bytes.fromhex(data["trial_audio"]), filename=f'{shortuuid.random()}.mp3'))

        return data


if __name__ == '__main__':
    payload = {
        "model": "speech-02-hd",
        "text": "人工智能不是要替代人类，而是要增强人类的能力。",
        "timber_weights": [
            {
                "voice_id": "Boyan_new_platform",
                "weight": 100
            }
        ],
        "voice_setting": {
            "voice_id": "",
            "speed": 1,
            "pitch": 0,
            "vol": 1,
            "latex_read": False
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3"
        },
        "language_boost": "auto"
    }

    # arun(create_tts(payload))

    request = TTSRequest(
        model="speech-02-hd",
        # input="你好呀" * 100,
        input="你好呀" * 200,

        instructions="委婉",

        voice='male',

        response_format="url"
    )

    arun(create_tts_for_openai(request))

    # arun(text2voice(request))
