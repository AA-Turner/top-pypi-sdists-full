#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2026/3/17 23:33
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from meutils.schemas.image_types import ImageRequest
from meutils.llm.openai_utils import to_openai_params

from openai import AsyncOpenAI


async def generate(request: ImageRequest, api_key: Optional[str] = None):
    client = AsyncOpenAI(
        base_url="https://api.x.ai/v1",
        api_key=api_key or os.getenv("GROK_API_KEY"),
    )
    data = to_openai_params(request)

    # extra_body={"aspect_ratio": "16:9"},
    # extra_body={"resolution": "2k"},

    if request.image_urls:
        if len(request.image_urls) == 1:
            data["image"] = {"url": request.image_urls[0], "type": "image_url"}
        else:
            data["images"] = [
                {
                    "url": url,
                    "type": "image_url"
                } for url in request.image_urls
            ]

        # logger.debug(bjson(data))
        data.pop("size", None)
        response = await client.post("/images/edits", body=data, cast_to=object)

        return response

    # logger.debug(bjson(data))
    data.pop("size", None)
    return await client.images.generate(**data)


if __name__ == '__main__':
    request = ImageRequest(
        model="grok-imagine-image",
        # model="grok-imagine-image_2k",

        size="16x9",
        prompt="带个墨镜",
        image="https://s3.ffire.cc/files/jimeng.jpg"

        # prompt="Add the cat from the first image to the second one.",
        # image=[
        #     # "https://docs.x.ai/assets/api-examples/images/image-edit-1.jpeg",
        #     # "https://docs.x.ai/assets/api-examples/images/image-edit-2.jpeg"
        # ]

    )

    arun(generate(request))
