#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : spider
# @Time         : 2024/1/18 12:09
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 经纬度
import json

import requests

url = "https://api.map.baidu.com"

params = {'qt': 'gc',
          'wd': '南京市雨花台区南京南站',
          'cn': '北京市',
          'ie': 'utf-8',
          'oue': '1',
          'fromproduct': 'jsapi',
          'v': '2.1',
          'res': 'api',
          'callback': 'BMap._rd._cbk57312',
          'ak': 'CG8eakl6UTlEb1OakeWYvofh',
          'seckey': 
              'WDTCqRTPViBQC9Ntv0XlrvG64IBwuCDpqNqu6KxRpWc=,7l5VkLxKddt3oR9nwbL-1orEnLu4akSUBIJtOhRdQkb2ygfQkyF-9TRkDdRZ7S_QC0jX2agOfZKRm8-xer6QNJhpBAbzbUxcF9EoqGsPNM7AIXv0ir0egW1Rn_sopbnwTHImbltrTpXrnW4-0t6P9X43lh8-DlPyZItvM2283GAc4hz7IiJcGYB3n_GLO9AE-9vGy_QGY88XZ8UatiJA8A',
          'timeStamp': '1730434021654',
          'sign': 'd8afe5934cbd'
          }


response = requests.request("GET", url, params=params)

data = response.text.strip(')').split('(', 1)[-1]

json.loads(data)