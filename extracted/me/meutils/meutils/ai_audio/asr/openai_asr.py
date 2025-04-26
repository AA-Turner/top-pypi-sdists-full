#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_asr
# @Time         : 2023/11/23 13:10
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description
import io
import os

import requests
from meutils.io.files_utils import to_file

from meutils.pipe import *
from openai import OpenAI

# response_format: Literal["json", "text", "srt", "verbose_json", "vtt"]
file = open(
    "f275d9ac-5a62-4bbe-baf9-3fa10e0332f4.mp3",
    'rb')  # 正确
# file=open("2022112519张健涛29.mp3", 'rb')
# file = httpx.get("https://oss.chatfire.cn/data/demo.mp3").content

client = OpenAI(
    # base_url="https://openai.chatfire.cn/v1",
    api_key=os.getenv("OPENAI_API_KEY") + "-336",
    # api_key=os.getenv("OPENAI_API_KEY_OPENAI") + "-336",

    # api_key=os.getenv("SILICONFLOW_API_KEY"),
    # base_url=os.getenv("SILICONFLOW_BASE_URL")

    # base_url="http://0.0.0.0:8000/v1",
    # base_url="https://api.chatfire.cc/v2",
    # base_url="https://api.chatfire.cc/v1",

    # api_key=os.getenv("DEEPINFRA_API_KEY"),
    # base_url="https://api.deepinfra.com/v1/openai",
)
# client = OpenAI(
#     api_key=os.environ.get("GROQ_API_KEY"),
#     # base_url=os.getenv("GROQ_BASE_URL"),
#     base_url="https://groq.chatfire.cc/v1",
#
# )
with timer():
    file = Path('audio.mp3').read_bytes()
    file = Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/x1.mp3").read_bytes()

    # file = Path('m4a.mp3')

    # file = Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/example.mp3").read_bytes()

    # file = Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/国外健身和生活设备市场观察及分析.mp3").read_bytes()

    # file = Path('audio.mp3').read_bytes()

    # file = arun(to_file(file))  # mp3后缀
    file = ('_.mp3', file)  # ok

    _ = client.audio.transcriptions.create(
        file=file,

        # model="whisper-1",
        # model="openai/whisper-large",

        # model="SenseVoiceSmall",
        model="FunAudioLLM/SenseVoiceSmall",

        # model="distil-whisper/distil-large-v3-ct2",

        # model="asr",

        # model="sensevoice",
        # model="whisper-large-v3",
        # response_format="text",  # ["json", "text", "srt", "verbose_json", "vtt"]
        # response_format="srt",  # ["json", "text", "srt", "verbose_json", "vtt"]
        # response_format="verbose_json",  # ["json", "text", "srt", "verbose_json", "vtt"]
        # response_format="vtt",  # ["json", "text", "srt", "verbose_json", "vtt"]

    )
    print(_)
    #
    # _ = client.audio.translations.create(
    #     file=file,
    #     # model="whisper-1",
    #     model="whisper-large-v3",
    #     # response_format="text",  # ["json", "text", "srt", "verbose_json", "vtt"]
    #     # response_format="srt",  # ["json", "text", "srt", "verbose_json", "vtt"]
    #     # response_format="verbose_json",  # ["json", "text", "srt", "verbose_json", "vtt"]
    #     # response_format="vtt",  # ["json", "text", "srt", "verbose_json", "vtt"]
    #
    # )
    # print(_)

# Transcription(text='健身需要注意适度和平衡 过度的锻炼可能会导致身体受伤 因此 进行健身活动前 最好先咨询医生 或专业的健身教练 制定一个适合自己的健身计划 一般来说 一周内进行150分钟的适度强度的有氧运动 或者75分钟的高强度有氧运动 加上每周两天的肌肉锻炼就能达到保持健康的目标')

