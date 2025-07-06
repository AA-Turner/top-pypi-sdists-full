#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : _test
# @Time         : 2024/1/9 08:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.serving.fastapi import App
from meutils.serving.fastapi.routers import scheduler

if __name__ == '__main__':
    app = App()
    scheduler.scheduler.add_job(lambda: print("hello"), 'interval', seconds=3)

    app.include_router(scheduler.router)
    app.run(port=8899)
