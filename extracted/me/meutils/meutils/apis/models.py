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


def make_billing_model(model: str, request: dict):
    _model = model.removeprefix("fal-")
    if _model.startswith(("pika", "fal-pika")):
        duration = request.get("duration")
        resolution = request.get("resolution")

        billing_model = f"{duration}s_{resolution}"

        return f"{model}_{billing_model}"

    elif _model.startswith(("ideogram", "fal-ideogram")):
        billing_model = request.get("rendering_speed", "BALANCED").lower()

        return f"{model}_{billing_model}"
