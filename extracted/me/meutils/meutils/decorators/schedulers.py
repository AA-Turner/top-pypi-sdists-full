#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : schedulers
# @Time         : 2023/8/22 15:28
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://zhuanlan.zhihu.com/p/491679794

"""https://blog.csdn.net/somezz/article/details/83104368"

        trigger='date': 一次性任务，即只执行一次任务。
            next_run_time (datetime|str) – 下一次任务执行时间
            timezone (datetime.tzinfo|str) – 时区

        trigger='interval': 循环任务，即按照时间间隔执行任务。
            seconds (int) – 秒
            minutes (int) – 分钟
            hours (int) – 小时
            days (int) – 日
            weeks (int) – 周
            start_date (datetime|str) – 启动开始时间
            end_date (datetime|str) – 最后结束时间
            timezone (datetime.tzinfo|str) – 时区

        trigger='cron': 定时任务，即在每个时间段执行任务。None为0
            second (int|str) – 秒 (0-59)
            minute (int|str) – 分钟 (0-59)
            hour (int|str) – 小时 (0-23)
            day_of_week (int|str) – 一周中的第几天 (0-6 or mon,tue,wed,thu,fri,sat,sun)
            day (int|str) – 日 (1-31)
            week (int|str) – 一年中的第几周 (1-53)
            month (int|str) – 月 (1-12)
            year (int|str) – 年(四位数)
            start_date (datetime|str) – 最早开始时间
            end_date (datetime|str) – 最晚结束时间
            timezone (datetime.tzinfo|str) – 时区

"""

from meutils.pipe import *
from meutils.decorators import decorator
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler


@decorator
def scheduled_job(
        func,
        trigger='interval',
        trigger_kwargs: Optional[Dict[str, Any]] = None,
        scheduler: Optional[BaseScheduler] = None,
        *args, **kwargs
):
    scheduler = scheduler or AsyncIOScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(
        func,
        args=args,
        kwargs=kwargs,
        trigger=trigger,
        **trigger_kwargs or {}
    )
    # callback = None
    # callback and scheduler.add_listener(callback)

    scheduler.start()
    return scheduler


if __name__ == '__main__':
    from meutils.notice.feishu import send_message

    d = {}


    @scheduled_job(trigger='interval', seconds=3)
    def task():
        d['t'] = time.ctime()
        send_message(d)


    task()
