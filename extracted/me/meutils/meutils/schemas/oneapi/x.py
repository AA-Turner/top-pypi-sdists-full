#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2024/11/14 15:26
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


class VendorInfo(BaseModel):
    name: str
    desc: Optional[str] = None
    icon: Optional[str] = None
    notice: Optional[str] = None

    class Config:
        # 允许额外字段，增加灵活性
        extra = 'allow'


if __name__ == '__main__':
    print(VendorInfo(name="1", xx="2"))
