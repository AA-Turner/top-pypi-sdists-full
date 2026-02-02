#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2024/10/28 20:57
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

import jwt
import time
import datetime
#
# # Header and payload
# header = {
#     "alg": "HS512",
#     "type": "JWT"
# }
#
#
# payload = {
#     "jti": "80004477",
#     "rol": "ROLE_REGISTER",
#     "iss": "OpenXLab",
#     "clientId": "lkzdx57nvy22jkpq9x2w",
#     "phone": "",
#     "uuid": "73a8d9b0-8bbf-4973-9b71-4b687ea23a78",
#     "email": "313303303@qq.com",
#
#     "iat": int(time.time()),
#     "exp": int(time.time()) + 3600
# }
#
# # Your secret key
# secret = ""
#
# # Create the JWT
# token = jwt.encode(payload, secret, algorithm="HS512", headers=header)
#
# print(token)



@lru_cache()
def decode_jwt_token(jwt_token):
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
    def get_base_url(token):
        if "小螺帽" not in str(decode_jwt_token(token)):
            return "BASE_URL_ABROAD"
        else:
            return "BASE_URL"

    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDg3Mzg4MTQsInVzZXIiOnsiaWQiOiIyMjkwODQ3NTA2MDEzODgwMzciLCJuYW1lIjoi5bCP6J665bi9ODAzNyIsImF2YXRhciI6Imh0dHBzOi8vY2RuLmhhaWx1b2FpLmNvbS9wcm9kL3VzZXJfYXZhdGFyLzE3MDYyNjc3MTEyODI3NzA4NzItMTczMTk0NTcwNjY4OTY1ODk2b3ZlcnNpemUucG5nIiwiZGV2aWNlSUQiOiIyNDM3MTMyNTI1NDU5ODY1NjIiLCJpc0Fub255bW91cyI6ZmFsc2V9fQ.o0SoZMSTWkXNHxJjt3Ggby5MJWSfd-rnK_I95T_WMP8"

    # jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTAxMjg4NTIsInVzZXIiOnsiaWQiOiIzNzQwMTM3NzUyNzg4ODY5MTciLCJuYW1lIjoiTmFodWVsIE1vbGluYSIsImF2YXRhciI6IiIsImRldmljZUlEIjoiMzEzMzc0MTIyMjEyMjc4MjczIiwiaXNBbm9ueW1vdXMiOmZhbHNlfX0.uxTtDTcPT07piVA-x3N2ms2VrRN3JwcU99g_HJLwqLE"
    print(get_base_url(jwt_token))
