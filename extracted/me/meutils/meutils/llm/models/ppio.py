#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ppio
# @Time         : 2025/8/22 11:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

models = {

    "glm-4.5": "zai-org/glm-4.5",

    "qwen3-235b-a22b-thinking-2507": "qwen/qwen3-235b-a22b-thinking-2507",
    "qwen3-235b-a22b-instruct-2507": "qwen/qwen3-235b-a22b-instruct-2507",
    "kimi-k2-0711-preview": "moonshotai/kimi-k2-instruct",
    "deepseek-v3.1": "deepseek/deepseek-v3.1",
    "deepseek-v3": "deepseek/deepseek-v3-turbo",
    "deepseek-v3-0324": "deepseek/deepseek-v3-0324",
    "deepseek-v3-250324": "deepseek/deepseek-v3-0324",

    # "deepseek/deepseek-v3/community"
    "deepseek-r1": "deepseek/deepseek-r1-turbo",
    "deepseek-reasoner": "deepseek/deepseek-r1-turbo",

    "deepseek-r1-250528": "deepseek/deepseek-r1-0528",

}

print(','.join(models))
