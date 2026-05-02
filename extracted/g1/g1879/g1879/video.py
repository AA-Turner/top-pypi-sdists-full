# -*- coding:utf-8 -*-
from pathlib import Path

from cv2 import VideoCapture, imencode, CAP_PROP_POS_MSEC

from .imgs import crop_img


def video_screen(video_path: str,
                 save_path: str = None,
                 img_name: str = None,
                 second: float = 1,
                 x: int = None, y: int = None) -> bool:
    """截取视频某一时间的截图，可调整图片大小                  \n
    :param video_path: 视频的路径
    :param save_path: 图片保存的路径
    :param img_name: 图片文件名，无须后缀，自动保存为jpg
    :param second: 截取第几秒的图像
    :param x: 所保存图片的宽度
    :param y: 所保存图片的高度
    :return:是否截图成功
    """
    if not img_name:
        img_name = Path(video_path).stem
    if not save_path:
        save_path = Path(video_path).parent
    if not img_name.lower().endswith('.jpg'):
        img_name = f'{img_name}.jpg'

    vc = VideoCapture(video_path)  # 读取视频
    vc.set(CAP_PROP_POS_MSEC, second * 1000)  # 设置读取位置
    rval, frame = vc.read()  # 读取当前帧，rval用于判断读取是否成功

    if rval:
        img_path = f'{save_path}\\{img_name}'
        imencode('.jpg', frame)[1].tofile(img_path)

        # 调整图片大小，保持内容比例
        if x or y:
            crop_img(img_path, x, y)

        return True
    else:
        return False
