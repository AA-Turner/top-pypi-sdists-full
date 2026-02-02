#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_images
# @Time         : 2024/10/16 08:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from openai import AsyncOpenAI
from openai import APIStatusError

from meutils.pipe import *
from meutils.io.files_utils import to_base64, to_url
from meutils.llm.openai_utils import to_openai_images_params
from meutils.apis.utils import create_http_client
from meutils.notice.feishu import IMAGES, send_message as _send_message

from meutils.schemas.image_types import ImageRequest, FluxImageRequest, SDImageRequest, ImagesResponse

send_message = partial(
    _send_message,
    title=__name__,
    url=IMAGES
)

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=3aA5dH"
FEISHU_URL_FREE = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=xlvlrH"

BASE_URL = "https://api.siliconflow.cn/v1"


async def generate(request: ImageRequest, api_key: Optional[str] = None, base_url: Optional[str] = None):
    base_url = base_url or BASE_URL  # todo

    logger.debug(base_url)

    request.prompt_enhancement = True
    if request.model.lower().startswith("qwen"):
        if request.image:
            request.model = request.model.replace("qwen-image", "qwen-image-edit-2509")

            for k, v in zip(["image", "image2", "image3"], request.image_urls):
                setattr(request, k, v)

    data = to_openai_images_params(request)
    # data['extra_body'].update({
    #     "image_size": request.size
    # })
    if len(str(data)) < 1000: logger.debug(bjson(data))

    try:
        client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        response = await client.images.generate(**data)
        # logger.debug(response)

    except APIStatusError as e:
        logger.debug(e)
        # logger.debug(e.response.json())
        # logger.debug(e.response.status_code)

        if e.response.status_code > 403 and any(i in BASE_URL for i in {"siliconflow", "modelscope"}):
            client = AsyncOpenAI(
                base_url=BASE_URL,
                api_key=api_key,
                http_client=await create_http_client(1)
            )
            response = await client.images.generate(**data)
        raise e

    return response


if __name__ == '__main__':
    from meutils.pipe import *

    api_key = os.getenv("SILICONFLOW_API_KEY")
    base_url = None
    # base_url = "https://open.cherryin.ai/v1"
    # api_key = "sk-N6S3M2bur2hEWLmPmGB1ae8rjWu8rncsVf1Msw8C6FioDQFj"

    data = {
        "model": "qwen/qwen-image",
        # "model": "qwen/qwen-image(free)",



        # "model": "black-forest-labs/FLUX.1-Krea-dev",

        "prompt": "A young woman and a monkey inside a colorful house",
        # "image": [
        #     "https://v3.fal.media/files/panda/HDpZj0eLjWwCpjA5__0l1_0e6cd0b9eb7a4a968c0019a4eee15e46.png",
        #     "https://v3.fal.media/files/zebra/153izt1cBlMU-TwD0_B7Q_ea34618f5d974653a16a755aa61e488a.png",
        #     "https://v3.fal.media/files/koala/RCSZ7VEEKGFDfMoGHCwzo_f626718793e94769b1ad36d5891864a4.png"
        # ],
        # "aspect_ratio": "16:9",
        # "size": "16x9",
        "size": "16:9",

        # "movement_amplitude": "auto"
    }

    arun(generate(ImageRequest(**data), api_key, base_url))

    # https://api.siliconflow.cn/v1
