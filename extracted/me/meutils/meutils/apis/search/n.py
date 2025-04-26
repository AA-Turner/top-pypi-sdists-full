#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : n
# @Time         : 2024/12/6 17:51
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json

from meutils.pipe import *
import httpx

BASE_URL = 'https://n.cn/api/common'
url = "/conversation/v2"

# Headers
headers = {
    'access-token': '12113771263956298908596801732877',
    'auth-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtaWQiOiIxMjExMzc3MTI2Mzk1NjI5ODkwODU5NjgwMTczMjg3NyIsInFpZCI6IiIsImRldGFpbCI6ImxvZ2luIiwiZXhwIjoxNzM0NzczODM0fQ.TE1UEoSSzWWPeEY8s3goiHuwNvLi6uCEu3r5WA7oop4',
    'chat-token': 'f3d6075b0fe2a4d0497c6a6cd0697c35D1vZ0xSNLxfIUnJqpvpDlb=/-ttIYxjLMb3EMrWwBZU1doBGbL3ZAVmzayK88v4PMHDv3pgnqKCjtMOX7wIXGmMLQdlGz/NxAfFOqMN98gNS+JMtNQ3cqfcQELgNPOnBwFJMk0=',
    'device-platform': 'Web',

    'request-id': '9d805c53-1fae-4db3-80f8-990b222747d2',

    'chat-date': 'Fri, 06 Dec 2024 09:59:53 GMT',  # 页面过期

    'sid': '12113771263956298908596801732877',
    'timestamp': '2024-12-06T17:59:53+08:00',
    'zm-token': 'a3c840bbc53ab84b1b91cd70a8a80b3e',
    'zm-ua': 'a455ebc67d0b5007e2a055414dd14d78',
    'zm-ver': '1.2',
    'Cookie': '__guid=12113771.405349637294117200.1732877020501.2803; webp=1; sdt=afb18c30-6534-4cb2-8c18-ade7636c7a47; _ga=GA1.1.2029555368.1732877022; Q=u%3D360H1374548850%26n%3DLhna_643%26le%3D%26m%3DZGt1WGWOWGWOWGWOWGWOWGWOZwZm%26qid%3D1374548850%26im%3D1_t01b9f6bfa3ea676416%26src%3Dpcw_namiso%26t%3D1; __NS_Q=u%3D360H1374548850%26n%3DLhna_643%26le%3D%26m%3DZGt1WGWOWGWOWGWOWGWOWGWOZwZm%26qid%3D1374548850%26im%3D1_t01b9f6bfa3ea676416%26src%3Dpcw_namiso%26t%3D1; T=s%3D65ecc6b3a47cc8e6df468f2246926051%26t%3D1732877071%26lm%3D0-1%26lf%3D2%26sk%3D93ed9bbe8cc2756ce12afad645453560%26mt%3D1732877071%26rc%3D%26v%3D2.0%26a%3D1; __NS_T=s%3D65ecc6b3a47cc8e6df468f2246926051%26t%3D1732877071%26lm%3D0-1%26lf%3D2%26sk%3D93ed9bbe8cc2756ce12afad645453560%26mt%3D1732877071%26rc%3D%26v%3D2.0%26a%3D1; __DC_sid=12113771.2545635413030612000.1733477831073.6633; Auth-Token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtaWQiOiIxMjExMzc3MTI2Mzk1NjI5ODkwODU5NjgwMTczMjg3NyIsInFpZCI6IiIsImRldGFpbCI6ImxvZ2luIiwiZXhwIjoxNzM0NzczODM0fQ.TE1UEoSSzWWPeEY8s3goiHuwNvLi6uCEu3r5WA7oop4; __quc_silent__=1; test_cookie_enable=null; _ga_F1YB4HZHRB=GS1.1.1733477842.2.1.1733478071.14.0.1241444979; _ga_BCGTJC5JR6=GS1.1.1733477842.2.1.1733478071.0.0.0; __DC_monitor_count=12; _ga_MY08QYRPTL=GS1.1.1733477835.1.1.1733478388.31.0.1234880602; __DC_gid=12113771.779991695.1732877017079.1733479193697.18',
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

# Request data
data = {
    "conversation_id": "b18ae6a0b87a4b0f86f87ec2a36938c3",
    "message_id": "1864973026710818816",

    "re_answer_msg_id": "",
    "prompt": "周杰伦",
    "is_so": True,
    "is_copilot_enabled": False,
    "answer_mode": 4,
    "source_type": "prophet_web",
    "retry": False,
    "re_answer": 0,
    "search_type": "360",
    "model_type": "",
    "intention": "",
    "last_id": 0,
    "search_method": "1",
    "search_args": {},
    "msg_type": "",
    "kwargs": {
        "fr": "none",
        "zhuiwen": {
            "query": "周杰伦",
            "answer": "周杰伦",  # todo 追问拓展
        }
    }
}


# Make the request

async def create():
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        payload = {
            "title": "周杰伦",
            "answer_mode": 4,
            "kwargs": {"fr": "none"}
        }
        response = await client.post("/conversation/v2", data=payload)
        logger.debug(response.json())

        _data = response.json()['data']

        data.update()
        logger.debug(data)
        data['conversation_id'] = _data['conversation_id']
        data['message_id'] = _data['msg_id']

        async with client.stream(method="POST", url="/chat/v2", json=data) as response:
            response.raise_for_status()
            logger.debug(response.status_code)

            # logger.debug(response.status_code)
            async for chunk in response.aiter_lines():
                # for chunk in "response.aiter_lines()":
                yield chunk


if __name__ == "__main__":
    arun(create())
