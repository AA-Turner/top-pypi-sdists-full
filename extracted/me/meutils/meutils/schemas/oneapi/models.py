#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : models
# @Time         : 2024/11/18 13:35
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BAICHUAN = {
    'baichuan4-air': 0.49,

    'baichuan4-turbo': 7.5,
    'baichuan4': 50,
    'baichuan3-turbo': 6,
    'baichuan3-turbo-128k': 12,
    'baichuan2-turbo': 4,
}

if __name__ == '__main__':
    print(BAICHUAN | xjoin(','))


