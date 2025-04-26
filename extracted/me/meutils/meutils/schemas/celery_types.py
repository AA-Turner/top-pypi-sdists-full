#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : celery_types
# @Time         : 2024/11/25 17:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from enum import Enum
from meutils.pipe import *


# 1. 定义标准响应模型
class TaskStatus(str, Enum):
    #: Task state is unknown (assumed pending since you know the id).
    PENDING = 'PENDING'
    #: Task was received by a worker (only used in events).
    RECEIVED = 'RECEIVED'
    #: Task was started by a worker (:setting:`task_track_started`).
    STARTED = 'STARTED'
    #: Task succeeded
    SUCCESS = 'SUCCESS'
    #: Task failed
    FAILURE = 'FAILURE'
    #: Task was revoked.
    REVOKED = 'REVOKED'
    #: Task was rejected (only used in events).
    REJECTED = 'REJECTED'
    #: Task is waiting for retry.
    RETRY = 'RETRY'
    IGNORED = 'IGNORED'


class TaskResponse(BaseModel):
    code: int
    message: str
    task_id: str = Field(default_factory=shortuuid.random)  # celery task_id
    status: TaskStatus = "PENDING"
    data: Optional[Any] = None  # 存放具体的Task结构

    created_at: str = Field(default_factory=lambda: datetime.datetime.today().isoformat())  # "2024-11-19T03:11:22.795Z"

    # 系统水印: 一般用来存轮询token ###### 不要暴露
    system_fingerprint: Optional[str] = None

    class Config:
        # 允许额外字段，增加灵活性
        extra = 'allow'

    # kling示例
    # code: int = 0
    # message: str = ""
    # request_id: str = ""
    #
    # data: Optional[Task] = None
    #
    # # 系统水印
    # system_fingerprint: Optional[str] = None


if __name__ == '__main__':
    print(TaskResponse(code=1, message='', data={'a': 1}))