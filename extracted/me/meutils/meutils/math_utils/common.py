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
    if 'x' in size:
        w, h = size.split('x')
        w, h = calculate_min_resolution(w, h)
        return f"{w}:{h}"  # aspect_ratio

    elif ':' in size:
        return size


if __name__ == '__main__':
    print(size2aspect_ratio("1920x1080"))
    print(size2aspect_ratio("1920:1080"))
    print(size2aspect_ratio("1024x1024"))
