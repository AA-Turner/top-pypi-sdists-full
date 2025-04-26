#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/4/10 16:07
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from meutils.llm.clients import AsyncOpenAI
from meutils.llm.openai_utils import to_openai_params
from meutils.schemas.image_types import ImageRequest, ImagesResponse


class Images(object):
    def __init__(
            self,
            base_url: Optional[str] = None,
            api_key: Optional[str] = None,
            http_client: Optional[httpx.AsyncClient] = None
    ):
        self.base_url = base_url
        self.api_key = api_key

        self.client = AsyncOpenAI(base_url=self.base_url, api_key=self.api_key, http_client=http_client)

    async def generate(self, request: ImageRequest):
        data = to_openai_params(request)
        response = await self.client.images.generate(**data)  # todo: 兼容 response_format="b64_json"

        return response
