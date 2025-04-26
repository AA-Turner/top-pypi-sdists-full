#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : all_tasks
# @Time         : 2024/11/28 17:50
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


# 所有异步任务
from meutils.pipe import *
from meutils.async_task import worker

for p in get_resolve_path('.', __file__).glob('*'):

    if (not p.name.startswith('_')) and p.name.endswith('.py'):
        logger.debug(p)
        _ = try_import(f"meutils.async_task.tasks.{p.stem}")
