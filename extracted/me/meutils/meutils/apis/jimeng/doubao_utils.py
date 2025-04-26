#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/12/18 11:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
import random
import base64
import time
import uuid
import secrets
import string

# 常量定义
MODEL_NAME = "doubao"
DEFAULT_ASSISTANT_ID = "497858"
VERSION_CODE = "20800"
DEVICE_ID = random.random() * 999999999999999999 + 7000000000000000000
WEB_ID = random.random() * 999999999999999999 + 7000000000000000000
USER_ID = str(uuid.uuid4()).replace('-', '')
MAX_RETRY_COUNT = 3
RETRY_DELAY = 5000
FILE_MAX_SIZE = 100 * 1024 * 1024

# 伪装headers
FAKE_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-control": "no-cache",
    "Last-event-id": "undefined",
    "Origin": "https://www.doubao.com",
    "Pragma": "no-cache",
    "Priority": "u=1, i",
    "Referer": "https://www.doubao.com",
    "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


async def acquire_token(refresh_token: str) -> str:
    """
    获取缓存中的access_token
    目前doubao的access_token是固定的，暂无刷新功能

    Args:
        refresh_token: 用于刷新access_token的refresh_token

    Returns:
        str: access_token
    """
    return refresh_token


def generate_fake_ms_token() -> str:
    """
    生成伪msToken
    """
    # 生成96字节的随机数据
    random_bytes = secrets.token_bytes(96)
    # 转换为base64，并替换特殊字符
    token = base64.b64encode(random_bytes).decode('utf-8')
    return token.replace('+', '-').replace('/', '_').rstrip('=')


def generate_random_string(length: int) -> str:
    """
    生成指定长度的随机字符串
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_fake_a_bogus() -> str:
    """
    生成伪a_bogus
    """
    return f"mf-{generate_random_string(34)}-{generate_random_string(6)}"


def generate_params():
    params = {
        "aid": "497858",
        "device_id": int(DEVICE_ID),
        "device_platform": "web",
        "language": "zh",
        "pkg_type": "release_version",
        "real_aid": "497858",
        "region": "CN",
        "samantha_web": "1",
        "sys_region": "CN",
        "tea_uuid": int(WEB_ID),
        "use-olympus-account": "1",
        "version_code": "20800",
        "web_id": int(WEB_ID),
        "msToken": generate_fake_ms_token(),
        "a_bogus": generate_fake_a_bogus()
    }

    return params


def generate_cookie(refresh_token: str, ms_token: Optional[str] = None) -> str:
    """
    生成cookie
    """
    ms_token = ms_token or generate_fake_ms_token()

    current_timestamp = int(time.time())
    cookie_parts = [
        f"is_staff_user=false",
        f"store-region=cn-gd",
        f"store-region-src=uid",
        f"sid_guard={refresh_token}%7C{current_timestamp}%7C5184000%7CSun%2C+02-Feb-2025+04%3A17%3A20+GMT",
        f"uid_tt={USER_ID}",
        f"uid_tt_ss={USER_ID}",
        f"sid_tt={refresh_token}",
        f"sessionid={refresh_token}",
        f"sessionid_ss={refresh_token}",
        f"msToken={ms_token}",
    ]
    return "; ".join(cookie_parts)


async def get_upload_token():  # 3600过期
    """

    {'code': 0,
     'data': {'auth': {'access_key_id': 'AKTPYzNkMjJlNTNjMWE1NDJiN2E5MWFkOTYxMWViYzQxYTM',
                       'current_time': '2024-12-18T11:17:22+08:00',
                       'expired_time': '2024-12-18T12:17:22+08:00',
                       'secret_access_key': 'HFFTkEFKf+0DVpUrYy2yMzvgnkxLMU6+qydnGUSaDmd0vSRedpIi0qmeWSVElyOU',
                       'session_token': 'STS2eyJMVEFjY2Vzc0tleUlkIjoiQUtMVFlUZGhPR0ptWVRNNFl6ZG1OR1JoWVRoaE0yWTJPVFl5TW1SbU0yRmhNREEiLCJBY2Nlc3NLZXlJZCI6IkFLVFBZek5rTWpKbE5UTmpNV0UxTkRKaU4yRTVNV0ZrT1RZeE1XVmlZelF4WVRNIiwiU2lnbmVkU2VjcmV0QWNjZXNzS2V5IjoiTC9WZTVSMmt4N3dsY1kvS0E5alp1WVlpSlVFM0ZjdHMzQ2Q5QjJZMVE3NlRnUDVONWViMmpKQkRQMUdyUEtqeXNYNXRKVkJPdExvVjVNOGFyY24wQ2ZtdUZRRWMxMG8xMSs3UHdKdGY0LzQ9IiwiRXhwaXJlZFRpbWUiOjE3MzQ0OTU0NDIsIlBvbGljeVN0cmluZyI6IntcIlN0YXRlbWVudFwiOlt7XCJFZmZlY3RcIjpcIkFsbG93XCIsXCJBY3Rpb25cIjpbXCJJbWFnZVg6QXBwbHlJbWFnZVVwbG9hZFwiLFwiSW1hZ2VYOkNvbW1pdEltYWdlVXBsb2FkXCJdLFwiUmVzb3VyY2VcIjpbXCJ0cm46SW1hZ2VYOio6KjpTZXJ2aWNlSWQvYTlybnMycmw5OFwiXX0se1wiRWZmZWN0XCI6XCJBbGxvd1wiLFwiQWN0aW9uXCI6W1wiUFNNXCJdLFwiUmVzb3VyY2VcIjpbXCJmbG93LmFsaWNlLnJlc291cmNlX2FwaVwiXX1dfSIsIlNpZ25hdHVyZSI6ImI2MGUxNDZkZTU0Njg2NTdlYzVlZmFjZjJlOWNlOWE5YTdhY2UwNTFlZTdkYTJjZTRmNjdiYmRiM2U4MDQ3N2IifQ=='},
              'service_id': 'a9rns2rl98',
              'upload_host': 'imagex.bytedanceapi.com',
              'upload_path_prefix': 'bot-chat-image'},
     'msg': ''}

    :return:
    """
    cookie = generate_cookie('de2215a7bb8e442774cf388f03fac84c')
    url = "https://www.doubao.com/alice/upload/auth_token"

    headers = {
        'Cookie': cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    payload = {
        "scene": "bot_chat",
        "data_type": "image"
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()

        return response.json()


if __name__ == '__main__':
    # generate_cookie("")

    # arun(get_upload_token())
    print(generate_params())
    # print(get_signing_key('xW9YbDhTlWsXdaN7O2g1lfcyePxf5kJyg/r2mwSZG/iuSmbvVgToO6LVCLmUjVJ3'))
