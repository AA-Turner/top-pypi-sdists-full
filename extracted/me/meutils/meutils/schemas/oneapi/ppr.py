#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ppr
# @Time         : 2026/2/26 11:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

PPR = 0.75

models = {
    "Qwen3.5-35B-A3B": 0.02,
    "DeepSeek-V3.2": 0.03,

    "MiniMax-M2.5": 0.02,

    "glm-4.7": 0.03,
    "glm-5": 0.05,

    "Kimi-K2.5": 0.08,

    # 闭源
    "doubao-seed-2.0-code": 0.05,
    "doubao-seed-2.0-pro": 0.05,
}

if __name__ == '__main__':
    data = {m.lower(): PPR * p for m, p in models.items()}
    data = dict(zip(data, np.ceil(1000 * np.array(list(data.values()))) / 1000))

    print(bjson(data))
