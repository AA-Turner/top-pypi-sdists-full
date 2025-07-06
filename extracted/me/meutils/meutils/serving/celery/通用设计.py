#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 通用设计
# @Time         : 2024/11/25 18:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/GregaVrbancic/fastapi-celery/blob/master/app/main.py#L31

from meutils.pipe import *
from typing import Any, Dict, Optional
from celery.result import AsyncResult

from fastapi import FastAPI, APIRouter, Request, HTTPException
from enum import Enum
from pydantic import BaseModel


# 1. 定义标准响应模型
class TaskStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"


class TaskResponse(BaseModel):
    code: int
    message: str
    task_id: str
    status: TaskStatus
    data: Optional[Any] = None


# 2. 定义任务管理器
class TaskManager:
    @staticmethod
    async def create_task(task_func, **kwargs) -> TaskResponse:
        try:
            task = task_func.delay(**kwargs)
            return TaskResponse(
                code=0,
                message="Task created successfully",
                task_id=task.id,
                status=TaskStatus.PENDING
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_task_result(task_id: str) -> TaskResponse:
        result = AsyncResult(id=task_id)

        if result.ready():
            if result.successful():
                return TaskResponse(
                    code=0,
                    message="Task completed successfully",
                    task_id=task_id,
                    status=TaskStatus.SUCCESS,
                    data=result.get()
                )
            else:
                return TaskResponse(
                    code=1,
                    message=str(result.result),
                    task_id=task_id,
                    status=TaskStatus.FAILURE
                )
        else:
            return TaskResponse(
                code=0,
                message="Task is still running",
                task_id=task_id,
                status=TaskStatus.RUNNING
            )


# 3. 路由实现
router = APIRouter(prefix="/celery")


@router.get("/{task_id}", response_model=TaskResponse)
async def get_result(task_id: str):
    return await TaskManager.get_task_result(task_id)


@router.post("/task", response_model=TaskResponse)
async def create_task(request: Request):
    try:
        kwargs = await request.json()
        return await TaskManager.create_task(proxy_task, **kwargs)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 4. 错误处理装饰器
def handle_task_errors(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return TaskResponse(
                code=1,
                message=str(e),
                task_id="",
                status=TaskStatus.FAILURE
            )

    return wrapper


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()
    app.include_router(router)
    app.run(port=8899)
