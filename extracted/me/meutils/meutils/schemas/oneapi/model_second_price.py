#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : seconds
# @Time         : 2025/10/31 19:15
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo 接口
import math

import numpy as np

from meutils.pipe import *

TIMES = 4
TIMES_5 = 0.5
TIMES_6 = 0.6
TIMES_7 = 0.7
TIMES_8 = 0.8

data = {
    # kling
    "kling-video-o1": 0.4,
    "kling-video-o1-edit": 0.4,
    "kling-video-2.6": 0.07 * TIMES,
    "klingai/avatar-standard": 0.059 * TIMES,
    "klingai/avatar-pro": 0.121 * TIMES,
    "bytedance/omnihuman/v1.5": 0.168 * TIMES,

    # hailuo
    "minimax-hailuo-02_768p": 0.56 / 10 * TIMES,
    "minimax-hailuo-02_1080p": 0.49 / 6 * TIMES,
    "minimax-hailuo-2.3_768p": 0.56 / 10 * TIMES,
    "minimax-hailuo-2.3_1080p": 0.49 / 6 * TIMES,
    "minimax-hailuo-2.3-fast_768p": 0.32 / 10 * TIMES,
    "minimax-hailuo-2.3-fast_1080p": 0.33 / 6 * TIMES,

    "viduq2-turbo_720p": 0.2,
    "viduq2-turbo_1080p": 0.8,
    "viduq2-pro_720p": 0.2,
    "viduq2-pro_1080p": 0.8,

    # wan
    "wan2.5_480p": 0.05 * TIMES,
    "wan2.5_720p": 0.1 * TIMES,
    "wan2.5_1080p": 0.15 * TIMES,
    "wan2.6_720p": 0.1 * TIMES,
    "wan2.6_1080p": 0.15 * TIMES,

    # sora
    "sora-2": 0.1 * TIMES,
    "sora-2-pro": 0.3 * TIMES,

    # veo
    "veo3.1_720p": 0.4 * TIMES,
    "veo3.1_1080p": 0.4 * TIMES,
    "veo3.1-fast_720p": 0.15 * TIMES,
    "veo3.1-fast_1080p": 0.15 * TIMES,

    # seedance
    'doubao-seedance-1-0-pro_480p': 1.46 / 10 * 0.6,
    'doubao-seedance-1-0-pro_720p': 3.38 / 10 * 0.6,
    'doubao-seedance-1-0-pro_1080p': 7.34 / 10 * 0.6,
    'doubao-seedance-1-0-pro-fast_480p': 0.41 / 10 * 0.9,
    'doubao-seedance-1-0-pro-fast_720p': 0.95 / 10 * 0.9,
    'doubao-seedance-1-0-pro-fast_1080p': 2.06 / 10 * 0.9,
    'doubao-seedance-1-0-lite_480p': 0.41 / 10 * 0.9,
    'doubao-seedance-1-0-lite_720p': 0.95 / 10 * 0.9,
    'doubao-seedance-1-0-lite_1080p': 2.06 / 10 * 0.9,

    "doubao-seedance-1-5-pro_480p": 0.8 / 10 * 0.6,
    "doubao-seedance-1-5-pro_720p": 1.6 / 10 * 0.6,
    "doubao-seedance-1-5-pro_1080p": 3 / 10 * 0.6,

    # 'doubao-seedance-1-0-lite_480p': 0.97 / 10,
    # 'doubao-seedance-1-0-lite_720p': 2.26 / 10,
    # 'doubao-seedance-1-0-lite_1080p': 4.9 / 10,

    # 混元
    "hunyuan-video-v1.5": 0.2,

    # pixverse
    "pixverse-v5.5_720p": 1.386 / 10 * TIMES,
    "pixverse-v5.5_1080p": 2.52 / 8 * TIMES,

    # runway
    "runway/gen4-turbo": 0.053 * TIMES,
    "runway/gen4-aleph": 0.158 * TIMES,

    # luma
    "luma/ray-flash-2_720p": 0.25 / 5 * TIMES,
    "luma/ray-flash-2_1080p": 0.3 / 5 * TIMES,
    "luma/ray-flash-2_4k": 0.5 / 5 * TIMES,

    "luma/ray-2_720p": 0.25 / 4 * TIMES,
    "luma/ray-2_1080p": 0.3 / 4 * TIMES,
    "luma/ray-2_4k": 0.5 / 4 * TIMES,

}

if __name__ == '__main__':
    _ = ','.join([k for k, v in data.items() if k.startswith("doubao")])
    print(_)

    data = dict(zip(data, np.ceil(1000 * np.array(list(data.values()))) / 1000))
    print(json.dumps(data, indent=4))
