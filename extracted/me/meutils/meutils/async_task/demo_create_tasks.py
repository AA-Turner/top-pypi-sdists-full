#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2024/11/28 15:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from meutils.async_task.tasks import  hailuo


if __name__ == '__main__':
    request = hailuo.SoraVideoRequest()
    result = hailuo.create_task.send(request)
    print(result)
