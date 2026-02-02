#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ppio_hailuo
# @Time         : 2025/7/30 09:02
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.apis.utils import make_request_httpx
from meutils.schemas.openai_types import TTSRequest
from meutils.config_utils.lark_utils import get_next_token_for_polling

from meutils.apis.ppio.videos import base_url, feishu_url


@retrying()
async def text_to_speech(request: TTSRequest, api_key: Optional[str] = None):
    """
    调用ppio接口创建语音
    :param request:
    :return:
    """
    if isinstance(api_key, str) and api_key.startswith("oneapi:"):
        api_key = api_key.removeprefix("oneapi:")

    api_key = api_key or await get_next_token_for_polling(feishu_url, from_redis=True, ttl=3600)  # todo: 优化

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = request.model_dump(exclude_none=True)
    payload = {
        "text": request.input,
        "stream": False,
        "output_format": request.response_format if request.response_format in {"url", "hex"} else "hex",
        "voice_setting":
            {
                "speed": request.speed or 1,
                "voice_id": request.voice or "wumei_yujie",
                "emotion": "happy"
            },
        **payload
    }

    # logger.debug(bjson(payload))

    response = await make_request_httpx(
        base_url=base_url,
        path=request.model,
        payload=payload,

        headers=headers,

        debug=True
    )

    if request.response_format not in {"url", "hex"}:
        _ = bytes.fromhex(response["audio"])

        # logger.debug(type(_))

        return _

    return response


if __name__ == '__main__':
    data = {
        "model": "minimax-speech-02-turbo",
        "input": "你好",
        "voice": "柔美女友",
        "response_format": "url"
    }
    arun(
        text_to_speech(
            TTSRequest(
                model="minimax-speech-02-turbo",
                input="你好",

                # response_format='hex',

                # **data
            )
        ))

"""
curl \
-X POST https://api.ppinfra.com/v3/minimax-speech-02-turbo \
-H "Authorization: Bearer sk_3W5amR6wiLNSzAyz9wkHBxSf848ZQckbTzZQrxNY1Og" \
-H "Content-Type: application/json" \
-d '{
  "text": "近年来，人工智能在国内迎来高速发展期，技术创新与产业应用齐头并进。从基础的大模型研发到语音识别、图像处理、自然语言理解等关键技术突破，AI 正在深度赋能医疗、金融、制造、交通等多个领域。同时，政策支持和资本推动加速了技术落地，众多科技企业、创业团队和科研机构持续投入，形成了活跃的创新生态。AI 正逐步从实验室走向实际生产力，成为推动数字中国建设和经济高质量发展的重要引擎，未来发展潜力巨大。",
  "stream": false,
  "output_format": "url",
  "voice_setting": {
    "speed": 1.1,
    "voice_id": "male-qn-jingying",
    "emotion": "happy"
  }
}'

"""

