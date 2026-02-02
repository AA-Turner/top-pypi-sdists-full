#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : token_monitor
# @Time         : 2024/4/22 14:50
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : refresh_token key 鉴权 /token/check
# /v1/token/kimi_xxxxx # kimi_sk-...
# /v1/token/glm_xxxxx
# 从配置中心读取 keys
# 定时监测，失效剔除【飞书告警】
# 提供get接口，客户端定时拉取【统计使用频次，均匀采样】
# 检测接口 并且加入轮询库 借助配置中心
# 最原始检测逻辑
#######核心：检查token加入轮询配置中，15分钟检查一下

import httpx

# 无效的令牌 401 403

from meutils.pipe import *
from meutils.async_utils import arequest, arun

base_url = "http://154.3.0.117:39002"

payload = {
    "token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9...",
    "base_url": ""
}

print(arun(arequest(url='/token/check', method='post', base_url=base_url, payload=payload)).json())
