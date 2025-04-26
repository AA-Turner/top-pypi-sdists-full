#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : audio
# @Time         : 2025/3/23 16:07
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from dashscope.audio.asr import Transcription

file_urls = [
    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
]
language_hints = ["zh", "en"]

data = {
    "model": "paraformer-v2",
    "input": {"file_urls": file_urls},
    "parameters": {
        "channel_id": [0],
        "language_hints": language_hints,
        "vocabulary_id": "vocab-Xxxx",
    },
}

task_response = Transcription().async_call(
    model="paraformer-v2",
    file_urls=file_urls,
    language_hints=language_hints,
)

response = Transcription().wait(task_response)  # .output.results
