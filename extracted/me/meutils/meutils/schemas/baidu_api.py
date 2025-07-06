#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : baidu_api
# @Time         : 2023/8/25 11:15
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


class Location(BaseModel):
    top: int
    left: int
    width: int
    height: int


class OCRElement(BaseModel):
    words: str
    location: Location


class OCResult(BaseModel):
    element: List[OCRElement]
