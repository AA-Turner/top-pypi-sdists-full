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




"doubao-seedance-1-5-pro_5s_480p"

# "doubao-seedance-1-5-pro_10s_480p": 0.9,
# "doubao-seedance-1-5-pro_10s_720p": 1.5,
# "doubao-seedance-1-5-pro_10s_1080p": 3,

models = {}
for i in range(4, 13, 1):
    m = f"doubao-seedance-1-5-pro_{i}s_480p"
    m = f"doubao-seedance-1-5-pro_{i}s_720p"
    m = f"doubao-seedance-1-5-pro_{i}s_1080p"

    # models[m] = 0.9 * (i / 10)
    # models[m] = 1.5 * (i / 10)
    models[m] = 3 * (i / 10)



if __name__ == '__main__':
    data = models
    data = dict(zip(data, np.ceil(1000 * np.array(list(data.values()))) / 1000))




