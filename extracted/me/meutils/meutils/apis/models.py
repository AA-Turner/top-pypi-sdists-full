#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : models
# @Time         : 2025/7/14 16:47
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


def create_fal_models(model: str, request: dict):
    if model == "pika":
        duration = request.get("duration")
        resolution = request.get("resolution")

        billing_model = f"{duration}s_{resolution}"
    else:
        duration = request.get("duration", "5")
        resolution = request.get("resolution", "720p")

        billing_model = f"_{duration}s_{resolution}"
    return billing_model
