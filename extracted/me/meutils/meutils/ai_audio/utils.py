#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2023/11/22 15:48
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

import pysrt
from pysrt.srttime import SubRipTime

from pydub import AudioSegment
from pydub.playback import play


# 合并
def merge_audio_silent(audio_file, duration=1000, exclude=True):
    p = Path(audio_file)
    old_dir = p.parent.name
    new_dir = (p.parent.parent / f"{old_dir}_new")
    new_dir.mkdir(exist_ok=True)
    filename = new_dir / p.name

    audio = AudioSegment.from_file(audio_file)
    if exclude:
        duration -= len(audio)  # 剔除本身的长度
    audio += AudioSegment.silent(duration=max(duration, 0))
    audio.export(filename)
    return filename


def merge_audios(audio_files, filename: Optional[str] = None):
    audio = sum(map(AudioSegment.from_file, audio_files))
    filename = filename or "audio_merged.wav"
    audio.export(filename)
    return filename


def to_audio(file, filename="example.wav", format='wav', **kwargs):
    AudioSegment.from_file(file).export(filename, format=format, **kwargs)


if __name__ == '__main__':
    file = "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/asr/shaoyinceo.m4a"
    file = "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/asr/audio-.mp3"
    file = "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/x1.wav"

    to_audio(file, filename="x1.mp3", format='mp3')

