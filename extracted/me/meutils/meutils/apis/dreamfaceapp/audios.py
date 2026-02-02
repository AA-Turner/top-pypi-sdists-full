#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : audios
# @Time         : 2025/5/23 14:12
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

import requests
import json

url = "https://tools.dreamfaceapp.com/df-server/audio/v2/get_animate_audio_list"

payload = json.dumps({
    "code": "zh"
})
headers = {
    'dream-face-web': 'dream-face-web',
    'priority': 'u=1, i',
    'token': 'eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NDgwMDg1NDMsInBheWxvYWQiOnsiaWQiOiI2ODMwMDdhNDI2YmNjZDAwMDhlYjMxMjIiLCJ0aGlyZFBsYXRmb3JtIjoiR09PR0xFIiwidGhpcmRJZCI6IjEwMjg2OTM5NzI4OTkyMjc5NTE5MyIsInBhc3N3b3JkIjpudWxsLCJ0aGlyZEV4dCI6eyJlbWFpbCI6ImpyMTU5NjIyOTQ5ODBAZGp2Yy51ayIsIm5hbWUiOiJ6enkzMDIwOCB5a2Z3eDEyMjgxIiwiZ2VuZGVyIjpudWxsLCJiaXJ0aGRheSI6bnVsbCwibmlja05hbWUiOm51bGwsImdpdmVuTmFtZSI6Inp6eTMwMjA4IiwiZmFtaWx5TmFtZSI6InlrZnd4MTIyODEiLCJwcm9maWxlUGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0tGQXBqUjVZTVhqLXNEYWhWRGw5YVNQT0VuVGlSaXFlMUQ0RTNEU1J5Nno1Wk9FQT1zOTYtYyJ9LCJjcmVhdGVUaW1lIjoxNzQ3OTc4MTQ4NDU0LCJ1cGRhdGVUaW1lRm9ybWF0IjoiMjAyNS0wNS0yMyAxMzoyOTowOC40NTQiLCJkZWxldGUiOm51bGwsImNyZWF0ZVRpbWVGb3JtYXQiOiIyMDI1LTA1LTIzIDEzOjI5OjA4LjQ1NCIsInVwZGF0ZVRpbWUiOjE3NDc5NzgxNDg0NTQsInBsYXRmb3JtVHlwZSI6Mn19.aWdRtZhxch0iQ7xsmR-Im_MLEqgWy7dW8eRigUxz4es',
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'content-type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
