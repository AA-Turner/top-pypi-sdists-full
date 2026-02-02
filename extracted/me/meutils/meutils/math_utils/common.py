#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2025/6/10 09:11
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


import math


def calculate_min_resolution(w, h):
    """
    计算给定宽高比的最小像素公约数分辨率（宽高互质）

    参数:
        aspect_ratio (str): 宽高比字符串，例如"16:9"

    返回:
        tuple: (宽, 高) 的元组，整数类型
    """
    # 分割字符串并转换为整数
    w, h = map(int, (w, h))

    # 计算最大公约数
    gcd_val = math.gcd(w, h)

    # 化简为互质的整数比
    width = w // gcd_val
    height = h // gcd_val

    return width, height


def size2aspect_ratio(size):
    if not size:
        return "1:1"
    elif size == "1792x1024":
        return "16:9"
    elif size == "1024x1792":
        return "9:16"

    if 'x' in size:
        w, h = size.split('x')
        w, h = calculate_min_resolution(w, h)
        return f"{w}:{h}"  # aspect_ratio

    elif ':' in size:
        return size


def size2resolution(size) -> str:
    """
    把任意分辨率换算成最接近的 *p 格式。
    返回 '720p' / '1080p' / '1440p' / '2160p' / '4320p' / '?p'
    """

    w, h = map(int, size.split("x"))

    # 只需看高度；常见档位
    standards = (480, 512, 720, 1080, 1440, 2160, 4320)
    # 找到与 h 最接近的那个
    closest = min(standards, key=lambda x: abs(x - h))
    # 允许 10% 误差，否则认为非常规
    if abs(closest - h) / closest > 0.15:
        return f'{h}p'  # 非标准，直接返回原始高度
    return f'{closest}p'


if __name__ == '__main__':
    print(size2aspect_ratio("1920x1080"))
    print(size2aspect_ratio("1920:1080"))
    print(size2aspect_ratio("1024x1024"))
    print(size2aspect_ratio("16:9"))
    size = "1792x1024"
    size = "1280x720"
    print(size2aspect_ratio(size))

    # print(size2resolution("512x512"))
    # print(size2resolution("480x480"))
    # print(size2resolution("1674x1238"))
    # print(size2resolution("960x528"))
    # print(size2resolution("720x1280"))
