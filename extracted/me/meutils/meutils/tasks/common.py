#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/11/8 13:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : rq worker --with-scheduler

from meutils.pipe import *
from meutils.decorators.retry import retrying


def do_task(**kwargs):
    time.sleep(3)
    return kwargs


@retrying
def request_task(**kwargs):
    method = kwargs.pop('method', '')
    url = kwargs.pop('url', '')

    response = requests.request(method, url, **kwargs)  # request(method, url, **kwargs)

    return response.json()
