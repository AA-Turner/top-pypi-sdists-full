#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2023/11/21 18:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from meutils.ai_audio.utils import to_audio

for p in Path('.').glob('*.mp3'):
    # to_audio(p, p.name.replace('mp3', 'pcm'), format="s16le", codec="pcm_s16le")
    to_audio(open("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/asr/2022112519张健涛29.mp3", 'wb'), p, format="mp3")

# from pydub import AudioSegment
#
# # 读取 MP3 文件
# audio = AudioSegment.from_file("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/asr/音频文件夹/20190101-section_2.mp3", format="mp3")
#
# # 将 MP3 文件转换为 PCM 格式
# pcm_data = audio.raw_data
#
# # 将 PCM 数据保存到文件
# with open("output.pcm", "wb") as f:
#     f.write(pcm_data)
