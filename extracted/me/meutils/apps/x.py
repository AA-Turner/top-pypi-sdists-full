#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2025/5/8 11:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *




def jwt_token_decode(jwt_token):
    # 提取 payload 部分
    payload_part = jwt_token.split('.')[1]

    # 对 payload 进行 Base64 解码
    try:
        # 尝试标准 Base64 解码
        decoded_payload = base64.b64decode(payload_part + '==', validate=True).decode('utf-8')
    except base64.binascii.Error:
        # 尝试 URL 安全的 Base64 解码
        decoded_payload = base64.urlsafe_b64decode(payload_part + '==').decode('utf-8')

    # 解析 JSON 字符串
    payload = json.loads(decoded_payload)

    return payload


if __name__ == '__main__':
    jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDg3Mzg4MTQsInVzZXIiOnsiaWQiOiIyMjkwODQ3NTA2MDEzODgwMzciLCJuYW1lIjoi5bCP6J665bi9ODAzNyIsImF2YXRhciI6Imh0dHBzOi8vY2RuLmhhaWx1b2FpLmNvbS9wcm9kL3VzZXJfYXZhdGFyLzE3MDYyNjc3MTEyODI3NzA4NzItMTczMTk0NTcwNjY4OTY1ODk2b3ZlcnNpemUucG5nIiwiZGV2aWNlSUQiOiIyNDM3MTMyNTI1NDU5ODY1NjIiLCJpc0Fub255bW91cyI6ZmFsc2V9fQ.o0SoZMSTWkXNHxJjt3Ggby5MJWSfd-rnK_I95T_WMP8"
    print(jwt_token_decode(jwt_token))