#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : deepinfra
# @Time         : 2024/10/31 14:04
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.schemas.image_types import ImageRequest, ImagesResponse
from meutils.notice.feishu import IMAGES, send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.apis.siliconflow.images import generate as siliconflow_generate

BASE_URL = "https://api.deepinfra.com"

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=6lr4oi"

DEFAULT_MODEL = "black-forest-labs/FLUX-1.1-pro"
MODELS = {

    "flux.1-schnell": "black-forest-labs/FLUX.1-schnell",
    "flux.1-dev": "black-forest-labs/FLUX.1-dev",
    "flux.1-pro": "black-forest-labs/FLUX.1-dev",
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

    "stable-diffusion-3-5-large": "stabilityai/stable-diffusion-3-5-large"

}

send_message = partial(
    _send_message,
    title=__name__,
    url=IMAGES
)


async def generate(request: ImageRequest, token: Optional[str] = None):
    try:
        token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL)
        headers = {"Authorization": f"Bearer {token}"}

        request.model = DEFAULT_MODEL  # MODELS.get(request.model, DEFAULT_MODEL)

        # Height of the generated image in pixels. Must be a multiple of 32 (Default: 1024, 256 ≤ height ≤ 1440)
        w, h = map(int, request.size.split("x"))

        max_size = max(w, h)
        w, h = w * 1440 / max_size, h * 1440 / max_size
        w, h = max(256, w), max(256, h)
        request.size = f"{int(w)}x{int(h)}"

        logger.debug(request)

        payload = {
            "prompt": request.prompt,
            "prompt_upsampling": True,
            "seed": request.seed,
            "safety_tolerance": 6,
            "width": w,
            "height": h
        }

        async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
            response = await client.post(f"/v1/inference/{request.model}", json=payload)
            response.raise_for_status()
            data = response.json()

            return ImagesResponse(image=data["image_url"], metadata=data)

    except Exception as e:
        logger.error(e)
        send_message(f"生成失败：{e}, 使用siliconflow重试")
        return await siliconflow_generate(request)


if __name__ == '__main__':
    arun(generate(ImageRequest(prompt="一只可爱的猫", size="1440x1440")))
