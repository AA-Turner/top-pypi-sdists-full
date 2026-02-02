#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : luma_types
# @Time         : 2024/7/22 10:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

# {
#     "user_prompt": "Grazing cows move slowly across an idyllic meadow, the camera tracking alongside them in a smooth side-angle motion",
#     "expand_prompt": true,
#     "aspect_ratio": "16:9"
# }
BASE_URL = "https://internal-api.virginia.labs.lumalabs.ai/api/photon/v1"  # luma.chatfire.cc
BASE_URL = "https://luma.chatfire.cc/api/photon/v1"

EXAMPLES = [
    {
        "user_prompt": "清凉夏季美少女，微卷短发，运动服，林间石板路，斑驳光影，超级真实，16K",
        "expand_prompt": True,
        "aspect_ratio": "16:9"
    },

    {
        "user_prompt": "清凉夏季美少女，微卷短发，运动服，林间石板路，斑驳光影，超级真实，16K",
        "expand_prompt": True,
        "aspect_ratio": "16:9",
        "image_url": "https://h2.inkwai.com/bs2/upload-ylab-stunt/ai_portal/1721561429/3z7bHmSC1Y/3yrmpqh7typspfcchmepar.png",
        "image_end_url": "https://p2.a.kwimgs.com/bs2/upload-ylab-stunt/ai_portal/1721561524/GPoJWxBS8s/y9wlbuku3exeo7ra85s4su.png"
    },

]


# /user/generations/?offset=0&limit=12

# https://internal-api.virginia.labs.lumalabs.ai/api/photon/v1/generations/56d3e505-a1f5-475c-9ba7-8beeac8aa2ac/extend
class LumaRequest(BaseModel):
    user_prompt: str = ""
    expand_prompt: bool = True  # 提示词优化
    aspect_ratio: str = "16:9"
    image_url: str = ""
    image_end_url: str = ""

    # def __init__(self, /, **data: Any):
    #     super().__init__(**data)

    class Config:
        json_schema_extra = {
            "example": EXAMPLES
        }


if __name__ == '__main__':
    print(LumaRequest(user_prompt='xxxx'))
