#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : routers
# @Time         : 2023/8/4 14:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from celery.result import AsyncResult

from fastapi import FastAPI, APIRouter
from fastapi import FastAPI, Form, Depends, File, UploadFile, Body, Request, BackgroundTasks

from meutils.pipe import *
from meutils.serving.celery.tasks import *

router = APIRouter()


@router.get("/celery/{task_id}")
async def get_result(task_id):
    result = AsyncResult(id=task_id)
    if result.ready():
        return result.get()  # task_id
    else:
        return {'code': 1, 'message': result.status, 'task_id': task_id}


@router.post("/celery/task")  # producer
async def create(request: Request):
    kwargs = await request.json()
    task = proxy_task.delay(**kwargs)
    return {'code': 1, 'message': '', 'task_id': task.id}


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()
    app.include_router(router)
    app.run(port=8899)
