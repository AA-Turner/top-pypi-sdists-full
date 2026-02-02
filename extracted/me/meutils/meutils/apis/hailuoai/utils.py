#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2026/1/20 10:36
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


import oss2

from meutils.pipe import *
from meutils.hash_utils import md5
from meutils.io.files_utils import to_bytes
from meutils.jwt_utils import decode_jwt_token
from meutils.schemas.hailuo_types import BASE_URL_ABROAD as BASE_URL

from meutils.schemas.hailuo_types import VideoRequest, VideoResponse
from meutils.llm.check_utils import check_tokens
from meutils.decorators.retry import retrying
from meutils.notice.feishu import send_message as _send_message, VIDEOS

from meutils.apis.hailuoai.yy import get_yy

APP_ID = '3001'
VERSION_CODE = '22203'

PARAMS = {
    'device_platform': 'web',
    'app_id': APP_ID,
    'version_code': VERSION_CODE,
    'biz_id': '0',
    'os_name': 'Mac',
    'browser_name': 'chrome',
    'device_memory': '8',
    'cpu_core_num': '10',
    'browser_language': 'zh-CN',
    'browser_platform': 'MacIntel',
    'screen_width': '1920',
    'screen_height': '1080',
    'lang': "zh-Intl",

    'uuid': '8c059369-00bf-4777-a426-d9c9b7984ee6',
    'device_id': '339114928865529864',
    'unix': f'{int(time.time())}000'
}


@alru_cache(ttl=1 * 24 * 60 * 60)
@retrying()
async def get_access_token(token: str):
    params = PARAMS.copy()

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'token': token,
        'yy': get_yy(payload, params=params, url="/v1/api/user/renewal")
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post("/v1/api/user/renewal", params=params, content=json.dumps(payload))
        response.raise_for_status()
        logger.debug(response.json())
        return response.json()['data']['token']


@alru_cache(ttl=1 * 60)
async def get_request_policy(token):
    """
    {
        "data": {
            "accessKeyId": "STS.NUVNbdQfqTNixCxUTAhdeJToq",
            "accessKeySecret": "DRBsh8Qm8VnXXxTwFMX5KkXVoqbbsPj4ewEfgTLysGvM",
            "securityToken": "CAISiwN1q6Ft5B2yfSjIr5bjBdjQvLlQ44yCemXJsVQUZOtJpZHEkzz2IHhMf3VpAusWsPw1n2tT6/sdlrBoS4JMREPJN5EhtsQLrl75PdKY4Jzltedb0EIf6JFQUUyV5tTbRsmkZj+0GJ70GUem+wZ3xbzlD2vAO3WuLZyOj7N+c90TRXPWRDFaBdBQVH0AzcgBLinpKOqKOBzniXayaU1zoVhYiHhj0a2l3tbmvHi4tlDhzfIPrIncO4Wta9IWXK1ySNCoxud7BOCjmCdb8EpN77wkzv4GqzLGuNCYCkkU+wiMN+vft9ZjKkg7RNBjSvMa8aWlzKYn57OCyt2v8XsXY7EJCRa4bZu73c7JFNmuMtsEbrvhMxzPqIvXbsKp6lh/MSxDblgRIId8dWURExUpTSrBIaOh6M4Bo5NbzHzuOsgSpnkVpz2AlbLiT9M/1aieRiRTcymwO/ayjeq6CeAF3mM8Mm0qPRouTM2+Zo5YD3N1opjTpiapdUYLox8awbuQLp25tMiF6FiLDvouuRqAAQJZHVcOeb5qnR6mkzw5hwzSOXoMXVFzDE2aB7dvRYFD9HiG6T66hE4Xlfpph9H7xWrpaBf5vqHQXp4gyuqVOgFIjdPECwisXlyAKQWMak7bGToh3cetCux3pjq74sP/KAjzSzDkwciJBbn8vZzNKKR/ozxqve925vtPPPWGPowwIAA=",
            "expiration": "2024-10-22T02:55:14Z",
            "dir": "cdn-yingshi-ai-com/prod/2024-10-22-09/user/multi_chat_file",
            "endpoint": "oss-cn-wulanchabu.aliyuncs.com",
            "bucketName": "minimax-public-cdn",
            "serverTime": "2024-10-22T02:10:07Z"
        }
    }
    """
    # token = await get_access_token(token)

    headers = {
        'token': token,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }


    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.get("/v1/api/files/request_policy")
        response.raise_for_status()
        return response.json()['data']


async def upload(file: bytes, token: str):
    data = await get_request_policy(token)

    access_key_id = data["accessKeyId"]
    access_key_secret = data["accessKeySecret"]
    security_token = data["securityToken"]
    bucket_name = data["bucketName"]
    endpoint = data["endpoint"]
    dir = data["dir"]

    # 创建OSS客户端    with timer():
    #         arun(hailuo_upload(file))
    auth = oss2.StsAuth(access_key_id, access_key_secret, security_token)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    # file
    size = len(file)

    # 要上传的文件路径和文件名
    mimeType = "png"
    filename = f"{uuid.uuid4()}.{mimeType}"
    object_name = f"{dir}/{filename}"  # png写死
    bucket.put_object(object_name, file)

    params = {}
    payload = {
        "originFileName": "_.png",
        # "originFileName": "503af3b5-9c3b-4bdc-a6d4-256debce3dd5_00001_.png",

        "filename": filename,
        # "fileName": "db884a7c-99a4-40f5-929e-db8769dbf64a.png",

        "dir": dir,
        "endpoint": "oss-cn-wulanchabu.aliyuncs.com",
        "bucketName": "minimax-public-cdn",
        "size": f"{size}",
        "mimeType": mimeType,
        "fileMd5": md5(file),
        "fileScene": 10
    }
    headers = {
        'token': token
    }
    logger.debug(headers)

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=120) as client:
        response = await client.post("/v1/api/files/policy_callback", params=params, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))
        return data

    # {'data': {'fileID': '307139766909288449',
    #           'ossPath': 'https://cdn.hailuoai.com/prod/2024-10-28-10/user/multi_chat_file/c9d8fc64-d9bf-42c0-8779-f39973579fca.png?image_process=resize,fw_320/format,webp'},
    #  'statusInfo': {'code': 0,
    #                 'debugInfo': '',
    #                 'httpCode': 0,
    #                 'message': '成功',
    #                 'requestID': '33a42a75-15e5-4d4e-b425-eeefc4d3f374',
    #                 'serverAlert': 0,
    #                 'serviceTime': 1730083971}}

async def check_token(token, threshold: int = 30, **kwargs):
    if not isinstance(token, str):
        return await check_tokens(token, check_token)

    try:
        token = await get_access_token(token)
        headers = {
            "token": token
        }
        params = {}
        async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
            response = await client.get("/v1/api/user/equity", params=params)
            response.raise_for_status()
            data = response.json()

            logger.debug(bjson(data))

            return any(i in str(data) for i in {"Ultra", "Unlimited", "高级会员"})
    except Exception as e:
        logger.error(e)
        logger.debug(token)
        return False

if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzIyODE1NzcsInVzZXIiOnsiaWQiOiI0NDQyMjk2MDAzMzA0OTgwNTUiLCJuYW1lIjoibWZ1aiBiamhuIiwiYXZhdGFyIjoiIiwiZGV2aWNlSUQiOiIzMzkxMTQ5Mjg4NjU1Mjk4NjQiLCJpc0Fub255bW91cyI6ZmFsc2V9fQ.__NDyZQQqyYb7TLrumo944EfuCmrbzYngQloNBK4CmM"

    # arun(get_access_token(token))

    arun(get_request_policy(token))

    # access_token = token
    # arun(upload(Path("img.png").read_bytes(), token=access_token))


