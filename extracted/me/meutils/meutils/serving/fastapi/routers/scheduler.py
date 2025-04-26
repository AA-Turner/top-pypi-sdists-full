#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : scheduler
# @Time         : 2024/1/9 08:51
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from fastapi import status
from fastapi import APIRouter, File, UploadFile, Query, Form, Response, Request
from apscheduler.schedulers.asyncio import AsyncIOScheduler as Scheduler

router = APIRouter()

scheduler = Scheduler(timezone="Asia/Shanghai")


@router.on_event("startup")
async def start_scheduler():
    """scheduler.add_job(do_job, 'interval', seconds=3)
    - 结合playwright定时刷新cookies
    """
    # scheduler.add_job(do_job, **trigger_args)  # 注入任务

    scheduler.start()

# @router.on_event("startup")
# async def start_scheduler():
#     from meutils.decorators.schedulers import scheduled_job
#
#     @scheduled_job(trigger_kwargs={'seconds': 5})
#     def tick():
#         print(f"########TASK: {time.ctime()}")
#
#     tick()


# @router.on_event("startup")
# async def start_scheduler():
#     def tick():
#         print(time.ctime())
#     from apscheduler.schedulers.asyncio import AsyncIOScheduler as Scheduler
#     from apscheduler.schedulers.background import BackgroundScheduler as Scheduler
#
#     scheduler = Scheduler(timezone="Asia/Shanghai")
#     scheduler.add_job(tick, 'interval', seconds=3)
#     scheduler.start()


# from meutils.pipe import *
# from meutils.serving.fastapi import App
# from meutils.serving.fastapi.routers import scheduler
#
# if __name__ == '__main__':
#     app = App()
#     scheduler.scheduler.add_job(lambda: print("hello"), 'interval', seconds=3)
#
#     app.include_router(scheduler.router)
#     app.run(port=8899)