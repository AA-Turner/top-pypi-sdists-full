#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : scenedetect_demo
# @Time         : 2023/11/17 16:07
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

import scenedetect
from scenedetect.scene_manager import SceneManager, save_images as _save_images
from scenedetect.scene_manager import write_scene_list as _write_scene_list
from scenedetect.scene_manager import write_scene_list_html as _write_scene_list_html

from scenedetect.stats_manager import StatsManager
from scenedetect.detectors.content_detector import ContentDetector, SceneDetector

import pysrt
from pysrt.srttime import SubRipTime


class SceneDetect(object):

    def __init__(self, video_path, detector: Optional[SceneDetector] = None):
        self.videostream = scenedetect.open_video(video_path)
        self.scene_manager = SceneManager()
        self.scene_manager.add_detector(detector or ContentDetector())
        self.scene_manager.detect_scenes(self.videostream, show_progress=True)

    def save_images(
            self,
            num_images=1,
            image_name_template: str = '$VIDEO_NAME-Scene-$SCENE_NUMBER-$IMAGE_NUMBER',
            output_dir: Optional[str] = None,
            show_progress: Optional[bool] = True,
            **kwargs
    ):
        kwargs['num_images'] = num_images
        kwargs['image_name_template'] = image_name_template
        kwargs['output_dir'] = output_dir
        kwargs['show_progress'] = show_progress

        image_filenames = _save_images(self.scene_list, self.videostream, **kwargs)

        return image_filenames

    def to_srt(self, texts: Optional[List[str]] = None, filename="example.srt"):
        """
            text为空会临时放入time_delta
        :param texts:
        :param filename:
        :return:
        """
        # 创建一个 SubRipFile 实例
        texts = texts or [""] * len(self.scene_list)

        subs = pysrt.SubRipFile()
        for index, ((scene_s, scene_e), text) in enumerate(zip(self.scene_list, texts)):
            time_delta = scene_e.get_seconds() - scene_s.get_seconds()
            text = text or int(time_delta * 1000)
            start = SubRipTime(*re.split('[:.]', scene_s.get_timecode()) | xmap(float))
            end = SubRipTime(*re.split('[:.]', scene_e.get_timecode()) | xmap(float))
            # 创建一个新的字幕项
            sub = pysrt.SubRipItem(index=index, start=start, end=end, text=text)
            # position 属性允许你指定字幕在视频画面中的位置。这个属性是一个元组，包含两个整数值，可以临时放一下时长
            subs.append(sub)
        # 保存字幕文件
        subs.save(filename, encoding='utf-8')

    @cached_property
    def scene_list(self):
        return self.scene_manager.get_scene_list()

    def write_scene_list_html(self, output_html_filename, **kwargs):
        _write_scene_list_html(output_html_filename, self.scene_list, **kwargs)

    def write_scene_list(self, output_csv_filename, **kwargs):
        with open(output_csv_filename, 'w') as f:
            _write_scene_list(f, self.scene_list, **kwargs)


if __name__ == '__main__':
    p = "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_video/312_1700705412.mp4"

    s = SceneDetect(p)
    # image_filenames = s.save_images(output_dir='xx')
    # print(image_filenames)
    # print(s.scene_list)
