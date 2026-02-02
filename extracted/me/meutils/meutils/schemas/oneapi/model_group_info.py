#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : model_group_info
# @Time         : 2024/11/21 15:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo 表格

from meutils.pipe import *
from meutils.schemas.oneapi import icons

model_group_info = {
    "Chatfire": {
        "name": "Chatfire",
        "desc": "ChatfireAPI，国内领先的API厂商",
        "icon": "https://registry.npmmirror.com/@lobehub/assets-emoji-anim/1.0.0/files/assets/cowboy-hat-face.webp",
        "notice": "<h1 align = \"center\">[点击查看接入文档](https://api.chatfire.cn/docs)</h1>"
    },
    "OpenAI": {
        "name": "OpenAI",
        "desc": "openai",
        "icon": icons.openai,
        "notice": "<h1 align = \"center\">[点击查看接入文档](https://api.chatfire.cn/docs)</h1>"
    },
    "OpenAI Plus": {
        "name": "OpenAI Plus",

        "desc": "这类模型都是由 Openai ChatGPT逆向工程而来的",
        "icon": icons.openai_plus,
        "notice": "<h1 align = \"center\">[点击查看接入文档](https://api.chatfire.cn/docs)</h1>"
    },

    "Claude": {
        "name": "Claude",
        "desc": "claude",
        "icon": icons.claude,
        "notice": "<h1 align = \"center\">[点击查看接入文档](https://api.chatfire.cn/docs)</h1>"
    },

    "Flux": {
        "name": "Flux",
        "desc": "flux",
        "icon": icons.flux,
        "notice": "<h1 align = \"center\">[点击查看接入文档](https://api.chatfire.cn/docs)</h1>"
    }
}
