#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : step_types
# @Time         : 2024/6/19 09:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BASE_URL = "https://yuewen.cn"

PASSPORT_REGISTER_DEVICE = "/passport/proto.api.passport.v1.PassportService/RegisterDevice"  # 是不是一个就行 ttl=180
PASSPORT_REFRESH_TOKEN = "/passport/proto.api.passport.v1.PassportService/RefreshToken"

API_CREATE_CHAT = "/api/proto.chat.v1.ChatService/CreateChat"
API_CHAT = "/api/proto.chat.v1.ChatMessageService/SendMessageStream"
