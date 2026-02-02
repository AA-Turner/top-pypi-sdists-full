#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : avmerge
# @Time         : 2023/11/20 17:00
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://blog.51cto.com/u_16175450/6695076

from meutils.pipe import *
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

audio_path = "/Users/betterme/Downloads/videoplayback.m4a"
audio_path = "audio.mp3"
video_path = "/Users/betterme/Downloads/videoplayback.mp4"

# 打开视频和音频
video_clip = VideoFileClip(video_path)
audio_clip = AudioFileClip(audio_path)

# final_clip = concatenate_videoclips([video_clip1, video_clip2])

# 将视频剪辑与音频剪辑连接起来
video_clip.set_audio(audio_clip)


# 导出带有音频的最终视频
video_clip.write_videofile("avmerged3.mp4")


#
# FileNotFoundError: [Errno 2] No such file or directory:\
#     'ffmpeg -hide_banner -y -i "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_video/output.mp4" ' \
#     '-ac 1 "/Users/betterme/PycharmProjects/AI/pyvideotrans/tmp/output/output.wav"'


def extract_audio(video__path, audio_path):
    my_clip = AudioFileClip(video__path)
    my_clip.write_audiofile(audio_path)
    return my_clip