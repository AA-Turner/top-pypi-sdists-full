#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2023/8/21 14:26
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

os.environ["EVN_FILE"] = "/Users/betterme/PycharmProjects/AI/aiapi/aiapi/core/dev.env"

from meutils.settings.base import BaseSetting


class TestSetting(BaseSetting):
    name: str = '初始化'


print(TestSetting())
