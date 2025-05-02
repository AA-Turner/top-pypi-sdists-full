#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : system
# @Time         : 2025/4/30 18:06
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

# curl 'https://usa.chatfire.cn/api/option/' \
#   -X 'PUT' \
#   -H 'New-API-User: 1' \
#   -H 'sec-ch-ua-platform: "macOS"' \
#   -H 'Cache-Control: no-store' \
#   -H 'Referer: https://usa.chatfire.cn/setting?tab=operation' \
#   -H 'sec-ch-ua: "Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36' \
#   -H 'Accept: application/json, text/plain, */*' \
#   -H 'Content-Type: application/json' \
#   --data-raw '{"key":"LogConsumeEnabled","value":"false"}'