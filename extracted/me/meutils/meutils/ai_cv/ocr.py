#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ocr
# @Time         : 2023/5/18 16:11
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/RapidAI/RapidOCR/wiki/RapidOCR%E8%B0%83%E4%BC%98%E5%B0%9D%E8%AF%95%E6%95%99%E7%A8%8B

# LocalOcr

from meutils.pipe import *
from rapidocr_onnxruntime import RapidOCR

# from rapidocr_openvino import RapidOCR

rapid_ocr = RapidOCR()
# results, elapse = rapid_ocr('invoice.jpg')
# results, elapse = rapid_ocr('tbl.png')
results, elapse = rapid_ocr('bg.png')

rprint(results)
print([i[1] for i in results])

# rprint([dict(zip(['坐标', '文字'], r)) for r in results])
