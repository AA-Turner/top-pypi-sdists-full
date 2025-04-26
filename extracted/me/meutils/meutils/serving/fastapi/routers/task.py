#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : task
# @Time         : 2024/5/9 15:41
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.db.redis_db import redis_aclient
from fastapi import status
from fastapi import APIRouter, File, UploadFile, Query, Form, Response, Request, FastAPI
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/redis/{task_id}")
@alru_cache(ttl=60)  # 缓存
async def get_task_from_redis(task_id: str):
    task_info = await redis_aclient.get(task_id)
    return task_info


class RedisRequest(BaseModel):
    task_id: str
    task_info: str
    ttl: Optional[int] = None


@router.post("/redis")
async def set_task_for_redis(requst: RedisRequest):
    await redis_aclient.set(requst.task_id, requst.task_info, ex=requst.ttl)
    # return JSONResponse(content="", status_code=status.HTTP_200_OK)



redis_aclient.response_callbacks


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()
    app.include_router(router)
    app.run()
