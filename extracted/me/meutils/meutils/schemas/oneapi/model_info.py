#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : model_info
# @Time         : 2024/11/21 15:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.schemas.oneapi import icons

model_info = {
    "ai-search": {
        "group": "Chatfire",
        "icon": "https://registry.npmmirror.com/@lobehub/assets-emoji-anim/1.0.0/files/assets/cowboy-hat-face.webp"
    },
    "gpt-4o": {
        "group": "OpenAI",

        # "name": "Gpt-4O",
        # "note": "gpt-4o",
        "tags": "nb",
    },

    "gpt-4o-all": {
        "group": "OpenAI Plus",

        # "name": "Gpt-4O",
        # "note": "gpt-4o",
        "tags": "nb-all",
    }
}
