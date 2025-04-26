#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2024/12/16 17:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from openai import  AsyncClient
from meutils.pipe import *
from meutils.apis.jimeng.doubao_utils import generate_cookie

from meutils.schemas.image_types import ImageRequest

from meutils.schemas.jimeng_types import BASE_URL, MODELS_MAP, FEISHU_URL
from meutils.apis.jimeng.common import create_draft_content, get_headers, check_token
from meutils.config_utils.lark_utils import get_next_token_for_polling


async def create_():
    headers = {
        'agw-js-conv': 'str',
        'Cookie': 's_v_web_id=verify_m4t9wrdc_qgbhUw0z_07iP_4GFV_8HA7_6jr0e9lLCqQO; passport_csrf_token=8a8aa82fa109ecb3cb25e7afa10de214; passport_csrf_token_default=8a8aa82fa109ecb3cb25e7afa10de214; oauth_token=e45378cb-5afd-4495-88f5-58440e321b48; n_mh=lG4jjJNpPRqpnflIMXQoPMflNZdP31M8fFqgdR9Id5g; uid_tt=1a11a8af13cf1c878482fa862287107c; uid_tt_ss=1a11a8af13cf1c878482fa862287107c; sid_tt=de2215a7bb8e442774cf388f03fac84c; sessionid=de2215a7bb8e442774cf388f03fac84c; sessionid_ss=de2215a7bb8e442774cf388f03fac84c; is_staff_user=false; store-region=cn-js; store-region-src=uid; odin_tt=774fcc6d25d5259fd2af19858e0518c64943eb788718658b403ad8eb13ebbc6ebcb4c42620e87a48b2efb45fe78dc163b82399750898bb201c89f324b9e25b94; passport_auth_status=042935fbff60617ac0735d3ba4cfb559%2C7c535e1ccd98b367728b6560feb66a2e; passport_auth_status_ss=042935fbff60617ac0735d3ba4cfb559%2C7c535e1ccd98b367728b6560feb66a2e; sid_guard=de2215a7bb8e442774cf388f03fac84c%7C1734489199%7C5184000%7CSun%2C+16-Feb-2025+02%3A33%3A19+GMT; sid_ucp_v1=1.0.0-KGQyN2NlYjIxNTA1NTc3ZjI3NWQ2MjZkY2FhNGM3MGM0NzdkNGVjZDMKHwjAreC708zWBBDv6Ii7BhjCsR4gDDDn782qBjgIQCYaAmxxIiBkZTIyMTVhN2JiOGU0NDI3NzRjZjM4OGYwM2ZhYzg0Yw; ssid_ucp_v1=1.0.0-KGQyN2NlYjIxNTA1NTc3ZjI3NWQ2MjZkY2FhNGM3MGM0NzdkNGVjZDMKHwjAreC708zWBBDv6Ii7BhjCsR4gDDDn782qBjgIQCYaAmxxIiBkZTIyMTVhN2JiOGU0NDI3NzRjZjM4OGYwM2ZhYzg0Yw; ttwid=1%7C4rAQ216JOophOdIJRX4cHa6E8FSBjbjqHCKmFCNrQuc%7C1734510550%7C6217dce55189d102c393a4de7022e9ee2e2fa75f211108551b349a0a04532921; passport_fe_beating_status=true; tt_scid=b.csKGNI6QALEo8gG9vJu3nCfptGnLkTxVXPX.wNPQ0q9PaXuKzXfuFQC0i2U7gVa974; gd_random_1831913=eyJtYXRjaCI6ZmFsc2UsInBlcmNlbnQiOjAuMjIzMzcxMDAwNzk1MzUxNzd9.NuOx3z2e4BUOJrwTMG9F3lxrnhmz9jNR6BrhQYU4BhI; gd_random_1525008=eyJtYXRjaCI6ZmFsc2UsInBlcmNlbnQiOjAuMjIzMzcxMDAwNzk1MzUxNzd9.NuOx3z2e4BUOJrwTMG9F3lxrnhmz9jNR6BrhQYU4BhI; gd_random_1831904=eyJtYXRjaCI6ZmFsc2UsInBlcmNlbnQiOjAuMjIzMzcxMDAwNzk1MzUxNzd9.NuOx3z2e4BUOJrwTMG9F3lxrnhmz9jNR6BrhQYU4BhI; msToken=enism5q1i_XLtL8VKKjkjidcvGhyW0U3EGJBI19P3fyqk8NsW4fXW4g8s4TnlgRaF-aWS0kHrmNnENw5L4mFRyyz6A5yZbpR3nCRYJrvBi3-GrtptyOBhznILSv4OO0',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'content-type': 'application/json'
    }
    payload = {
        "messages": [
            {
                "content": "{\"text\":\"颜色反转\"}",
                "content_type": 2009,
                "attachments": [
                    {
                        "type": "image",
                        "key": "tos-cn-i-a9rns2rl98/b87240eb828f43f8a87952e8246f2143.png",
                        "extra": {
                            "refer_types": "style"
                        },
                        "identifier": "2c4b5ab0-bd1a-11ef-b0b0-d38662f7353b"
                    }
                ]
            }
        ],
        "completion_option": {
            "is_regen": False,
            "with_suggest": False,
            "need_create_conversation": False,
            "launch_stage": 1,
            "is_replace": False,
            "is_delete": False,
            "message_from": 0,
            "event_id": "0"
        },
        "section_id": "533682637787650",
        "conversation_id": "533682637787394",
        "local_message_id": "71ee47b0-bd1c-11ef-b0b0-d38662f7353b"
    }

    client = AsyncClient(base_url="https://www.doubao.com/samantha", default_headers=headers, api_key='xx')
    response = await client.post("/chat/completion", body=payload, cast_to=object, stream=True)
    for i in response:
        print(i)
    # return response

if __name__ == '__main__':
   arun(create())