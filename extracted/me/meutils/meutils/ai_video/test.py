#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : test
# @Time         : 2023/11/17 15:24
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

scene_prompt = """
You are an expert in understanding scene transitions based on visual features in a video. For the given sequence of images per timestamp, identify different scenes in the video. Generate audio description for each scene with time ranges.
Be sure to answer in Chinese.
""".strip()

audio_prompt = """
You are an expert at understanding audio descriptions of different scenes in a video. Can you leverage the information provided, including title, abstract, audio descriptions and generate full audio description of each scene with non overlapping time ranges. Keep as many scenes possible covering all time ranges. You may find character names in the title or abstract. Use character names wherever possible in the audio descriptions. Keep the audio description for each time range within one short sentence.
Be sure to answer in Chinese.
""".strip()

messages = [
    # {
    #     "role": "system",
    #     "content": [
    #         {"type": "text", "text": "What’s in this image?"},
    #     ]
    # },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": scene_prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    "detail": "auto"
                },
            },
        ],
    }
]
