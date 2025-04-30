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
from meutils.io.files_utils import to_base64, to_url
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.llm.openai_utils import to_openai_images_params
from meutils.llm.check_utils import check_token_for_siliconflow
from meutils.notice.feishu import IMAGES, send_message as _send_message
from meutils.decorators.retry import retrying

from meutils.apis.translator import deeplx
from meutils.apis.proxy.kdlapi import get_one_proxy

from meutils.schemas.translator_types import DeeplxRequest
from meutils.schemas.image_types import ImageRequest, FluxImageRequest, SDImageRequest, ImagesResponse

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=3aA5dH"
FEISHU_URL_FREE = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=xlvlrH"

BASE_URL = "https://api.siliconflow.cn/v1"

DEFAULT_MODEL = "black-forest-labs/FLUX.1-schnell"
MODELS = {

    "flux.1-schnell": "black-forest-labs/FLUX.1-schnell",
    "flux.1-dev": "black-forest-labs/FLUX.1-dev",
    "flux.1-pro": "black-forest-labs/FLUX.1-dev",
    "flux.1.1-pro": "black-forest-labs/FLUX.1-dev",
    "flux-1.1-pro": "black-forest-labs/FLUX.1-dev",  # replicate
    "flux1.1-pro": "black-forest-labs/FLUX.1-dev",

    "flux.1-pro-max": "black-forest-labs/FLUX.1-dev",

    "flux-schnell": "black-forest-labs/FLUX.1-schnell",
    "flux-dev": "black-forest-labs/FLUX.1-dev",
    "flux-pro": "black-forest-labs/FLUX.1-dev",
    "flux-pro-max": "black-forest-labs/FLUX.1-dev",

    "stable-diffusion-xl-base-1.0": "stabilityai/stable-diffusion-xl-base-1.0",  # 图生图
    "stable-diffusion-2-1": "stabilityai/stable-diffusion-2-1",  # 图生图

    "stable-diffusion": "stabilityai/stable-diffusion-3-medium",
    "stable-diffusion-3-medium": "stabilityai/stable-diffusion-3-medium",
    "stable-diffusion-3": "stabilityai/stable-diffusion-3-medium",

    "stable-diffusion-3-5-large": "stabilityai/stable-diffusion-3-5-large",

    "stabilityai": "stabilityai/stable-diffusion-3-5-large",

}

send_message = partial(
    _send_message,
    title=__name__,
    url=IMAGES
)
check_token = check_token_for_siliconflow

check_valid_token = partial(check_token_for_siliconflow, threshold=-1)


@retrying(max_retries=3, title=__name__)
async def generate(request: ImageRequest, api_key: Optional[str] = None):
    request.prompt_enhancement = True
    if not request.prompt:
        # {'model': 'flux-schnell', 'messages': [{'role': 'user', 'content': '写一个10个字的冷笑话'}]}
        return ImagesResponse(**request.model_dump())

    if not request.model.startswith(("flux", "black-forest-labs")):  # 自动翻译
        request.prompt = (
            await deeplx.translate(DeeplxRequest(text=request.prompt, target_lang="EN"))
        ).get("data", request.prompt)

    request.model = MODELS.get(request.model, DEFAULT_MODEL)
    # logger.debug(request)

    if any(i in request.model.lower() for i in {"pro-max", "pro"}):
        request.num_inference_steps = 20
        api_key = api_key or await get_next_token_for_polling(
            FEISHU_URL,
            check_token=check_token,
            from_redis=True,
            min_points=0.1
        )

    elif any(i in request.model.lower() for i in {"dev", "pro"}):  # 压缩像素
        request.num_inference_steps = 20
        api_key = api_key or await get_next_token_for_polling(
            FEISHU_URL,
            check_token=check_token,
            from_redis=True,
            min_points=0.1
        )
        # request.size = "2048x1024"

        w, h = map(int, request.size.split("x"))
        max_size = max(w, h)
        w, h = w * 1024 / max_size, h * 1024 / max_size
        request.size = f"{int(w)}x{int(h)}"
    else:
        api_key = api_key or await get_next_token_for_polling(FEISHU_URL_FREE, check_valid_token, from_redis=True)

    data = to_openai_images_params(request)
    # logger.debug(data)

    # 代理
    http_client = None
    if request.user == 'proxy':
        http_client = httpx.AsyncClient(proxy=await get_one_proxy(), timeout=60)

    client = AsyncOpenAI(base_url=BASE_URL, api_key=api_key, http_client=http_client, timeout=60)
    response = await client.images.generate(**data)
    response.model = ""
    # logger.debug(response)

    # response.data[0].url = response.data[0].url.replace(r'\u0026', '&')
    send_message(f"request: {request.model}\n{request.prompt}\nresponse: {response.data[0].url}",)

    response.data[0].url = await to_url(response.data[0].url, content_type="image/png")
    if request.response_format == "b64_json":
        b64_json = await to_base64(response.data[0].url)

        response.data[0].url = None
        response.data[0].b64_json = b64_json
    if response.data[0].url:
        return response
    else:
        raise ValueError("no image")


if __name__ == '__main__':
    from meutils.pipe import *

    data = {
        # "model": "flux-schnell",
        "model": "stable-diffusion-3-5-large",

        "prompt": "(Chinese dragon soaring through the clouds).(majestic, colorful, mythical, powerful, ancient).(DSLR camera).(wide-angle lens).(dawn)(fantasy photography).(Kodak Ektar 100)",
        "negative_prompt": "",
        "n": 1,
        # "response_format": "url",
        # "response_format": "b64_json",

        # "size": "16x9",
        "num_inference_steps": 20,
        "seed": None
    }

    # data = {'model': 'flux1.1-pro',
    #         'prompt': 'Surrealism, Chinese art, fairy, close-up of the upper body, hazy, glowing, dreamy, light pink and light blue gradient long hair, beautiful and charming, dressed in cashmere-like clothing, streamlined design, elegant, fair-skinned and beautiful, delicate features, comfortable, lying on an ice blue bed, background of a crescent moon and starry sky, with a touch of romantic gifts, virtual engine rendering, 3D model, OC rendering, perfect composition, ultra-detailed details, 3D rendering close-up shot. (flux1.1-pro)',
    #         'negative_prompt': '', 'n': 1, 'response_format': 'url', 'size': '1152x2048', 'num_inference_steps': 20,
    #         'seed': None}
    #
    # data = {
    #     "model": "flux-dev",
    #     "prompt": "(Chinese dragon soaring through the clouds).(majestic, colorful, mythical, powerful, ancient).(DSLR camera).(wide-angle lens).(dawn)(fantasy photography).(Kodak Ektar 100)",
    #     "negative_prompt": "",
    #     "n": 1,
    #     "response_format": "url",
    #     "size":"1366x768",
    #     "num_inference_steps": 20,
    #     "seed": None
    # }

    # request = FluxImageRequest(model="flux", prompt="a dog", size="1024x1024", num_inference_steps=1)
    # request = FluxImageRequest(model="flux-pro", prompt="a dog", size="10x10", num_inference_steps=1)

    data = {'model': 'flux-schnell', 'prompt': '画一个2025年电脑如何一键重装系统win10教程详解的封面图', 'n': 1,
            'size': '680x400'}
    request = FluxImageRequest(**data)

    print(request)
    # request = SDImageRequest(
    #     # model="stable-diffusion-2-1",
    #     # model="stable-diffusion-xl-base-1.0",
    #     model="stable-diffusion-3-5-large",
    #     # model="stable-diffusion",
    #
    #     prompt="an island near sea, with seagulls, moon shining over the sea, light house, boats int he background, fish flying over the sea",
    #     size="576x1024",
    # )

    arun(generate(request))

    # https://api.siliconflow.cn/v1
