#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : auth
# @Time         : 2023/12/19 17:12
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 
# todo: 按模型取 key 免费模型可以写死在redis里，付费模型可以从feishu里取
import numpy as np
from typing import Optional, Union

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

from meutils.config_utils.lark_utils import get_series, get_next_token

http_bearer = HTTPBearer()


# 定义获取token的函数
async def parse_token(token: str) -> Optional[str]:
    if token is None: return None

    # 前处理
    base_url = None
    if '|' in token:
        base_url, token = token.split('|', maxsplit=1)

    if token.startswith('redis:'):  # redis里按序轮询
        if "feishu.cn" in token:  # redis:https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=Y7HVfo
            feishu_url = token.removeprefix("redis:")
            token = await get_next_token(feishu_url, ttl=24 * 3600)

            # logger.debug(token)

        else:  # redis:token1,token2
            tokens = token.removeprefix("redis:").split(',')  # todo: 初始化redis
            token = np.random.choice(tokens)

    elif token.startswith("feishu:") and "feishu.cn" in token:  # feishu 随机 feishu:https://
        feishu_url = token.removeprefix("feishu:")
        tokens = await get_series(feishu_url)
        token = np.random.choice(tokens)

    elif token.startswith("http") and "feishu.cn" in token:  # feishu 取所有 keys 主要针对 channel todo: channel:https://
        feishu_url = token
        tokens = await get_series(feishu_url, duplicated=True)
        token = '\n'.join(tokens)  # 多渠道
    elif token.startswith("channel:") and "feishu.cn" in token:  # channel 全部 channel:https://
        feishu_url = token.removeprefix("channel:")

        tokens = await get_series(feishu_url, duplicated=True)
        token = '\n'.join(tokens)  # 多渠道

    elif ',' in token:  # 内存里随机轮询
        token = np.random.choice(token.split(','))

    elif token in {"None", "none", "null"}:
        token = None

    # 后处理
    if base_url:
        token = f"{base_url}|{token}"

    return token


async def get_bearer_token(
        auth: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)
) -> Optional[str]:
    """
    获取Bearer token
    :param auth: HTTP认证凭证
    :return: token字符串
    """
    if auth is None: return None

    return await parse_token(auth.credentials)


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

    # arun(parse_token("https://ai.gitee.com/v1/rerank|5PJFN89RSDN8CCR7CRGMKAOWTPTZO6PN4XVZV2FQ"))

    arun(parse_token("https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=Gvm9dt"))
