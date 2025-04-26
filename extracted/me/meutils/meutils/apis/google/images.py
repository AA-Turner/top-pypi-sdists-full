#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/4/7 13:07
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : D3 生图、编辑图

from meutils.pipe import *

from meutils.apis.google.chat import Completions, CompletionRequest

from meutils.schemas.image_types import ImageRequest




async def generate(request: ImageRequest, api_key: Optional[str] = None):
    request = CompletionRequest(
        model="gemini-2.0-flash-exp-image-generation",
        messages=[

        ],
    )
    return Completions().create_for_images(request)