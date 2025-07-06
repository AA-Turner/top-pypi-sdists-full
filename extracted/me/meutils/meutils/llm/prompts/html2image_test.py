#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : html2image
# @Time         : 2024/9/18 14:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from html2image import Html2Image

hti = Html2Image()

html_content = Path('x.html').read_text()

# hti.screenshot(html_str=html_content, save_as='output_desktop.png', size=(1920, 1080))
hti.screenshot(html_str=html_content, save_as='output_mobile.png', size=(375, 812))
