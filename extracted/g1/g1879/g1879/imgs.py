# -*- coding:utf-8 -*-
# @Author    : g1879
# @date      : 2021/7/10
# @email     : g1879@qq.com
# @File      : files.py
"""
    处理图片的常用方法
    经测试，openCV缩小后图片质量比PIL好
    但openCV写起来比较麻烦
    注意：安装cv2语句是 pip install opencv-python
         安装PIL语句是 pip install pillow
"""
from pathlib import Path
from shutil import copy
from typing import List, Union

from PIL import Image
from cv2 import imencode, imdecode, resize, INTER_AREA
from numpy import fromfile, uint8

from .paths import get_usable_name, get_usable_path


def get_imgs_list(path: str, ignore: Union[str, tuple, list] = None) -> List[Path]:
    """获取所有图片，返回Path对象列表                  \n
    :param path: 文件夹绝对路径
    :param ignore: 忽略的图片格式，如['.jpg']
    :return: 图片绝对路径列表
    """
    if isinstance(ignore, str):
        ignore = (ignore,)

    ignore = ignore or ()
    ignore = set(map(lambda x: x.lower() if x.startswith('.') else f'.{x}'.lower(), ignore))
    formats = {'.jpg', '.png', '.bmp', '.jpeg', '.gif'} - ignore

    return [x for x in Path(path).iterdir() if x.suffix.lower() in formats]


def img_to_jpg(path: str, del_src: bool = True) -> None:
    """将一个图片转为jpg格式                  \n
    :param path: 图片路径
    :param del_src: 是否删除原图片
    :return: None
    """
    img_file = Path(path)

    if img_file.suffix.lower() == '.jpg':
        return

    folder = img_file.parent
    base_name = get_usable_name(str(folder), f'{img_file.stem}.jpg')
    base_name = Path(base_name).stem

    img = Image.open(path)
    img = img.convert('RGB')
    img.save(f'{folder}\\{base_name}.jpg')

    # 删除不是jpg的图片
    if del_src:
        img_file.unlink()


def imgs_to_jpg(path: str, del_src: bool = True) -> None:
    """将传入路径中的所有图片转为jpg                  \n
    :param path: 存放图片的文件夹路径
    :param del_src: 是否删除原图片
    :return: None
    """
    imgs = get_imgs_list(path, ('.jpg',))

    # 执行转换
    for img_path in imgs:
        img_to_jpg(str(img_path), del_src)


def find_min_x(path: Union[Path, str]) -> int:
    """返回路径中最小宽度图片的宽度"""
    return min(tuple(Image.open(x).size[0] for x in get_imgs_list(path)))


def zoom_img(path: Union[Path, str],
             x: int = None,
             y: int = None,
             to_path: str = None,
             rename: str = None) -> Path:
    """按照传入的xy值修改图片大小，如只传入一个值，保持图片比例缩放。可指定保存路径和文件名。  \n
    注意：指定文件名时会覆盖同名文件，否则会自动避免重名。                                 \n
    :param path: 图片路径
    :param x: 压缩后的宽度
    :param y: 压缩后的高度
    :param to_path: 压缩后保存路径，不传入时替换源文件
    :param rename: 保存的文件名。指定文件名时会覆盖同名文件，不指定时会自动重命名。
    :return: 压缩后的路径
    """
    path = Path(path)
    ext = path.suffix
    if to_path:
        Path(to_path).mkdir(parents=True, exist_ok=True)
        new_path = Path(f'{to_path}\\{rename}{ext}') if rename else get_usable_path(f'{to_path}\\{path.name}')
    else:
        new_path = path if not rename else path.parent / f'{rename}{ext}'

    # 读取图片，用这种方式读取才支持中文路径
    img = imdecode(fromfile(path, dtype=uint8), -1)
    old_y, old_x = img.shape[:2]

    # 根据传入的值生成新xy值
    xy = _get_zoom_xy(old_x, old_y, x, y)

    if xy:
        img = resize(img, xy, interpolation=INTER_AREA)
        imencode(ext, img)[1].tofile(new_path)  # 用这种方式保存使中文路径生效
    elif to_path or rename:
        copy(path, new_path)

    return new_path


def crop_img(path: Union[str, Path],
             x: int = None,
             y: int = None,
             to_path: str = None,
             rename: str = None) -> Path:
    """按目标值保持内容比例缩放图片，裁剪超出的部分。如只传入一个值，固定另一个值做裁剪。可指定保存路径和文件名。   \n
    注意：指定文件名时会覆盖同名文件，否则会自动避免重名。                                                  \n
    :param path: 图片路径
    :param x: 裁剪后的宽度
    :param y: 裁剪后的高度
    :param to_path: 裁剪后保存路径，不传入时替换源文件
    :param rename: 保存的文件名。指定文件名时会覆盖同名文件，不指定时会自动重命名。
    :return: 裁剪后的路径
    """
    path = Path(path)
    ext = path.suffix
    if to_path:
        Path(to_path).mkdir(parents=True, exist_ok=True)
        new_path = Path(f'{to_path}\\{rename}{ext}') if rename else get_usable_path(f'{to_path}\\{path.name}')
    else:
        new_path = path if not rename else path.parent / f'{rename}{ext}'

    # 读取图像文件，获取原宽高值
    img = imdecode(fromfile(path, dtype=uint8), -1)
    old_y, old_x = img.shape[:2]
    x = x or old_x
    y = y or old_y

    # 根据比例，缩小图片
    if old_x != x or old_y != y:
        diff = old_x / old_y - x / y
        if diff < 0:
            xy = _get_zoom_xy(old_x, old_y, x=x)
        elif diff > 0:
            xy = _get_zoom_xy(old_x, old_y, y=y)
        elif x > old_x:  # 等比放大图片
            xy = x, y
        else:  # 等比裁剪图片
            xy = False

        # 如果比例有变化，或等比放大，先按长边缩放图片
        if xy:
            old_x, old_y = xy
            img = resize(img, xy, interpolation=INTER_AREA)

        # 根据比例，裁剪图片
        if old_x / old_y <= x / y:
            upper = (old_y - y) // 2
            img = img[upper:upper + y, 0:x]  # 裁剪坐标为[y0:y1, x0:x1]
        else:
            left = (old_x - x) // 2
            img = img[0:y, left:left + x]  # 裁剪坐标为[y0:y1, x0:x1]

        # 保存图片
        imencode(ext, img)[1].tofile(new_path)

    elif to_path or rename:
        copy(path, new_path)

    else:
        new_path = path

    return new_path


def _get_zoom_xy(old_x, old_y, x=None, y=None) -> Union[bool, tuple]:
    """计算缩放图像后的xy值                  \n
    :param old_x: 图像原宽度
    :param old_y: 图像原高度
    :param x: 目标宽度
    :param y: 目标高度
    :return: False或xy值组成的元组
    """
    if (not x and not y) or (x == old_x and y == old_y):
        return False

    if x and not y:
        if old_x == x:
            return False
        else:
            y = int(old_y * x / old_x)
    elif y and not x:
        if old_y == y:
            return False
        else:
            x = int(old_x * y / old_y)

    return x, y
