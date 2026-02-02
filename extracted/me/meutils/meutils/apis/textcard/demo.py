#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2024/9/18 10:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import re

from meutils.pipe import *

HTML_PARSER = re.compile(r'```html(.*?)```', re.DOTALL)
s = """
这是一堆文本
```html
这是一段html
```
这是一堆文本
"""

print(HTML_PARSER.findall(s))

# {"messages":[{"role":"user","content":"早饭"}],"chat_id":"ssZZTRs","model":"Qwen/Qwen2-Math-72B-Instruct"}
