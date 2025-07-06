#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : mineru
# @Time         : 2025/1/23 13:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

import requests

token = """
eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiI4MDAwNDQ3NyIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTczNzYxMTQ5MiwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiIiwidXVpZCI6IjczNTZjNjY1LTU4MTMtNGQxNC04ZjFiLWM0NWIyZmFhYTBhMCIsImVtYWlsIjoiMzEzMzAzMzAzQHFxLmNvbSIsImV4cCI6MTczODgyMTA5Mn0.i8CwWoRE6j5wAC_hD9z9amkWT56HdOewgXMFV4jMpg17JHB0HOY-K4o9zp06Puav2vxkuC3Lnqm_8ip7-QdxsQ
"""
url = 'https://mineru.net/api/v4/extract/task'
header = {
    'Content-Type': 'application/json',
    "Authorization": f"Bearer {token.strip()}"
}
data = {
    'url': 'https://cdn-mineru.openxlab.org.cn/demo/example.pdf',
    'is_ocr': True,
    'enable_formula': False,
}

res = requests.post(url, headers=header, json=data)
print(res.status_code)
print(res.json())
print(res.json()["data"])

# {'task_id': 'adb223f6-794b-4950-8d60-d766ebd0bf14'}

task_id = 'adb223f6-794b-4950-8d60-d766ebd0bf14'
import requests

url = f'https://mineru.net/api/v4/extract/task/{task_id}'
header = {
    'Content-Type':'application/json',
    "Authorization": f"Bearer {token.strip()}"
}

res = requests.get(url, headers=header)
print(res.status_code)
print(res.json())
print(res.json()["data"])