#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : asr
# @Time         : 2023/11/21 13:57
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


import whisper
from datetime import timedelta

def transcribe_audio(audio_path, model='base', language='zh'):
    model = whisper.load_model(model, download_root="/Users/betterme/PycharmProjects/AI/pyvideotrans/models")  # Change this to your desired model
    print(f"Whisper model loaded.{language},{audio_path=}")
    transcribe = model.transcribe(audio_path, language=language)
    segments = transcribe['segments']
    print(f"{segments=}")
    result = ""
    for segment in segments:
        print(segment)
        startTime = str(0) + str(timedelta(seconds=int(segment['start']))) + ',000'
        endTime = str(0) + str(timedelta(seconds=int(segment['end']))) + ',000'
        text = segment['text']
        segmentId = segment['id'] + 1
        result += f"{segmentId}\n{startTime} --> {endTime}\n{text.strip()}\n\n"
    return result


if __name__ == '__main__':
    audio_path = "../../../zh_.wav"
    print(transcribe_audio(audio_path=audio_path))