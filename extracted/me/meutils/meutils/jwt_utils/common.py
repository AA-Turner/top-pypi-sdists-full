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

# Header and payload
header = {
    "alg": "HS512",
    "type": "JWT"
}


payload = {
    "jti": "80004477",
    "rol": "ROLE_REGISTER",
    "iss": "OpenXLab",
    "clientId": "lkzdx57nvy22jkpq9x2w",
    "phone": "",
    "uuid": "73a8d9b0-8bbf-4973-9b71-4b687ea23a78",
    "email": "313303303@qq.com",

    "iat": int(time.time()),
    "exp": int(time.time()) + 3600
}

# Your secret key
secret = ""

# Create the JWT
token = jwt.encode(payload, secret, algorithm="HS512", headers=header)

print(token)



