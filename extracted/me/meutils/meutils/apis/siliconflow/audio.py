#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_images
# @Time         : 2024/10/16 08:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from openai import AsyncOpenAI

from meutils.pipe import *
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.llm.openai_utils import to_openai_images_params  # todo
from meutils.llm.check_utils import check_token_for_siliconflow
from meutils.notice.feishu import send_message as _send_message, AUDIO
from meutils.decorators.retry import retrying
from meutils.io.files_utils import to_bytes

from meutils.schemas.openai_types import STTRequest

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=3aA5dH"
FEISHU_URL_FREE = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=xlvlrH"

BASE_URL = os.getenv("SILICONFLOW_BASE_URL")

DEFAULT_MODEL = "FunAudioLLM/SenseVoiceSmall"
MODELS = {
    "sensevoice": "FunAudioLLM/SenseVoiceSmall",
}

send_message = partial(
    _send_message,
    title=__name__,
    url=AUDIO
)

check_token = check_token_for_siliconflow
check_valid_token = partial(check_token_for_siliconflow, threshold=-1)


@retrying(max_retries=3, title=__name__)
async def asr(request: STTRequest, api_key: Optional[str] = None):
    api_key = api_key or await get_next_token_for_polling(FEISHU_URL_FREE, check_valid_token, from_redis=True)

    request.model = MODELS.get(request.model, DEFAULT_MODEL)
    request.file = ('_.mp3', await to_bytes(request.file))

    data = request.model_dump(exclude_none=True)

    client = AsyncOpenAI(base_url=BASE_URL, api_key=api_key)
    response = await client.audio.transcriptions.create(**data)
    return response


if __name__ == '__main__':
    request = STTRequest(
        model="sensevoice",
        file=Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/asr/audio.mp3").read_bytes()
    )

    arun(asr(request))
