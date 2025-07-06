#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/5/23 14:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

import requests
import json

url = "https://tools.dreamfaceapp.com/dw-server/face/animate_image_web"


def create_task(token: Optional[str] = None):
    headers = {
        'dream-face-web': 'dream-face-web',
        'priority': 'u=1, i',
        'token': 'eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NDgwMDg1NDMsInBheWxvYWQiOnsiaWQiOiI2ODMwMDdhNDI2YmNjZDAwMDhlYjMxMjIiLCJ0aGlyZFBsYXRmb3JtIjoiR09PR0xFIiwidGhpcmRJZCI6IjEwMjg2OTM5NzI4OTkyMjc5NTE5MyIsInBhc3N3b3JkIjpudWxsLCJ0aGlyZEV4dCI6eyJlbWFpbCI6ImpyMTU5NjIyOTQ5ODBAZGp2Yy51ayIsIm5hbWUiOiJ6enkzMDIwOCB5a2Z3eDEyMjgxIiwiZ2VuZGVyIjpudWxsLCJiaXJ0aGRheSI6bnVsbCwibmlja05hbWUiOm51bGwsImdpdmVuTmFtZSI6Inp6eTMwMjA4IiwiZmFtaWx5TmFtZSI6InlrZnd4MTIyODEiLCJwcm9maWxlUGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0tGQXBqUjVZTVhqLXNEYWhWRGw5YVNQT0VuVGlSaXFlMUQ0RTNEU1J5Nno1Wk9FQT1zOTYtYyJ9LCJjcmVhdGVUaW1lIjoxNzQ3OTc4MTQ4NDU0LCJ1cGRhdGVUaW1lRm9ybWF0IjoiMjAyNS0wNS0yMyAxMzoyOTowOC40NTQiLCJkZWxldGUiOm51bGwsImNyZWF0ZVRpbWVGb3JtYXQiOiIyMDI1LTA1LTIzIDEzOjI5OjA4LjQ1NCIsInVwZGF0ZVRpbWUiOjE3NDc5NzgxNDg0NTQsInBsYXRmb3JtVHlwZSI6Mn19.aWdRtZhxch0iQ7xsmR-Im_MLEqgWy7dW8eRigUxz4es',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'content-type': 'application/json'
    }

    payload = {
        "aigc_img_no_save_flag": False,
        "template_id": "6606889f54e4e700070db4b1",
        "app_version": "4.7.1",
        "timestamp": 1747980670819,
        "user_id": "bda0f9897c2aa378c5230cff3418168a",
        "no_water_mark": 1,
        "merge_by_server": False,
        "account_id": "683007a426bccd0008eb3122",
        "pt_infos": [
            {
                "lan": "zh",
                "audio_id": "6629c44502c44c00073515e1",
                "context": "这个屌公司一群傻逼吧",
                "voice_engine_id": "zh-CN-XiaomengNeural",
                "video_url": "https://lmdbk.com/5.mp4"
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
            "sing_title": "这个屌公司一群傻逼吧",
            "animate_channel": "dynamic"
        }
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    create_task()