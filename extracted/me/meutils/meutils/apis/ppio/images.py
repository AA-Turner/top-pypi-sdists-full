#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/10/9 11:55
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import httpx

from meutils.pipe import *
from meutils.llm.clients import AsyncClient

from meutils.schemas.image_types import ImageRequest, ImagesResponse


async def generate(request: ImageRequest, api_key: str, base_url: Optional[str] = None):
    request.prompt = request.prompt[-2000:]

    if request.model.startswith("gemini"):
        # model = "gemini-2.5-flash-image-preview"
        if request.image:
            request.model += "-image-edit"
        else:
            request.model += "-text-to-image"

    payload = {
        "model": request.model,
        "prompt": request.prompt
    }

    # gemini-2.5-flash-image-preview-text-to-image
    if request.image_urls:
        payload["image_urls"] = request.image_urls

    logger.debug(bjson(payload))

    base_url = f"https://api.ppinfra.com/v3"
    client = AsyncClient(base_url=base_url, api_key=api_key)
    response = await client.post(
        request.model,
        body=payload,
        cast_to=object
    )
    if image_urls := response.get("image_urls"):
        data = [{"url": image_url} for image_url in image_urls]
        return ImagesResponse(data=data)
    else:
        raise Exception(f"生成图片失败: {response} \n\n{request}")


if __name__ == '__main__':
    # request = ImageRequest(
    #     model="gemini-2.5-flash-image-preview",
    #     # prompt="a cat",
    #
    # )

    request = ImageRequest(
        model="gemini-2.5-flash-image-preview",
        prompt="将小鸭子放在女人的t恤上",
        # prompt="海底世界",
        size="1024x1024",
        image=[
            "https://v3.fal.media/files/penguin/XoW0qavfF-ahg-jX4BMyL_image.webp",
            "https://v3.fal.media/files/tiger/bml6YA7DWJXOigadvxk75_image.webp"
        ]
    )

    ""

    print()

    arun(generate(request, api_key="sk_7ceUKU7SnW36hHyxPR4mGiPeDaCx4ClhkySmSs_5cgg"))


    """
    
curl -X 'POST' \
  'https://image.chatfire.cn/images/v1/images%2Fgenerations?base_url=http%3A%2F%2Fall.chatfire.cn%2Fppinfra%2Fv1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer sk_DOte_nsLGmI9s-nZFfgA9_DGTBbW3YMZyRC7bypeDiI' \
  -d '{
    "model": "gemini-2.5-flash-image-preview",
    "prompt": "将小鸭子放在女人的t恤上",
    "size": "1024x1024",
    "image": [
        "https://v3.fal.media/files/penguin/XoW0qavfF-ahg-jX4BMyL_image.webp",
        "https://v3.fal.media/files/tiger/bml6YA7DWJXOigadvxk75_image.webp"
    ]
}'


    """

