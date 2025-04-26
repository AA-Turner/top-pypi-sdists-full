#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : headers
# @Time         : 2025/2/23 00:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from fastapi import FastAPI, Request, Depends, HTTPException
from typing import Dict, Optional


# 定义一个依赖函数来获取所有请求头
# def get_headers(request: Request) -> Dict[str, str]:
#     return dict(request.headers)

def get_headers(request: Request):
    return dict(request.headers)

# lambda request: dict(request.headers)
# @app.get("/headers/")
# async def read_headers(headers: Dict[str, str] = Depends(get_headers)):
#     # 在这里你可以使用 headers 字典
#     if "upstream_api_key" not in headers:
#         raise HTTPException(status_code=400, detail="API key is required")
#
#     # 返回所有请求头
#     return {"headers": headers}
