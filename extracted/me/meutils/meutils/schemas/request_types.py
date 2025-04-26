#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : request_types
# @Time         : 2024/12/20 16:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

# requests.request()


class RequestTypes(BaseModel):
    method: str = "POST"

    base_url: str
    api_key: Optional[str] = None
