#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : adjusted_audio1
# @Time         : 2023/11/21 18:07
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from pydub import AudioSegment


def adjust_duration(audio1, audio2):
    # 加载音频文件
    audio1 = AudioSegment.from_file(audio1)
    audio2 = AudioSegment.from_file(audio2)

    # 获取两个音频文件的时长
    duration1 = len(audio1)
    duration2 = len(audio2)

    # 计算速度比率
    speed_ratio = duration1 / duration2
    print(speed_ratio)

    # 调整第二个音频的速度
    adjusted_audio2 = audio2.speedup(playback_speed=speed_ratio)

    return audio1, adjusted_audio2


if __name__ == '__main__':
    from pydub.playback import play

    # play(AudioSegment.from_file('10.wav'))

    # todo: 减速在报错

    adjusted_audio1, adjusted_audio2 = adjust_duration('1.wav', '10.wav')
    # 可以播放调整后的音频文件
    play(adjusted_audio1)
    play(adjusted_audio2)
