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
        return billing_model

    elif model == "ideogram":
        billing_model = request.get("rendering_speed", "BALANCED").lower()
        return billing_model
