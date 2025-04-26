#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2024/10/16 19:27
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://docs.together.ai/reference/post_images-generations


from openai import AsyncOpenAI

from meutils.pipe import *
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.llm.openai_utils import to_openai_images_params
from meutils.notice.feishu import IMAGES, send_message as _send_message
from meutils.apis.translator import deeplx

from meutils.schemas.translator_types import DeeplxRequest
from meutils.schemas.image_types import ImageRequest, TogetherImageRequest

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=tEsIyw"
FEISHU_URL_FREE = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=tEsIyw"

DEFAULT_MODEL = "black-forest-labs/FLUX.1-schnell-Free"
MODELS = {
    "flux-fast": DEFAULT_MODEL,
    "flux-turbo": DEFAULT_MODEL,
    "flux-schnell": DEFAULT_MODEL,

    "flux1.1-pro": "black-forest-labs/FLUX.1.1-pro",
}

send_message = partial(
    _send_message,
    title=__name__,
    url=IMAGES
)


async def generate(request: TogetherImageRequest, api_key: Optional[str] = None):
    request.model = MODELS.get(request.model, DEFAULT_MODEL)

    request.prompt = (
        await deeplx.translate(DeeplxRequest(text=request.prompt, target_lang="EN"))
    ).get("data", request.prompt)

    logger.debug(request)
    data = to_openai_images_params(request)

    for i in range(5):
        if any(i in request.model.lower() for i in {"pro"}):
            api_key = api_key or await get_next_token_for_polling(FEISHU_URL)
        else:
            api_key = api_key or await get_next_token_for_polling(FEISHU_URL_FREE, from_redis=True)

        try:
            client = AsyncOpenAI(base_url=os.getenv("TOGETHER_BASE_URL"), api_key=api_key)
            response = await client.images.generate(**data)
            response.model = ""
            return response
        except Exception as e:
            logger.error(e)
            if i > 2:
                send_message(f"生成失败: {e}\n\n{api_key}\n\n{request.model_dump_json(indent=4, exclude_none=True)}")


if __name__ == '__main__':
    from meutils.pipe import *

    api_keys = """
e3c18de174dc0cf7bdabc6f68432085a613fdabd2b3c2ffb4f3ed216f9aab44e
    """.split()

    for api_key in api_keys:
        request = TogetherImageRequest(model="pro", prompt="a dog", size="512x1024", n=4)
        print(request)
        arun(generate(request, api_key=api_key))
        break
