#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : xx
# @Time         : 2023/11/17 16:12
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import os
from datetime import timedelta
from scenedetect.scene_manager import SceneManager


# 将时间戳转换为字符串格式
def timestamp_to_string(timestamp):
    return str(timedelta(seconds=timestamp))


# 获取场景列表
scene_list = SceneManager.get_scene_list('scene_list.csv')

# 遍历输出的图像文件并重命名
for i, filename in enumerate(os.listdir('.')):
    if filename.startswith('scene') and filename.endswith('.png'):
        timestamp = scene_list[i].get_timecode().get_seconds()
        new_filename = timestamp_to_string(timestamp).replace(':', '-') + '.png'
        os.rename(filename, new_filename)
