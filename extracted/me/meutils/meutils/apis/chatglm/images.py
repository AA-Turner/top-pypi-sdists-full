#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2024/10/17 11:59
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from openai import AsyncOpenAI

from meutils.pipe import *
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.llm.openai_utils import to_openai_images_params
from meutils.schemas.image_types import ImageRequest, CogviewImageRequest
from meutils.notice.feishu import IMAGES, send_message as _send_message
from meutils.io.image import image2nowatermark_image

FEISHU_URL = "..."  # api
FEISHU_URL_FREE = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=siLmTk"

BASE_URL = "http://any2chat.chatfire.cn/glm/v1"

DEFAULT_MODEL = "cogview-3"
MODELS = {

}

send_message = partial(
    _send_message,
    title=__name__,
    url=IMAGES
)


async def generate(request: CogviewImageRequest, redirect_model: Optional[str] = None, api_key: Optional[str] = None):
    request.model = MODELS.get(request.model, DEFAULT_MODEL)

    api_key = api_key or await get_next_token_for_polling(FEISHU_URL_FREE)

    data = to_openai_images_params(request)
    for i in range(3):
        try:
            client = AsyncOpenAI(base_url=BASE_URL, api_key=api_key)
            response = await client.images.generate(**data)
            response.data[0].url = await image2nowatermark_image(response.data[0].url) or response.data[0].url
            return response
        except Exception as e:
            logger.error(e)
            if i > 2:
                send_message(f"生成失败: {e}\n\n{api_key}\n\n{request.model_dump_json(indent=4, exclude_none=True)}")


if __name__ == '__main__':
    from meutils.pipe import *

    arun(generate(CogviewImageRequest(model='cogview-3', prompt="a dog", size="1024x1024")))



    # response.data[0].url = await image2nowatermark_image(response.data[0].url)
