#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2024/10/25 22:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json

from meutils.pipe import *
from meutils.apis.hailuoai.hasha import js_code

import execjs

# 编译 JavaScript 代码
context = execjs.compile(js_code)

# 调用 JavaScript 函数
result = context.call("exports", "1729863023000")
print(result)  # 输出: Hello, World

url = "https://hailuoai.com/v1/api/files/policy_callback?device_platform=web&app_id=3001&version_code=22201&uuid=8c059369-00bf-4777-a426-d9c9b7984ee6&device_id=243713252545986562&os_name=Mac&browser_name=chrome&device_memory=8&cpu_core_num=10&browser_language=zh-CN&browser_platform=MacIntel&screen_width=1352&screen_height=878&unix=1729865709000"

payload = json.dumps({"fileName": "2300140d-a576-408b-ba89-40541786a6e4.png",
                      "originFileName": "503af3b5-9c3b-4bdc-a6d4-256debce3dd5_00001_.png",
                      "dir": "cdn-yingshi-ai-com/prod/2024-10-25-22/user/multi_chat_file",
                      "endpoint": "oss-cn-wulanchabu.aliyuncs.com", "bucketName": "minimax-public-cdn",
                      "size": "1681865", "mimeType": "png", "fileMd5": "923e10167a2d7b36e866319dad738b1e",
                      "fileScene": 10})

s = f"""/v1{url.split('/v1', 1)[-1]}_{payload}{context.call("exports", url.rsplit('unix=', 1)[-1])}"""

