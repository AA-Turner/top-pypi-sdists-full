#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : pixverse_type
# @Time         : 2024/7/24 13:11
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import time

from meutils.pipe import *

BASE_URL = "https://app-api.pixverse.ai/creative_platform"

EXAMPLES = [
    {
        "Prompt": "太空战机高速穿过一个巨大的科幻内部通道，冲出通道飞向太空，通道尽头可以看到外面是太空大战",
        "Model": "v1",
        "Credit": 0,
        "AspectRatio": "512x288",
        "Seed": 937033649,
        "ConfigName": "t2v_0.4.1",
        "PromptToDualClips": 1,
        "Style": "realistic",
        "AutoCharacterPrompt": 0,
        "RemoveWatermark": 0,
        "TaskCnt": 2,
        "Quality": "480p",
        "Width": 512,
        "Height": 288,
        "CreationType": 1
    },
    {
        "Img": 4857092,
        # "ImgUrl": "https://media.pixverse.ai/upload/3597df25-8161-4eea-99a4-502ac2b49227.png",
        "ImgUrl": "https://dgss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/res/r/image/2017-09-27/297f5edb1e984613083a2d3cc0c5bb36.png",
        "Model": "v2",
        "Credit": 0,
        "Seed": 1467863527,
        "ConfigName": "it2v_2.0.1",
        "Duration": 5,
        "AutoCharacterPrompt": 0,
        "RemoveWatermark": 0,
        "PromptToDualClips": 0,
        "Quality": "480p",
        "CreationType": 2,
        "Prompt": "开花过程"
    }
]


class PixverseRequest(BaseModel):
    Prompt: Optional[str] = None
    Img: int = Field(default_factory=lambda: int(time.time()))
    ImgUrl: Optional[str] = None
    CreationType: int = 1

    Model: str = 'v2'
    AspectRatio: str = '512x288'
    Quality: str = '1080p'

    ConfigName: str = "t2v_0.4.1"

    PromptToDualClips: int = 1
    Style: str = 'realistic'
    AutoCharacterPrompt: int = 0
    RemoveWatermark: int = 1
    TaskCnt: int = 2
    Width: int = 512
    Height: int = 288

    Duration: int = 8

    Credit: int = 0
    Seed: Optional[int] = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if self.ImgUrl:
            pass
            self.CreationType = 2
            self.ConfigName = "it2v_2.0.1"

    class Config:
        json_schema_extra = {
            "examples": EXAMPLES
        }
