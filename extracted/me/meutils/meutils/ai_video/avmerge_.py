#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : avmerge_
# @Time         : 2023/11/20 17:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

audio_path = "/Users/betterme/Downloads/videoplayback.m4a"
# audio_path = "audio.mp3"
video_path = "/Users/betterme/Downloads/videoplayback.mp4"


def merge_audio_video(audio_file, video_file, output_file):
    command = f'ffmpeg -i {audio_file} -i {video_file} -c:v copy -c:a aac -strict experimental {output_file}'
    subprocess.call(command, shell=True)


# 调用函数进行音频和视频合并
merge_audio_video(audio_path, video_path, "output.mp4")

#
# !ffmpeg -i /Users/betterme/Downloads/videoplayback.mp4 \
# -i audio_merged.wav \
# -vf "subtitles=new.srt" \
# -c:v libx264 -c:a aac \
# output.mp4
