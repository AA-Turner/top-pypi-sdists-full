#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : mystic
# @Time         : 2024/8/21 13:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.config_utils.lark_utils import get_spreadsheet_values, get_next_token_for_polling
from meutils.schemas.openai_types import ImageRequest, ImagesResponse
from meutils.apis.translator import deeplx
from meutils.schemas.translator_types import DeeplxRequest
from meutils.schemas.image_types import ASPECT_RATIOS

from meutils.decorators.retry import retrying

from meutils.notice.feishu import send_message as _send_message

# https://www.mystic.ai/v4/runs/run_64c682fd3a6f4da4bbdacec7720add5f

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=7VYdjp"

BASE_URL = "https://www.mystic.ai/v4/runs"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


@retrying(max_retries=5, title=__name__)
async def create_image(request: ImageRequest, token: Optional[str] = None, async_run: bool = False):
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL)

    prompt = (await deeplx.translate(DeeplxRequest(text=request.prompt, target_lang="EN"))).get("data")

    width, height = map(int, ASPECT_RATIOS.get(request.size, '1024x1024').split('x'))

    if 'pro' in request.model:
        width = max(width, 1440)
        height = max(height, 1440)

        payload = {
            "pipeline": "pipeline_0710417cf4464e72b03dc9ef17773253",
            "inputs": [
                {
                    "type": "dictionary",
                    "value": {
                        "prompt": prompt,
                        "prompt_upsampling": False,

                        "width": width,
                        "height": height,

                        "steps": 15,
                        "guidance": 3,

                        "variant": "flux.1-pro",

                        "safety_tolerance": request.nsfw_level,  # 小等于6
                        "interval": 2,
                        "seed": 0,

                    }
                }
            ],
            "async_run": async_run
        }
    else:  # dev
        payload = {
            "pipeline": "pipeline_8a895066ef054c2e89cdf316611a1937",
            "inputs": [
                {
                    "type": "string",
                    "value": prompt
                },
                {
                    "type": "dictionary",
                    "value": {

                        "height": 1024,
                        "width": 1024,

                        "guidance_scale": 4,
                        "max_sequence_length": 256,
                        "num_images_per_prompt": 1,
                        "num_inference_steps": 15,
                        "seed": 1
                    }
                }
            ],
            "async_run": True
        }

    headers = {
        'Cookie': token,
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post(BASE_URL, json=payload)

        logger.debug(response.status_code)
        logger.debug(response.text)

        if response.is_success:
            data = response.json()
            logger.debug(data)

            return ImagesResponse(data=[data['outputs'][0]['file']])


if __name__ == '__main__':
    arun(create_image(ImageRequest(prompt="一条狗")))
