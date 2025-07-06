#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/5/23 13:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *



import requests
import json

url = "https://tools.dreamfaceapp.com/dw-server/face/animate_image_web"

payload = json.dumps({
   "aigc_img_no_save_flag": False,
   "template_id": "6606889f54e4e700070db4b1",
   "app_version": "4.7.1",
   "timestamp": 1747978119668,
   "user_id": "d7668b9337aa943709a4387101583ab1",
   "no_water_mark": 0,
   "merge_by_server": False,
   "account_id": "67fcdea4ae936300076d8d89",
   "pt_infos": [
      {
         "lan": "en",
         "audio_id": "6d770a8819e946a797aec5bb43547142",
         "context": "a dog",
         "voice_engine_id": "prompt_97f7a53122124635be47b3a773c061e6",
         "video_url": "https://cdns3.dreamfaceapp.com/web/common/material/219e971f53e54f3bb8fe9d55e12a1688.mp4"
      }
   ],
   "work_type": "AVATAR_VIDEO",
   "santa_info": {
      "email": "",
      "signature": ""
   },
   "photo_info_list": [
      {
         "photo_path": "",
         "origin_face_locations": [
            {
               "left_upper_x": 0,
               "left_upper_y": 0,
               "right_width": 1,
               "down_high": 1
            }
         ],
         "square_face_locations": [
            {
               "left_upper_x": 0,
               "left_upper_y": 0,
               "down_high": 1,
               "right_width": 1
            }
         ],
         "five_lands": [
            [
               [
                  1,
                  1
               ],
               [
                  1,
                  1
               ],
               [
                  1,
                  1
               ],
               [
                  1,
                  1
               ],
               [
                  1,
                  1
               ]
            ]
         ],
         "face_nums": 1,
         "mask_path": ""
      }
   ],
   "play_types": [
      "VIDEO",
      "PT"
   ],
   "ext": {
      "track_info": "{}",
      "sing_title": "a dog",
      "animate_channel": "dynamic"
   }
})
headers = {
   'dream-face-web': 'dream-face-web',
   'priority': 'u=1, i',
   'token': 'eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NDQ2NTQxMTYsInBheWxvYWQiOnsiaWQiOiI2N2ZjZGVhNGFlOTM2MzAwMDc2ZDhkODkiLCJ0aGlyZFBsYXRmb3JtIjoiR09PR0xFIiwidGhpcmRJZCI6IjExMTQ5Nzk1NTUyNjQxMTE4MjUwNiIsInBhc3N3b3JkIjpudWxsLCJ0aGlyZEV4dCI6eyJlbWFpbCI6ImFpY2hhdGZpcmVAZ21haWwuY29tIiwibmFtZSI6Im1lIGJldHRlciIsImdlbmRlciI6bnVsbCwiYmlydGhkYXkiOm51bGwsIm5pY2tOYW1lIjpudWxsLCJnaXZlbk5hbWUiOiJtZSIsImZhbWlseU5hbWUiOiJiZXR0ZXIiLCJwcm9maWxlUGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0lnU1NDaHMxRDRzVGoxU1RrN1BzVG03eTUzSkRYOTlvOEJ4cFpjVjY1NjBBSmJSZz1zOTYtYyJ9LCJjcmVhdGVUaW1lIjoxNzQ0NjI1MzE2MDIyLCJ1cGRhdGVUaW1lRm9ybWF0IjoiMjAyNS0wNC0xNCAxODowODozNi4wMjIiLCJkZWxldGUiOm51bGwsImNyZWF0ZVRpbWVGb3JtYXQiOiIyMDI1LTA0LTE0IDE4OjA4OjM2LjAyMiIsInVwZGF0ZVRpbWUiOjE3NDQ2MjUzMTYwMjIsInBsYXRmb3JtVHlwZSI6Mn19.Rxt41B__ExhAHdmCHMiDDOkFl8IddSena5lsxbnNEX0',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'content-type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
