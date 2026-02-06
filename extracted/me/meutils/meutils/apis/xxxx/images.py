#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/12/31 17:57
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.llm.clients import AsyncClient
from meutils.llm.openai_utils import to_openai_params

from meutils.schemas.image_types import ImageRequest, ImagesResponse

base_url = "https://aiping.cn/api/v1"


async def generate(request: ImageRequest, api_key: Optional[str] = None):
    payload = {
        "model": request.model,
        # "prompt": request.prompt,

        "input": {
            "prompt": request.prompt,
            "negative_prompt": "模糊，低质量",
            # "image": request.image  # 图像编辑模型必填
        },
        "extra_body": {
            # "size": request.size,
            "width": 2048,
            "height": 2048,
            "provider": {
                "only": [],
                "order": [],
                "sort": None,
                "output_price_range": [],
                "latency_range": []
            }
        }
    }

    client = AsyncClient(base_url=base_url, api_key=api_key)
    response = await client._client.post(
        "/images/generations",
        json=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    logger.debug(response.text)
    return response


if __name__ == '__main__':
    api_key = "QC-d433b9f117a6bc44fe11057b89aabd45-98185b4235af1510f4e0aad7b5ec7bfa"
    request = ImageRequest(
        model="Doubao-Seedream-4.5",
        prompt="给图中的狗戴上一个生日帽",
        # size="2048x2048",
        size="2K",

    )

    arun(generate(request, api_key))


"""

curl -X POST "https://aiping.cn/api/v1/images/generations" \
    -H "Authorization: Bearer QC-d433b9f117a6bc44fe11057b89aabd45-98185b4235af1510f4e0aad7b5ec7bfa" \
    -H "Content-Type: application/json" \
    -d '{
    "model": "Doubao-Seedream-4.5",
    "input": {
        "prompt": "一个宇航员在都市街头漫步",
        "negative_prompt": "模糊，低质量",
        "image": "http://wanx.alicdn.com/material/20250318/stylization_all_1.jpeg"
    },
    "extra_body": {
        "provider": {
            "only": [], 
            "order": [],
            "sort": null,
            "output_price_range": [],
            "latency_range": []
        }
    }
}'
"""