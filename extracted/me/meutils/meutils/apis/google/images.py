#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/4/7 13:07
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : D3 生图、编辑图
"""
# {
    #     "index": 0,
    #     "type": "image_url",
    #     "image_url": {
    #         "url": "b64"
    #     }
    #
    # }

"""

from meutils.pipe import *
from meutils.io.files_utils import to_url, to_base64
from meutils.str_utils import parse_base64
from meutils.llm.clients import AsyncOpenAI
from meutils.apis.images.edits import edit_image, ImageProcess

from meutils.schemas.image_types import ImageRequest, ImagesResponse
from meutils.schemas.openai_types import CompletionRequest


async def openai_generate(request: ImageRequest, api_key: Optional[str] = None, base_url: Optional[str] = None):
    api_key = api_key or os.getenv("OPENROUTER_API_KEY")

    is_hd = False
    if request.model.endswith("-hd"):
        is_hd = True
        request.model = request.model.removesuffix("-hd")

    image_urls = request.image_urls
    # image_urls = await to_url(image_urls, filename='.png', content_type="image/png")
    # image_urls = await to_base64(image_urls, content_type="image/png")

    image_urls = [
        {
            "type": "image_url",
            "image_url": {
                "url": image_url
            }
        }
        for image_url in image_urls or []
    ]

    _request = CompletionRequest(
        model=request.model,
        stream=False,
        max_tokens=None,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": request.prompt
                    },
                    *image_urls
                ]
            }
        ],
    )

    data = _request.model_dump(exclude_none=True)

    client = AsyncOpenAI(
        base_url=base_url,
        api_key=api_key
        # base_url="https://openrouter.ai/api/v1",
        # base_url="https://all.chatfire.cn/openrouter/v1",
        # api_key=api_key or os.getenv("OPENROUTER_API_KEY"),

    )

    completion = await client.chat.completions.create(**data)
    logger.debug(completion)
    if completion and completion.choices and (revised_prompt := completion.choices[0].message.content.strip()):
        logger.debug(revised_prompt)

        if (hasattr(completion.choices[0].message, "images") and (images := completion.choices[0].message.images)):

            image_urls = [image['image_url']['url'] for image in images]
        else:
            image_urls = parse_base64(revised_prompt)

        if is_hd:
            # logger.debug(image_urls)
            tasks = [edit_image(ImageProcess(model="clarity", image=image_url)) for image_url in image_urls]
            responses = await asyncio.gather(*tasks)

            image_urls = [dict(response.data[0])["url"] for response in responses if response.data]
            response = ImagesResponse(image=image_urls)

        else:
            image_urls = await to_url(image_urls, filename=f'{shortuuid.random()}.png', content_type="image/png")
            response = ImagesResponse(image=image_urls)

        # logger.debug(response)

        if response.data:
            return response

    # content_filter
    raise Exception(f"Image generate failed: {completion}")


if __name__ == '__main__':
    # base_url = "https://all.chatfire.cn/openrouter/v1"
    # api_key = os.getenv("OPENROUTER_API_KEY")

    # api_key = "sk-MAZ6SELJVtGNX6jgIcZBKuttsRibaDlAskFAnR7WD6PBSN6M"
    # base_url = "https://new.yunai.link/v1"

    # base_url = "https://api.huandutech.com/v1"
    # api_key = "sk-qOpbMHesasoVgX75ZoeEeBEf1R9dmsUZVAPcu5KkvLFhElrn"

    base_url = "http://209.222.101.251:3014/v1beta"

    api_key = "sk-S6rE16CQyLC2ONtbMO5gdOqkSzDhdWJXAr2oQxMUhxZUV2644"

    request = ImageRequest(
        # model="google/gemini-2.5-flash-image-preview:free",
        # model="google/gemini-2.5-flash-image-preview:free-hd",

        model="gemini-2.5-flash-image",

        # prompt="裸体女孩",

        prompt="a cat",
        # image=["https://oss.ffire.cc/files/kling_watermark.png"],
    )

    r = arun(
        openai_generate(
            request, base_url=base_url, api_key=api_key
        )
    )
