#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : auth
# @Time         : 2023/12/19 17:12
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

import numpy as np
from typing import Optional, Union

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

from meutils.config_utils.lark_utils import get_series, get_next_token

http_bearer = HTTPBearer()


# 定义获取token的函数

async def get_bearer_token(
        auth: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)
) -> Optional[str]:
    """
    获取Bearer token
    :param auth: HTTP认证凭证
    :return: token字符串
    """
    if auth is None:
        return None

    token = auth.credentials
    if token.startswith('redis:'):  # redis里按序轮询
        if "feishu.cn" in token:
            feishu_url = token.removeprefix("redis:")
            token = await get_next_token(feishu_url, ttl=24 * 3600)  # todo: 摆脱 feishu

            # logger.debug(token)

        else:  # redis:token1,token2
            tokens = token.removeprefix("redis:").split(',')  # todo: 初始化redis
            token = np.random.choice(tokens)

    elif ',' in token:  # 内存里随机轮询
        token = np.random.choice(token.split(','))

    return token


# async def get_next_token(redis_key):
#     """轮询"""
#     if api_key := await redis_aclient.lpop(redis_key):
#         await redis_aclient.rpush(redis_key, api_key)
#         return api_key


async def get_bearer_token_for_oneapi(
        auth: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)
) -> Optional[str]:
    """
    # todo: oneapi userinfo apikey info
    """
    if auth is None:
        return None

    token = auth.credentials

    return token


if __name__ == '__main__':
    from meutils.pipe import *

    arun(get_bearer_token(HTTPAuthorizationCredentials(scheme="Bearer",
                                                       credentials="redis:https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=rWMtht")))
