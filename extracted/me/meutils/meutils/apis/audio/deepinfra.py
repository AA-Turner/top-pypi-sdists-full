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
from meutils.decorators.retry import retrying
from meutils.io.files_utils import to_bytes
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.notice.feishu import send_message as _send_message, AUDIO
from meutils.schemas.openai_types import STTRequest

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=6lr4oi"

BASE_URL = os.getenv("DEEPINFRA_BASE_URL")

DEFAULT_MODEL = "openai/whisper-large-v3-turbo"
MODELS = {
    "whisper-large-v3": "openai/whisper-large-v3",
    "whisper-large-v3-turbo": "openai/whisper-large-v3-turbo",
    "whisper-1": "distil-whisper/distil-large-v3"
}

send_message = partial(
    _send_message,
    title=__name__,
    url=AUDIO
)


@retrying(max_retries=3, title=__name__)
async def asr(request: STTRequest, api_key: Optional[str] = None):
    api_key = api_key or await get_next_token_for_polling(FEISHU_URL)

    request.model = MODELS.get(request.model, DEFAULT_MODEL)
    request.file = ('_.mp3', await to_bytes(request.file))

    data = request.model_dump(exclude_none=True)

    client = AsyncOpenAI(base_url=BASE_URL, api_key=api_key)
    response = await client.audio.transcriptions.create(**data)
    return response


if __name__ == '__main__':
    request = STTRequest(
        model="whisper-1",
        file=Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/asr/audio.mp3").read_bytes()
    )

    arun(asr(request))
    # print(MODELS.values())
