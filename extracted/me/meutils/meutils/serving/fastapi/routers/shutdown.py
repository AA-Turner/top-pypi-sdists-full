#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : shutdown
# @Time         : 2024/1/9 08:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from fastapi import APIRouter, File, UploadFile, Query, Form, Response, Request

router = APIRouter()


@router.on_event("shutdown")
async def shutdown_event():
    # 执行清理操作，关闭事件循环 或者 通知
    await asyncio.get_event_loop().shutdown_asyncgens()
