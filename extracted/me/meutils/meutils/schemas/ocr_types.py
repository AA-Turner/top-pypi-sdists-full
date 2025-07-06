#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ocr_types
# @Time         : 2024/9/27 10:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


class OCRRequest(BaseModel):
    """
    plain texts OCR & format texts OCR: 这两种模式适用于图像 OCR。
    plain multi-crop OCR & format multi-crop OCR: 对于内容更复杂的图片，您可以使用这些模式获得更高质量的结果。
    plain fine-grained OCR & format fine-grained OCR: 在这些模式下，您可以在输入图片上指定细粒度区域，以实现更灵活的 OCR。细粒度区域可以是方框的坐标、红色、蓝色或绿色。
    """
    image: str

    mode: Literal[
        'simple',
        'plain texts OCR', 'plain multi-crop OCR', 'plain fine-grained OCR',
        'format texts OCR', 'format multi-crop OCR', 'format fine-grained OCR'] = "plain texts OCR"

    fine_grained_mode: Literal['box', 'color'] = "color"
    """plain fine-grained OCR
    "box", "", "[409,763,756,891]"
    "color", "red", ""
    """
    ocr_color: Literal['red', 'green', 'blue'] = "red"
    """plain fine-grained OCR"""
    ocr_box: str = ""
    """plain fine-grained OCR
    The input value that is provided in the "input box: [x1,y1,x2,y2]" Textbox component.
    """
