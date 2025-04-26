#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2024/11/11 10:26
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

NOTICE = get_resolve_path('./NOTICE.html', __file__).read_text()

FOOTER = get_resolve_path('./FOOTER.md', __file__).read_text()