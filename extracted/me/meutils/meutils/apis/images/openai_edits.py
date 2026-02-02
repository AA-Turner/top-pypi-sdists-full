#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_edits
# @Time         : 2025/5/30 13:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : formdata
"""
图片编辑

即梦编辑图像 垫图

flux



"""

from meutils.pipe import *
from openai import OpenAI
from meutils.schemas.image_types import ImageEditRequest

# from meutils.llm.openai_utils import to_openai_params

openai = OpenAI(
    base_url="http://0.0.0.0:8000/v1",
    api_key="sk-1234567890",
)

images = [open("image1.webp", "rb"), open("image2.webp", "rb")]

# images = open("image1.webp", "rb")

r = openai.images.edit(
    model="fal-ai/flux-pro/kontext",
    image=images,
    prompt="Put the little duckling on top of the woman's t-shirt.",
    n=1,
    size="1024x1024"
)

# r = openai.images.generate(
#     model = "fal-ai/imagen4/preview",
#     prompt='a cat',
# )
# def edit(
#         self,
#         *,
#         image: Union[FileTypes, List[FileTypes]],
#         prompt: str,
#         background: Optional[Literal["transparent", "opaque", "auto"]] | NotGiven = NOT_GIVEN,
#         mask: FileTypes | NotGiven = NOT_GIVEN,
#         model: Union[str, ImageModel, None] | NotGiven = NOT_GIVEN,
#         n: Optional[int] | NotGiven = NOT_GIVEN,
#         quality: Optional[Literal["standard", "low", "medium", "high", "auto"]] | NotGiven = NOT_GIVEN,
#         response_format: Optional[Literal["url", "b64_json"]] | NotGiven = NOT_GIVEN,
#         size: Optional[Literal["256x256", "512x512", "1024x1024", "1536x1024", "1024x1536", "auto"]]
#               | NotGiven = NOT_GIVEN,
#         user: str | NotGiven = NOT_GIVEN,
#         # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
#         # The extra values given here take precedence over values defined on the client or passed to this method.
#         extra_headers: Headers | None = None,
#         extra_query: Query | None = None,
#         extra_body: Body | None = None,
#         timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
