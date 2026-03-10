#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : logfire_middleware
# @Time         : 2026/3/2 23:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import logfire
from opentelemetry_instrumentor_dramatiq import DramatiqInstrumentor

# 1. 配置 Logfire
logfire.configure(token=os.getenv("LOGFIRE_TOKEN_TASKS"))

# 2. 启用 Dramatiq 自动监控
DramatiqInstrumentor().instrument()
