#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/12/15 16:55
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.io.files_utils import to_bytes, to_url
from meutils.llm.clients import AsyncOpenAI
from meutils.schemas.image_types import ImageRequest

BASE_URL = "https://api.textin.com/ai/service/v1"


async def generate(request: ImageRequest, api_key: Optional[str] = None):
    app_id, secret_code = (api_key or os.getenv("TEXTIN_API_KEY")).split("|")

    logger.debug(f"{app_id, secret_code}")

    pass
