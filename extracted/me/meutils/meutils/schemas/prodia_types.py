#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : prodia_types
# @Time         : 2024/8/14 14:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BASE_URL = "https://api.prodia.com/v1"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=71b08f"


class FaceswapRequest(BaseModel):
    sourceUrl: str
    targetUrl: str
