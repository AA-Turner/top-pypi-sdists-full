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

"""
        "message": "{\"error\":{\"code\":\"\",\"message\":\"所有令牌分组 default 下对于模型 fal-minimax-voice-clone_minimax-_6s_720p 均无可用渠道，请更换分组尝试 (request id: 20250913110021793629462u1r59kQ8)\",\"type\":\"rix_api_error\"}}",

"""


def make_billing_model(model: str, request: dict):
    """

    :param model: biz model
    :param request:
    :return:
    """
    _model = model.removeprefix("fal-").lower()
    if _model.startswith(("pika", "fal-pika")):
        duration = request.get("duration")
        resolution = request.get("resolution")

        billing_model = f"{duration}s_{resolution}"

        return f"{model}_{billing_model}"

    elif _model.startswith(("ideogram", "fal-ideogram")):
        billing_model = request.get("rendering_speed", "BALANCED").lower()

        return f"{model}_{billing_model}"

    elif _model.startswith(("minimax-speech", "minimax-voice")):  # 按量跳过
        return


    elif _model.startswith(("minimax")):
        # MiniMax-Hailuo-02 T2V-01-Director I2V-01-Director S2V-01 I2V-01-live I2V-01 T2V-01

        duration = request.get("duration", 6)
        resolution = request.get("resolution", "720P")
        model = request.get("model", "").lower()

        if "01" in model:
            duration = 6
            resolution = "720P"

        if model.startswith("minimax"):  # 02
            resolution = request.get("resolution", "768P")

        billing_model = f"""minimax-{model.removeprefix("minimax-")}_{duration}s_{resolution}"""

        return billing_model


if __name__ == '__main__':
    data = {
        # "model": "MiniMax-Hailuo-02",
        "model": "T2V-01-Director",
        "prompt": "男子拿起一本书[上升]，然后阅读[固定]。",
        # "duration": 6,
        # "resolution": "1080P"
    }

    data = {
        "model": "T2V-01",
        "prompt": "男子拿起一本书[上升]，然后阅读[固定]。",
        "duration": 6,
        # "resolution": "1080P"
    }

    data = {
        "text": "你正在用海螺语音，先克隆音乐，然后合成语音。",
        "voice_setting": {
            "speed": 1,
            "vol": 1,
            "voice_id": "Voice904740431752642196",
            "pitch": 0,
        },
        "output_format": "url"
    }

    print(make_billing_model("fal-minimax-speech", data))
