#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : asr
# @Time         : 2023/5/17 13:51
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : pip install meutils openai-whisper pysrt opencc opencc-python-reimplemented -U
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/miniconda/lib/python3.10/site-packages/nvidia/cudnn/lib

import pysrt
from datetime import timedelta

from meutils.pipe import *
from meutils.str_utils import chinese_convert

from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment

from whisper.normalizers import BasicTextNormalizer, EnglishTextNormalizer

class ASR(object):

    def __init__(self, model_size_or_path='base', local_files_only=True):
        self.model = WhisperModel(
            model_size_or_path=model_size_or_path,
            local_files_only=local_files_only,
        )

    def audio_to_srt(self, audio, filename='subtitle.srt', **transcribe_kwargs):
        segments = self.transcribe(audio, **transcribe_kwargs)
        self.to_srt(segments, filename)

    def transcribe(
            self,
            audio,
            language: Optional[str] = 'zh',
            task: str = "transcribe",
            **kwargs  # todo: 常用参数
    ):
        segments, self.info = self.model.transcribe(str(audio), language=language, task=task, )

        bn = BasicTextNormalizer()

        bar = tqdm(segments)
        for segment in bar:
            d = segment._asdict()
            d['text'] = bn(chinese_convert(segment.text))
            segment = Segment(**d)

            bar.set_description(segment.text)
            yield segment

    def to_srt(self, segments: Generator[Segment, Any, None], filename='subtitle.srt'):
        subs = pysrt.SubRipFile()

        for index, segment in enumerate(segments):  # todo: index 从0开始？
            subs.append(
                pysrt.SubRipItem(
                    index=index,
                    start=self.seconds_to_srt_time(segment.start),
                    end=self.seconds_to_srt_time(segment.end),
                    text=segment.text
                )
            )

            # if index > 2: break

        subs.save(filename, encoding='utf-8')

    @staticmethod
    @lru_cache
    def seconds_to_srt_time(seconds):
        """
            # 示例用法
            seconds = 350.00
            formatted_srt_time = format_seconds_to_srt_time(seconds)
            print(formatted_srt_time)
        :param seconds:
        :return:
        """
        # 使用 timedelta 类型创建时间间隔对象
        time_interval = timedelta(seconds=seconds)

        # 创建一个 SubRipTime 对象
        srt_time = pysrt.SubRipTime(
            hours=time_interval.seconds // 3600,
            minutes=(time_interval.seconds // 60) % 60,
            seconds=time_interval.seconds % 60,
            milliseconds=int(time_interval.microseconds / 1000)
        )

        return srt_time


if __name__ == '__main__':
    model_size = "small"
    # model_size = "large-v3"
    # model_size = "Systran/faster-distil-whisper-large-v3"
    asr = ASR(model_size_or_path=model_size, local_files_only=True)
    # audio_path = '../../../../zh_.wav'
    # audio_path = "/Users/betterme/Downloads/videoplayback.m4a"
    # audio_path = "20190101-section_2.mp3"
    # asr.audio_to_srt(audio_path)

    for p in Path('./').glob('*.mp3'):
        asr.audio_to_srt(
            p, f"./{p.parent.name}/{p.name.strip('.mp3')}.text",
        )
        break
