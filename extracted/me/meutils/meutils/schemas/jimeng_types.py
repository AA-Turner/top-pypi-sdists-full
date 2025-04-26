#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : jimeng_types
# @Time         : 2024/12/16 18:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import uuid

from meutils.pipe import *

BASE_URL = "https://jimeng.jianying.com"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=zkPAHw"

FEISHU_URL_MAPPER = {
    "758": "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=6JWRxt"  # 柏拉图
}

MODELS_MAP = {
    "jimeng-2.1": "high_aes_general_v21_L:general_v2.1_L",

    "jimeng-2.0-pro": "high_aes_general_v20_L:general_v2.0_L",
    "high_aes_general_v20_L:general_v2.0_L": "high_aes_general_v20_L:general_v2.0_L",

    "jimeng-2.0": "high_aes_general_v20:general_v2.0",
    "jimeng-1.4": "high_aes_general_v14:general_v1.4",
    "jimeng-xl-pro": "text2img_xl_sft",

    "default": "high_aes_general_v30l:general_v3.0_18b"
}
