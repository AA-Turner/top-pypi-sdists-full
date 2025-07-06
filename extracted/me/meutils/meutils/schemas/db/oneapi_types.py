#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : models
# @Time         : 2024/11/20 10:57
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from sqlalchemy import JSON
from sqlmodel import Field, Session, SQLModel, create_engine, select, insert, update, Column, DateTime, func


def get_default_name():
    return "xx"


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default_factory=lambda: "test")
    secret_name: str = ""
    age: Optional[int] = None
    # created_at: datetime.datetime = Field(
    #     default_factory=datetime.datetime.utcnow,
    # )
    updated_at: Optional[datetime.datetime] = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )


class OneapiTask(SQLModel, table=True):
    """https://github.com/Calcium-Ion/new-api/blob/main/model/task.go"""

    __tablename__ = "tasks"  # 自定义表名

    id: Optional[int] = Field(default=None, primary_key=True)

    task_id: Optional[str] = Field(default=None, max_length=50)
    remote_task_id: Optional[str] = Field(default=None, max_length=50)
    user_id: Optional[int] = Field(default=None)
    channel_id: Optional[int] = Field(default=None)

    data: Optional[dict] = Field(default=None, sa_type=JSON)

    """TaskStatus
    TaskStatusNotStart              = "NOT_START"
    TaskStatusSubmitted             = "SUBMITTED"
    TaskStatusQueued                = "QUEUED"
    TaskStatusInProgress            = "IN_PROGRESS"
    TaskStatusFailure               = "FAILURE"  # todo: 补偿积分+状态记录
    TaskStatusSuccess               = "SUCCESS"
    TaskStatusUnknown               = "UNKNOWN
    """
    status: Optional[str] = Field(default="SUBMITTED", max_length=20)

    progress: str = Field(default="0%", max_length=20)
    fail_reason: Optional[str] = Field(default=None)

    platform: Optional[str] = Field(default="🔥", max_length=30)
    action: Optional[str] = Field(default=None, max_length=40)  # black-forest-labs/flux-schnell

    """价格 50000=0.1 """
    quota: Optional[int] = Field(default=None)  #
    properties: Optional[dict] = Field(default=None, sa_type=JSON)

    submit_time: Optional[int] = Field(default_factory=lambda: int(time.time()))
    start_time: Optional[int] = Field(default_factory=lambda: int(time.time()))
    finish_time: Optional[int] = Field(default_factory=lambda: int(time.time()))

    created_at: Optional[int] = Field(default_factory=lambda: int(time.time()))
    updated_at: Optional[int] = Field(default_factory=lambda: int(time.time()))

    class Config:
        arbitrary_types_allowed = True


class OneapiUser(SQLModel, table=True):
    __tablename__ = "users"  # 自定义表名

    id: Optional[int] = Field(default=None, primary_key=True)
    username: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)

    quota: Optional[int] = Field(default=None)
    used_quota: Optional[int] = Field(default=None)

    request_count: Optional[int] = Field(default=None)

    access_token: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default="")

    class Config:
        arbitrary_types_allowed = True


class OneapiToken(SQLModel, table=True):
    __tablename__ = "tokens"  # 自定义表名

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None)
    key: Optional[str] = Field(default=None)

    used_quota: Optional[int] = Field(default=None)
    remain_quota: Optional[int] = Field(default=None)
    unlimited_quota: Optional[bool] = Field(default=False)

    class Config:
        arbitrary_types_allowed = True


if __name__ == '__main__':
    print(Hero())
    # print(Tasks())

    print(OneapiTask.__name__)
