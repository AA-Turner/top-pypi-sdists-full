#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2024/11/1 16:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

d1 = {
    "type": "curated_styles",
    "image_types": [
        "any",
        "digital_illustration",
        "illustration_3d",
        "digital_illustration_seamless",
        "digital_illustration_pixel_art",
        "digital_illustration_3d",
        "digital_illustration_psychedelic",
        "digital_illustration_hand_drawn",
        "digital_illustration_grain",
        "digital_illustration_glow",
        "digital_illustration_80s",
        "digital_illustration_watercolor",
        "digital_illustration_voxel",
        "digital_illustration_infantile_sketch",
        "digital_illustration_2d_art_poster",
        "digital_illustration_kawaii",
        "digital_illustration_halloween_drawings",
        "digital_illustration_2d_art_poster_2",
        "digital_illustration_engraving_color",
        "digital_illustration_flat_air_art",
        "digital_illustration_hand_drawn_outline",
        "digital_illustration_handmade_3d",
        "digital_illustration_stickers_drawings"
    ],
    "transform_model": "recraftv3",
    "offset": 0,
    "limit": 30
}

d2 = {
    "type": "curated_styles",
    "image_types": [
        "realistic_image",
        "realistic_image_mockup",
        "realistic_image_b_and_w",
        "realistic_image_enterprise",
        "realistic_image_hard_flash",
        "realistic_image_hdr",
        "realistic_image_natural_light",
        "realistic_image_studio_portrait",
        "realistic_image_motion_blur"
    ],
    "transform_model": "recraftv3",
    "offset": 0,
    "limit": 30
}

d3 = {
    "type": "curated_styles",
    "image_types": [
        "any",
        "digital_illustration",
        "illustration_3d",
        "digital_illustration_seamless",
        "digital_illustration_pixel_art",
        "digital_illustration_3d",
        "digital_illustration_psychedelic",
        "digital_illustration_hand_drawn",
        "digital_illustration_grain",
        "digital_illustration_glow",
        "digital_illustration_80s",
        "digital_illustration_watercolor",
        "digital_illustration_voxel",
        "digital_illustration_infantile_sketch",
        "digital_illustration_2d_art_poster",
        "digital_illustration_kawaii",
        "digital_illustration_halloween_drawings",
        "digital_illustration_2d_art_poster_2",
        "digital_illustration_engraving_color",
        "digital_illustration_flat_air_art",
        "digital_illustration_hand_drawn_outline",
        "digital_illustration_handmade_3d",
        "digital_illustration_stickers_drawings"
    ],
    "transform_model": "recraftv3",
    "offset": 0,
    "limit": 30
}

d4 = {
    "type": "curated_styles",
    "image_types": [
        "vector_illustration",
        "vector_illustration_seamless",
        "vector_illustration_line_art",
        "vector_illustration_doodle_line_art",
        "vector_illustration_flat_2",
        "vector_illustration_70s",
        "vector_illustration_cartoon",
        "vector_illustration_kawaii",
        "vector_illustration_linocut",
        "vector_illustration_engraving",
        "vector_illustration_halloween_stickers",
        "vector_illustration_line_circuit"
    ],
    "transform_model": "recraftv3",
    "offset": 0,
    "limit": 30
}


# d1['image_types'] + d2['image_types']+ d3['image_types']+ d4['image_types']

def min_max_normalize(data, feature_range=(0, 1)):
    """
    最大最小归一化函数,保持数据比例不变

    参数:
    data: 输入数据,可以是列表或numpy数组
    feature_range: 目标范围元组,默认为(0,1)

    返回:
    归一化后的数据
    """
    import numpy as np

    data = np.asarray(data)
    min_val = np.min(data)
    max_val = np.max(data)

    # 防止除零
    if max_val == min_val:
        return np.zeros_like(data)

    min_range, max_range = feature_range
    range_scale = max_range - min_range
    data_scale = max_val - min_val

    # 保持比例的归一化
    scale_factor = range_scale / data_scale
    scaled_data = data * scale_factor + (min_range - min_val * scale_factor)

    return scaled_data

min_max_normalize([1000, 3000], feature_range=(1024, 1024))