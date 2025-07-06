#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : translator_types
# @Time         : 2024/7/18 14:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


class DeeplxRequest(BaseModel):
    text: str

    source_lang: str = "auto"
    target_lang: str = "ZH"

    class Config:
        frozen = True

        json_schema_extra = {
            "example": {
                "text": "火哥AI是最棒的",
                "source_lang": "auto",
                "target_lang": "EN"
            }
        }
