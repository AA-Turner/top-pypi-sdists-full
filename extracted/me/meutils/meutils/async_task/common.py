#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2024/11/28 15:28
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.decorators.retry import retrying

from meutils.async_task import celery_config

from celery import Celery, Task, shared_task, states



worker = Celery()

worker.config_from_object(celery_config)

worker.conf.update(
    # result_expires=30 * 24 * 60 * 60,
    # enable_utc=False,
    # timezone='Asia/Shanghai',
    task_track_started=True,
)

if __name__ == '__main__':
    print(worker.conf.humanize(with_defaults=False))

    print(worker.conf.broker_url)
    print(worker.conf.result_backend)

    print(arun(get_task("59ddf636-3f27-4110-948e-5977c8cbe1b3")))
