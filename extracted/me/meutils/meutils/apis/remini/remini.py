#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : remini
# @Time         : 2024/7/24 17:36
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import httpx

from meutils.pipe import *

# 上传文件
"https://app.remini.ai/result?utm_medium=try-remini&v=e0b2645d-59ee-496f-822b-61266422397a-1721800092479&mediaType=image"
"https://app.remini.ai/result?utm_medium=try-remini&v=e0b2645d-59ee-496f-822b-61266422397a-1721800092479&mediaType=image&taskId=75cb6bca-0dfb-444b-8f91-82daddde2976"


import requests
import json

url = "https://app.remini.ai/api/v1/web/tasks/bulk-upload"

payload = json.dumps({
   "input_task_list": [
      {
         "image_content_type": "image/jpeg",
         "output_content_type": "image/jpeg",
         "ai_pipeline": {
            "bokeh": {
               "vivid": "0.75",
               "highlights": "0.25",
               "group_picture": "true",
               "aperture_radius": "0.30",
               "apply_front_bokeh": "false",
               "rescale_kernel_for_small_images": "true"
            },
            "face_enhance": {
               "model": "remini"
            },
            "jpeg_quality": 90,
            "background_enhance": {
               "model": "rhino-tensorrt"
            }
         }
      }
   ]
})
headers = {
   'authorization': 'Bearer 54a2d77f30704a958a1b906ac1c74d44.a0e8b69805a9f1b10303b95109c3ffca735fe309400f5034f58cca54909c44f55c26f1506948e3050430788646b3a36406bc070243a3b436e6c14f3daa88ce54',
   'priority': 'u=1, i',
   'Cookie': 'OptanonAlertBoxClosed=2024-07-10T07:05:39.777Z; _hjSessionUser_3525893=eyJpZCI6Ijk2Yjk3Mzg1LThjY2UtNWFjZS05YzU1LWM2NmM1NmZjZGI0MyIsImNyZWF0ZWQiOjE3MjA1OTUxNTY3ODYsImV4aXN0aW5nIjp0cnVlfQ; _gid=GA1.2.926197006.1721800038; _hjSessionUser_3043925=eyJpZCI6IjZmMGRiYjgzLTgzYTUtNThiOS04NTNiLTk0OTc3NGVmMzRjNSIsImNyZWF0ZWQiOjE3MjA1OTUxMzMzNDQsImV4aXN0aW5nIjp0cnVlfQ; _pico_cid=1bcf4dbf-f2b4-4608-8a3b-6f58cc19212e; OptanonConsent=isGpcEnabled; _hjSessionUser_2996761=eyJpZCI6IjNmMWI4MThkLTNhZjMtNTE3YS1iM2ZmLTIwZTg4NDEzOTJmMSIsImNyZWF0ZWQiOjE3MjE4MDAwOTgyMDEsImV4aXN0aW5nIjpmYWxzZX0; __stripe_mid=b79bc88d-9f4a-45e2-a248-022e850ef050c24417; _ga_5LMYDNFSDH=GS1.1.1721813433.3.0.1721813433.0.0.0; _ga=GA1.1.471085307.1720595133; _hjSession_3043925=eyJpZCI6IjBmNWRlNGY5LTZiN2YtNDQxMC1iYzhlLWU1MjBlM2VhMjQzMyIsImMiOjE3MjE4MTM0MzMxODUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0; _hjSession_3525893=eyJpZCI6IjY3NzE0OWRkLTI0ZDAtNGU2Zi1iYjkwLTEyOTAxMzczYzQ3ZCIsImMiOjE3MjE4MTM0MzcxOTAsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'content-type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
#
print(response.json())
#
# {
#     "bulk_upload_id": "939cb680-b80b-49f4-9098-28e36e9ac381",
#     "task_list": [
#         {
#             "task_id": "435c8a76-26eb-48bf-ba20-02df11648c97",
#             "upload_url": "https://storage.googleapis.com/bsp-remini-image-in-web-us-central1-autodelete/54a2d77f-3070-4a95-8a1b-906ac1c74d44/435c8a76-26eb-48bf-ba20-02df11648c97/25e310aa/input.jpg?X-Goog-Algorithm=GOOG4-HMAC-SHA256&X-Goog-Credential=GOOG1ETQDJI557KBP4YD5TQG6FMZHVKCP3S53FHI6XLBYYMT24W3PZAZNZZWQ%2F20240724%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20240724T093850Z&X-Goog-Expires=3600&X-Goog-SignedHeaders=content-type%3Bhost%3Bx-goog-custom-time&X-Goog-Signature=15a57b1f424d714d309533fec893c416ce8e7fb8841564ca7a7f5f16e9a2d2c3",
#             "upload_headers": {
#                 "Content-Type": "image/jpeg",
#                 "x-goog-custom-time": "2024-08-07T09:38:50Z"
#             }
#         }
#     ]
# }


file = open('test.png', 'rb').read()
files = [('file', ('x.png', file, 'image/png'))]
files ={'file': file}

upload_url = response.json()['task_list'][0]['upload_url']
upload_headers = response.json()['task_list'][0]["upload_headers"]
# r = httpx.options(upload_url, headers=headers)
# print(r.text)
headers = {**headers, **upload_headers}
print(headers)
r = httpx.put(upload_url, files=files, headers=headers)
print(r.text)

from meutils.io.files_utils import file_to_base64