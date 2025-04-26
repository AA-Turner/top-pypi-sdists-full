#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : flux
# @Time         : 2024/8/5 09:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import asyncio

from meutils.pipe import *
from meutils.config_utils.lark_utils import get_spreadsheet_values, get_next_token_for_polling
from meutils.schemas.openai_types import ImageRequest, ImagesResponse
from meutils.apis.translator import deeplx
from meutils.schemas.translator_types import DeeplxRequest
from meutils.decorators.retry import retrying
from meutils.schemas.image_types import ASPECT_RATIOS
from meutils.oss.minio_oss import Minio

from meutils.notice.feishu import send_message as _send_message

BASE_URL = "https://fluxpro.art"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=GdRbM9"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


# import fake_useragent
#
# ua = fake_useragent.UserAgent()


@retrying(max_retries=5, title=__name__, predicate=lambda x: x is True)
async def create_image(request: ImageRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL)

    prompt = (await deeplx.translate(DeeplxRequest(text=request.prompt, target_lang="EN"))).get("data")

    payload = {
        "prompt": prompt,
        "negative_prompt": request.negative_prompt,
        "aspect_ratio": request.size if request.size in ASPECT_RATIOS else "1:1",

        "guidance": request.guidance_scale,
        "steps": request.num_inference_steps,
        "nsfw_level": request.nsfw_level  # 0 1 2 3
    }

    headers = {
        'Cookie': token,
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post("/api/prompts/flux", json=payload)

        logger.debug(response.status_code)

        if response.status_code in {429, 403}:  # 触发重试
            logger.debug(f"{response.status_code} {token}")
            send_message(f"{response.status_code} {token}")
            return True

        if response.is_success:
            data = response.json().get('assets', [])
            image_data = []

            # asyncio.gather()

            async def atask(url):
                resp = await client.get(url, follow_redirects=True)
                file_object = await Minio().put_object_for_openai(
                    file=resp.content,
                    filename=f"{shortuuid.random()}.webp"
                )
                return {"url": file_object.filename, "revised_prompt": prompt}

            tasks = [atask(i.get('src')) for i in data]
            image_data = await asyncio.gather(*tasks)

            return ImagesResponse.construct(data=image_data)

        response.raise_for_status()


# {
#     "id": "clzianobv017nq200g3fd2zb1",
#     "prompt": "borttiful scenery nature glass bottle landscape, , purple galaxy seed",
#     "negative_prompt": "",
#     "aspect_ratio": "1:1",
#     "assets": [
#         {
#             "src": "/api/view/clzianobv017nq200g3fd2zb1/0.webp"
#         }
#     ],
#     "model": "FLUX.1 [pro]",
#     "created_at": "2024-08-06T10:45:19.723Z",
# }


if __name__ == '__main__':
    token="_ga=GA1.1.378655276.1724288763; next-auth.csrf-token=fc3c64918d60db1bc897b389c1b736dc6a4329f6675a485d428d7dd36d46695f%7C7d52961d266b22ef57ec398c4119f903c7a62c853eb69a9f4cc4742829bacce7; next-auth.callback-url=http%3A%2F%2Ffluxpro.art; next-auth.session-token=17394b70-92fc-43dc-ac7b-77a635076298; _ga_KJL6XMRTB6=GS1.1.1724293123.2.1.1724297068.0.0.0"
    arun(create_image(ImageRequest(prompt="画条狗", size='1024x512'), token=token))
    # arun(create_image(ImageRequest(prompt="画条狗"), token=token))
