#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/11/23 23:27
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.llm.openai_utils import to_openai_params
from meutils.schemas.image_types import ImageRequest, ImagesResponse
from openai import AsyncOpenAI


async def generate(request: ImageRequest, api_key: str = None, base_url: str = None):
    base_url = base_url or "https://api.aimlapi.com/v1"
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
    )
    logany(request)

    extra_body = {"num_images": request.n, "image_urls": None}
    if request.image_urls:
        extra_body['image_urls'] = request.image_urls

        if request.model.startswith(('google/gemini')):
            request.model = f"{request.model.strip('-edit')}-edit"

    data = to_openai_params(request)
    data["extra_body"] = {**data['extra_body'], **extra_body}

    logany(bjson(data))

    response = await client.images.generate(**data)
    logany(response)

    return response


if __name__ == "__main__":
    # main()

    api_key = "96f845c6e4664ba2bfa65aa1111693f5"

    data = {
        "prompt": "带个墨镜",
        "model": "google/gemini-3-pro-image-preview",
        "image_urls": [
            "https://s3.ffire.cc/files/jimeng.jpg",
        ],
        "aspect_ratio": "2:3"
    }

    data = {
        "model": "klingai/image-o1",
        "prompt": "Combine the images so the T-Rex is wearing a business suit, sitting in a cozy small café, drinking from the mug. Blur the background slightly to create a bokeh effect.",
        # "image": [
        #     "https://raw.githubusercontent.com/aimlapi/api-docs/main/reference-files/t-rex.png",
        #     "https://raw.githubusercontent.com/aimlapi/api-docs/main/reference-files/blue-mug.jpg",
        # ],
    }

    request = ImageRequest(**data)

    arun(generate(request, api_key))
