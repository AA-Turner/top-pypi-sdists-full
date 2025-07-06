#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : generations
# @Time         : 2025/6/11 17:06
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 统一收口

from meutils.pipe import *
from meutils.llm.clients import AsyncClient
from meutils.llm.openai_utils import to_openai_params

from meutils.schemas.image_types import ImageRequest

from meutils.apis.fal.images import generate as fal_generate


async def generate(
        request: ImageRequest,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
):
    if base_url:  # 优先级最高
        client = AsyncClient(api_key=api_key, base_url=base_url)
        return await client.images.generate(**to_openai_params(request))

    if request.model.startswith("fal-ai"):
        return await fal_generate(request, api_key)


if __name__ == '__main__':
    arun(generate(ImageRequest(model="flux", prompt="笑起来")))
