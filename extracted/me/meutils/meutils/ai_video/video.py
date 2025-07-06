#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : video
# @Time         : 2020/8/31 4:26 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from moviepy.editor import *


# TODO: 抽帧去重
def video2image(video: str, top_duration=180):
    p = Path(video)
    p = p.parent / p.name.split('.', maxsplit=1)[0]
    p.mkdir(exist_ok=True)

    with VideoFileClip(video) as clip:
        duration = int(clip.duration)
        for i in tqdm(range(min(duration, top_duration))):
            clip_ = clip.subclip(i, i + 1)
            clip_.save_frame(p / f'{i}.png')


def _video2audio(path_pair, verbose=False, subclip=None, ffmpeg_params=["-f", "mp3"]):
    """
        clip = VideoFileClip('蛋清和蛋黄是这么分离的.720p').subclip(3, 7)

    """
    video_path, audio_path = path_pair

    with VideoFileClip(video_path) as clip:
        duration = int(clip.duration)
        if subclip:
            s, e = subclip[0], duration if subclip is None or duration < subclip[1] else subclip[1]
            # s, e = subclip[0], duration if subclip or duration < subclip[1] else subclip[1]

            clip = clip.subclip(s, e)

        clip.audio.write_audiofile(
            audio_path,  # video_path.replace('.mp4', '.wav')
            fps=None, nbytes=2, buffersize=2000,
            codec=None, bitrate=None, ffmpeg_params=ffmpeg_params,
            write_logfile=False, verbose=verbose, logger='bar' if verbose else None
        )


def video2audio(video_path, audio_path):
    with AudioFileClip(video_path) as clip:
        clip.write_audiofile(audio_path)


if __name__ == '__main__':
    video_path = "douyin.mp4"

    # video2image("/Users/betterme/Downloads/11月15日.mp4")
    # video2audio([video_path, "x.mp3"])

    print(video2audio('/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/asr/blibli.mp4', "x.mp3"))
