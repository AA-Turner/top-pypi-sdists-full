#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/11/29 16:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 通用异步设计，兼容oneapi监控

from celery.result import AsyncResult

from meutils.pipe import *
from meutils.schemas.task_types import TaskResponse

from meutils.db.orm import update_or_insert
from meutils.schemas.db.oneapi_types import OneapiTask

from meutils.db.redis_db import redis_aclient

from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request, HTTPException, status, BackgroundTasks


async def create_task(async_task, request: Union[BaseModel, dict]):
    if not isinstance(request, dict):
        request = request.model_dump()

    result = async_task.apply_async(kwargs={"request": request})
    task_id = result.id

    return TaskResponse(task_id=task_id, request_id=task_id)


# {
#   "code": 0,
#   "message": "SUCCEED",
#   "request_id": "CjMkWmdJhuIAAAAAAAS0mA",
#   "data": {
#     "task_id": "CjMkWmdJhuIAAAAAAAS0mA",
#     "task_status": "submitted",
#     "created_at": 1732881630997,
#     "updated_at": 1732881630997
#   }
# }


async def get_task(
        task_id: str,
        remote_get_task: Optional[Callable] = None,
        filter_kwargs: Optional[dict] = None,
        background_tasks: Optional[BackgroundTasks] = None,
):
    """

    :param task_id:
    :param remote_get_task:
    :param filter_kwargs: #######参数可以舍弃
         filter_kwargs = {
            "task_id": task_id, #########理论上只需这个
            "user_id": user_id,
            "platform": "replicate",
            "action": "replicate",  # 模型
        }
    :return:
    """
    filter_kwargs = filter_kwargs or {}
    filter_kwargs["task_id"] = task_id

    result = AsyncResult(id=task_id)
    logger.debug(bjson(result._get_task_meta()))
    # logger.debug(bjson(result.get(timeout=30)))
    logger.debug(result)
    logger.debug(result.ready())
    logger.debug(result.state)

    # if result.status=="PENDING": # worker可能还未启动，会阻塞
    # if await redis_aclient.select(1) and not await redis_aclient.exists(f"celery-task-meta-{task_id}"):
    #     raise HTTPException(status_code=404, detail="TaskID not found")

    if result.ready():
        if result.successful():
            data = result.get(timeout=30).copy()  # 创建任务时：remote task的返回结果 ####### copy避免丢失字段
            logger.debug(bjson(data))
            token = data.pop("system_fingerprint", None)  # 远程任务 token/apikey

            remote_task_id = (
                    data.get("task_id")  # 提前写
                    or data.get("data", {}).get("task_id")
                    or data.get("data", {}).get("id")
                    or data.get("id")
                    or data.get("request_id")
            )

            response = TaskResponse(
                task_id=task_id,

                message="Task completed successfully",
                status=result.status,
                data=data
            )

            if remote_get_task:
                if inspect.iscoroutinefunction(remote_get_task):
                    remote_task_response = await remote_get_task(remote_task_id, token)
                else:
                    remote_task_response = remote_get_task(remote_task_id, token)

                if not isinstance(remote_task_response, dict):
                    remote_task_response = remote_task_response.model_dump()

                # logger.debug(response.model_dump_json(indent=4))
                # logger.debug(bjson(remote_task_response))

                _response = {**response.model_dump(), **remote_task_response}
                response = response.construct(**_response)

                # logger.debug(response.model_dump_json(indent=4))

        else:
            response = TaskResponse(
                task_id=task_id,

                code=1,
                message=str(result.result),
                status=result.status,
            )
    else:
        response = TaskResponse(
            task_id=task_id,

            message="Task is still running",
            status=result.status,
        )

    # 更新到数据库：异步任务
    update_fn = partial(update_oneapi_from_response, task_response=response)
    if background_tasks:
        background_tasks.add_task(update_or_insert, OneapiTask, filter_kwargs, update_fn)
    else:
        await update_or_insert(OneapiTask, filter_kwargs, update_fn)

    return response


# todo: 可以设计更通用的
async def update_oneapi_from_response(task: OneapiTask, task_response: TaskResponse):
    """

    filter_kwargs = {
            "task_id": task_id,
            "user_id": user_id,
            "platform": "replicate",
            "action": "replicate",  # 模型
        }

    需要获取这几个信息 user_id

    """
    # if task.status in {"SUCCESS", "FAILURE"}: return False  # 跳出轮询，不再更新

    task.data = task_response.model_dump(exclude={"system_fingerprint"})
    task.status = task_response.status
    task.progress = time.time() // 10 % 100

    if task.status == "SUCCESS":  ###### todo: 状态对齐
        task.progress = "100%"
    elif task.status == "FAILURE":
        task.fail_reason = "查看详情"

    task.updated_at = int(time.time())
    task.finish_time = int(time.time())  # 不是实际时间


if __name__ == '__main__':
    from meutils.async_task import worker, shared_task  #######重要 需要识别到worker

    from meutils.apis.kling import kolors_virtual_try_on
    from meutils.async_task.tasks import hailuo

    task_id = "7d4fbaf3-f641-482b-b02c-ccd30e61195a"
    # filter_kwargs = {
    #     "task_id": task_id,  #########理论上只需这个
    #     "user_id": 1,
    #     "platform": "kling",
    #     "action": "kling",  # 模型
    # }

    # arun(get_task(task_id, hailuo.get_task))
    #
    # task_id = "e3f76be8-f7eb-4562-a7af-029928d074d5"
    # arun(get_task(task_id, kolors_virtual_try_on.get_task))
