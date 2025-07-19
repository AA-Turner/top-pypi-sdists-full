#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : audio
# @Time         : 2025/7/17 13:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from openai import AsyncOpenAI

from meutils.pipe import *
from meutils.io.files_utils import to_url
from meutils.llm.clients import AsyncOpenAI
from meutils.llm.openai_utils import to_openai_params
from meutils.llm.check_utils import get_valid_token_for_fal

from meutils.config_utils.lark_utils import get_next_token_for_polling, get_next_token
from meutils.schemas.openai_types import STTRequest, TTSRequest

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Z59Js10DbhT8wdt72LachSDlnlf?sheet=iFRwmM"  # 异步任务号池

BASE_URL = "https://ai.gitee.com/v1"

from fal_client.client import AsyncClient, SyncClient, Status, FalClientError


# try:
#
#     data = await AsyncClient(key=token).run(
#         application=request.model,
#         arguments=arguments,
#     )
#     logger.debug(data)
#     return ImagesResponse(data=data.get("images"), timings={"inference": time.time() - s})
#
# except Exception as exc:  #
#     logger.error(exc)
#     from fastapi import HTTPException, status
#
#     raise HTTPException(
#         status_code=500,
#         detail=f"Failed to generate image: {exc}",
#     )

# "fal-ai/minimax/speech-02-turbo"
async def text_to_speech(request: TTSRequest, api_key: Optional[str] = None):
    api_key = api_key or await get_valid_token_for_fal()

    payload = {

        "text": request.input,
        "voice_setting": {
            "speed": 1,
            "vol": 1,
            "voice_id": request.voice or "Voice904740431752642196",  #
            "pitch": 0,
            "english_normalization": False
        },
        "output_format": "hex"

        # **request.model_dump(exclude_none=True)
    }

    try:

        data = await AsyncClient(key=api_key).run(
            application=request.model,
            arguments=payload,
        )
        logger.debug(data)

    except Exception as exc:  #
        logger.error(exc)
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=500,
            detail=f"Failed: {exc}",
        )


if __name__ == '__main__':
    data = {
        "model": "fal-ai/minimax/speech-02-turbo",
        "input": "根据 prompt audio url克隆音色",
        # "response_format": "url"

        "voice": "Wise_Woman"
    }

    request = TTSRequest(**data)
    print(request)

    arun(text_to_speech(request))
    # print(MODELS.values())
