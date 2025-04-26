#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : video
# @Time         : 2024/7/26 12:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 缓存

from meutils.pipe import *
from meutils.schemas.chatglm_types import VideoRequest, Parameter, BASE_URL, VIDEO_BASE_URL, EXAMPLES
from meutils.schemas.task_types import Task, FileTask

from meutils.decorators.retry import retrying
from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.db.redis_db import redis_aclient

from fake_useragent import UserAgent

ua = UserAgent()

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=siLmTk"
FEISHU_URL_OSS = "https://xchatllm.feishu.cn/sheets/MekfsfVuohfUf1tsWV0cCvTmn3c?sheet=pDMNdT"
send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


@alru_cache(ttl=7 * 24 * 3600)
@retrying()
async def get_access_token(refresh_token: str):
    # logger.debug(refresh_token)
    if access_token := await redis_aclient.get(refresh_token):
        return access_token

    headers = {
        "Authorization": f"Bearer {refresh_token}",
        'User-Agent': ua.random,
        "X-Device-Id": str(uuid.uuid4()),
        "X-Request-Id": str(uuid.uuid4()),
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        response = await client.post('/user/refresh')
        response.raise_for_status()

        logger.debug(response.status_code)
        logger.debug(response.text)

        access_token = response.json()['result']['accessToken']

        await redis_aclient.set(refresh_token, access_token, ex=7 * 24 * 3600)  # 缓存

        return access_token


async def check_token(token: str):
    try:
        await get_access_token(token)
        return True
    except Exception as e:
        logger.error(e)
        return False


async def upload(file: bytes, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)
    access_token = await get_access_token(token)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    files = [('file', ('x.png', file, 'image/png'))]

    async with httpx.AsyncClient(base_url=VIDEO_BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post('/static/upload', files=files)

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            data = response.json()
            if data['status'] == 0:
                return data, token
            raise Exception(data)

        response.raise_for_status()

        # {'message': 'success',
        #  'result': {'source_id': '66a8aa225d5f1682b2a07b5c',
        #             'source_url': 'https://sfile.chatglm.cn/chatglm-videoserver/image/50/5049bae9.png'},
        #  'rid': '6068cc37fd6348728386d15418c438a2',
        #  'status': 0}


async def upload_task(file: bytes, token: Optional[str] = None):  ############################ 过期时间一个月真的吗
    token = token or await get_next_token_for_polling(FEISHU_URL_OSS, from_redis=True)
    access_token = await get_access_token(token)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    files = [('file', ('x.png', file, 'image/png'))]

    async with httpx.AsyncClient(
            base_url="https://chatglm.cn/chatglm/backend-api/assistant", headers=headers,
            timeout=60) as client:
        response = await client.post('/file_upload', files=files)
        response.raise_for_status()

        logger.debug(response.text)
        logger.debug(response.status_code)

        data = response.json()
        url = data['result']['file_url']

        return url


# async def upload_task(file: bytes, token: Optional[str] = None):
#     token = token or await get_next_token_for_polling(FEISHU_URL)
#     access_token = await get_access_token(token)
#
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#     }
#
#     files = [('file', ('x.png', file, 'image/png'))]
#
#     async with httpx.AsyncClient(base_url=VIDEO_BASE_URL, headers=headers, timeout=60) as client:
#         response = await client.post('/static/upload', files=files)
#         response.raise_for_status()
#
#         logger.debug(response.text)
#         logger.debug(response.status_code)
#
#         data = response.json()
#         url = data['result']['source_url']
#
#         return url


@retrying(max_retries=8, max=8, predicate=lambda r: r is True, title=__name__)
async def create_task(request: VideoRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)
    access_token = await get_access_token(token)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    payload = request.model_dump()
    async with httpx.AsyncClient(base_url=VIDEO_BASE_URL, headers=headers, timeout=30) as client:
        response = await client.post('/chat', json=payload)

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            data = response.json()

            if any(i in str(data) for i in {"请稍后再试", }):  # 重试
                return True

            task_id = f"cogvideox-{data['result']['chat_id']}"
            return Task(id=task_id, data=data, system_fingerprint=token)

        response.raise_for_status()


async def get_task(task_id: str, token: str):
    task_id = isinstance(task_id, str) and task_id.split("-", 1)[-1]
    access_token = await get_access_token(token)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    async with httpx.AsyncClient(base_url=VIDEO_BASE_URL, headers=headers, timeout=30) as client:
        response = await client.get(f"/chat/status/{task_id}")

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            data = response.json()
            return data

        response.raise_for_status()


async def composite_video(task_id: str, token: str = None):
    access_token = await get_access_token(token)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    payload = {
        "chat_id": task_id,
        "key": "quiet",
        "audio_id": "669b799d7a9ebbe698de2102"
    }
    # 669b790d7a9ebbe698de20f6 回忆老照片 todo:
    # {chat_id: "66a325cbf66684c40b362a30", key: "epic", audio_id: "669b809d3915c1ddbb3d6705"} 灵感迸发

    async with httpx.AsyncClient(base_url=VIDEO_BASE_URL, headers=headers) as client:
        response = await client.post('/static/composite_video', json=payload)

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            data = response.json()
            return data
        response.raise_for_status()


# https://chatglm.cn/chatglm/video-api/v1/trial/apply post申请
# https://chatglm.cn/chatglm/video-api/v1/trial/status check权限

# async def check_token(refresh_token: str):
#     access_token = await get_access_token(refresh_token)
#
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#     }
#     url = "https://chatglm.cn/chatglm/video-api/v1/trial/status"
#     return httpx.get(url, headers=headers).json()


if __name__ == '__main__':
    # arun(upload_task(Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/apis/kuaishou/test.webp").read_bytes()))
    pass
    refresh_oken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDdlZDVkMDhlY2M0YzFmOGQ1NGU4OGQyMzVmMDYxZCIsImV4cCI6MTczNzg3NzYwNiwibmJmIjoxNzIyMzI1NjA2LCJpYXQiOjE3MjIzMjU2MDYsImp0aSI6ImQxNGNkZTk1ODg2NTRjZjJhZmMzMTYyYzhkOGU3YWZhIiwidWlkIjoiNjYxMTdjNGI1NGIwOTE2NjFjMDZmZWFlIiwidHlwZSI6InJlZnJlc2gifQ.4puphxxCPi5zXIsb1CxuuoJthILYgs9b31Hacq5BePg"

    # token = arun(get_access_token(refresh_oken))
    #     # request = VideoRequest(**EXAMPLES[0])
    #     # arun(create_task(request))
    #     # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3YmFmYWQzYTRmZDU0OTk3YjNmYmNmYjExMjY5NThmZiIsImV4cCI6MTcyMjA1OTYyOSwibmJmIjoxNzIxOTczMjI5LCJpYXQiOjE3MjE5NzMyMjksImp0aSI6ImU3ZTQzNmFiY2IzMDQ2M2M4NTU2M2EzMDI0ODhiYmExIiwidWlkIjoiNjVmMDc1Y2E4NWM3NDFiOGU2ZmRjYjEyIiwidHlwZSI6ImFjY2VzcyJ9.ToOESTWv-EJmhneE14czdAv59OulpuA-FLcB8f190zU"

    request = VideoRequest(**EXAMPLES[0])
    # arun(create_task(request, refresh_oken))
    task = arun(create_task(request))

    # arun(get_task('cogvideox-66ab320d18dd2553920bd664', refresh_oken))
    # arun(refresh_token(refresh_oken))
#     from meutils.config_utils.lark_utils import aget_spreadsheet_values
#
#     df = arun(aget_spreadsheet_values(feishu_url=FEISHU_URL, to_dataframe=True))
#     tokens = """
#     eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDdlZDVkMDhlY2M0YzFmOGQ1NGU4OGQyMzVmMDYxZCIsImV4cCI6MTczNzg3NzYwNiwibmJmIjoxNzIyMzI1NjA2LCJpYXQiOjE3MjIzMjU2MDYsImp0aSI6ImQxNGNkZTk1ODg2NTRjZjJhZmMzMTYyYzhkOGU3YWZhIiwidWlkIjoiNjYxMTdjNGI1NGIwOTE2NjFjMDZmZWFlIiwidHlwZSI6InJlZnJlc2gifQ.4puphxxCPi5zXIsb1CxuuoJthILYgs9b31Hacq5BePg
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3YmFmYWQzYTRmZDU0OTk3YjNmYmNmYjExMjY5NThmZiIsImV4cCI6MTczODAyNDg4MiwibmJmIjoxNzIyNDcyODgyLCJpYXQiOjE3MjI0NzI4ODIsImp0aSI6IjY5Y2ZiNzgzNjRjODQxYjA5Mjg1OTgxYmY4ODMzZDllIiwidWlkIjoiNjVmMDc1Y2E4NWM3NDFiOGU2ZmRjYjEyIiwidHlwZSI6InJlZnJlc2gifQ.u9pIfuQZ7Y00DB6x3rbWYomwQGEyYDSE-814k67SH74
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzNmE4NmM1Yzc2Y2Q0MTcyYTE5NGYxMjQwZTgyMmIwOSIsImV4cCI6MTc0MDUzMzMxMCwibmJmIjoxNzI0OTgxMzEwLCJpYXQiOjE3MjQ5ODEzMTAsImp0aSI6ImI4ZTE3YWNiMGVjMjRiMzc4YWEwMjNkNTYxZDg3NzdkIiwidWlkIjoiNjQ0YTNkMGNiYTI1ODVlOTA0NjAzOWRiIiwidHlwZSI6InJlZnJlc2gifQ.6nTeyJM52tJB4AUCBVvwZz_L3WgIHcC551VIuN6UdzQ
#
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5MDJkN2ZkMzg3YmI0YzU3YmMyMGYzNDcwYjYyODk2ZiIsImV4cCI6MTczNzg3NDQxOSwibmJmIjoxNzIyMzIyNDE5LCJpYXQiOjE3MjIzMjI0MTksImp0aSI6IjFlMTM0NmMzNjBiYjQwNTI5YzYzNzliNWI3ZjJkZWMwIiwidWlkIjoiNjYxMThkNGQ3ODY4YTA5ODViMmNmNGMyIiwidHlwZSI6InJlZnJlc2gifQ.skIlW8NsvGRf-HNYn22GiFm2iqK9CzhV4ZmjwMWRP9g
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyZmM5NmIxYmYzNGM0MGM4OTE5MzBhNWYwN2EyMjQxOCIsImV4cCI6MTczNzg3NDY5NywibmJmIjoxNzIyMzIyNjk3LCJpYXQiOjE3MjIzMjI2OTcsImp0aSI6ImNiNjJiMmMwMzM3NDQ1OTViZTgyNGIyY2M1ZWFkZjk2IiwidWlkIjoiNjVlZDY3OGQ2MTNmMTliYWFiMjBiMTkxIiwidHlwZSI6InJlZnJlc2gifQ.jQmTDY9GzLPwAunE6nLrEX2vX591Se9rJ08inrReV4g
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzODZkZTEyNmY5YmE0MjViOWJkZDY4ODM5ZDJkZTdjMCIsImV4cCI6MTczNzg3NDc2MCwibmJmIjoxNzIyMzIyNzYwLCJpYXQiOjE3MjIzMjI3NjAsImp0aSI6ImY0YzgzNzkwMmUyNDQwZjE4ZTY0MDM4OGEwYTdkZjI4IiwidWlkIjoiNjYxMTkwZWZhZTBiMDlmZTUwMTY5NWVmIiwidHlwZSI6InJlZnJlc2gifQ.07j5dMEXrMaWjfSCWgl1DNN0_iT-Dks_kvn6Tvdia3c
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYTgwN2RkMGI0ZGY0ZDE2OGIxMzQ2OWQ0NTViNDMyMyIsImV4cCI6MTczNzg3NDg0OCwibmJmIjoxNzIyMzIyODQ4LCJpYXQiOjE3MjIzMjI4NDgsImp0aSI6IjVmNzIwZjY5ODcyMTRmNWI4MjVjMmUzMjAzZjIxZGNhIiwidWlkIjoiNjYxMTgxYjBlMmI3ZTk4MDIzMWEzZDU1IiwidHlwZSI6InJlZnJlc2gifQ.vxnT4MkZ7f4cF2IOX-KMEFfIuQbVUEAXF_Lwmfuxq1M
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyY2ExYzBjMGE2MDE0YTBiYmI4MjkwNzI5OWU4MDEwZiIsImV4cCI6MTczNzg3NTA1MSwibmJmIjoxNzIyMzIzMDUxLCJpYXQiOjE3MjIzMjMwNTEsImp0aSI6IjNkNzI4YjJlNjdmYzRlYjY4ZjY4ZmE3NzhlMmZmZTFmIiwidWlkIjoiNjYyOTBlN2M3NmUxZGRmNjBhOTkzZWM0IiwidHlwZSI6InJlZnJlc2gifQ.RXxqocEHQ0Qj4JSxFEUtbEhXgQgn5zPAcPlmR4If64M
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwZWEyNjNmMmM1NTE0MDJhYTNlODRiYzY2YjAyZWEzMCIsImV4cCI6MTczNzg3NjMyNCwibmJmIjoxNzIyMzI0MzI0LCJpYXQiOjE3MjIzMjQzMjQsImp0aSI6ImJlNDk3YmFjMDdiOTQzMTNiZWQyNDhmNDE3YWExNTM1IiwidWlkIjoiNjYxMTg3MDYyYWJlNzU2YmVkMzE1MTZkIiwidHlwZSI6InJlZnJlc2gifQ.Ux7Jw_OOI10uNq8Ag2Jhasg8QrBUmNRxPLAvzrzMlyE
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyZjMzNzNhZWJiOTY0NWU3ODljMGZlYTk0NjYwZGM5NSIsImV4cCI6MTczNzg3NjQ1MSwibmJmIjoxNzIyMzI0NDUxLCJpYXQiOjE3MjIzMjQ0NTEsImp0aSI6ImI5MjllMTU3NWFkZTQyYmFhYWY3YTZmZjc2NmRhYWJlIiwidWlkIjoiNjYyOTE4YWZkZjU3YmEyNjIxMzk5OTAzIiwidHlwZSI6InJlZnJlc2gifQ.a98sfwbsgzNRGT2QOa1tqTFzBzFn33EfPLSGPpoEbNE
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOTg4MWY5YzJjMzI0MDA5YWQ2ZjZmNjFjOTdjYTZhNSIsImV4cCI6MTczNzg3NjYzNCwibmJmIjoxNzIyMzI0NjM0LCJpYXQiOjE3MjIzMjQ2MzQsImp0aSI6ImQ3YzA1YzQ0MTdmYjQwYzA5MWNmNDc1OTU4ZTJlZDRkIiwidWlkIjoiNjYxMTg4YTRhYmMwZjE5YjdkMjdlZDI4IiwidHlwZSI6InJlZnJlc2gifQ.aaWjrCrD76zZo5idLs6Nt6W4v5sE0npduEsFyvOkIyg
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMjQ4MTk4ZWQ4OTg0NmZhYjI3ZjE0ZTkxMzBjYWNmMiIsImV4cCI6MTczNzg3Njc3NiwibmJmIjoxNzIyMzI0Nzc2LCJpYXQiOjE3MjIzMjQ3NzYsImp0aSI6IjNlYmZjNDZhOTg2NDQyN2Y5N2U0MDcwOGI0M2E2ZjM2IiwidWlkIjoiNjYxMTg1Yjg1NGIwOTE2NjFjMDcwNTcwIiwidHlwZSI6InJlZnJlc2gifQ.yibRRGus5VSxfjbfZy4ZZN4jhiT1Q8cRXI5xZyeWpOI
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkNmE4N2E1NjA1NjE0MmQyYTBiN2ViMWIxMDgzMTU1MiIsImV4cCI6MTczNzg3NjgzNSwibmJmIjoxNzIyMzI0ODM1LCJpYXQiOjE3MjIzMjQ4MzUsImp0aSI6Ijg3ZDdkNmE1MTFiYzQ1NTE4MTUyMTkxZDdiMDdkYTkzIiwidWlkIjoiNjYyOTBkZDFhNmQ5YWZlM2U2ZjFjMDg2IiwidHlwZSI6InJlZnJlc2gifQ.MRuqTE0ID5oPZ9887UoxRB34dko6UygHSBXRKmc1O4Y
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NmRlNWZjMTcwMGU0MTgwOWNiMTc1MDg0ZGVlYzNkZSIsImV4cCI6MTczNzg3NjkwNywibmJmIjoxNzIyMzI0OTA3LCJpYXQiOjE3MjIzMjQ5MDcsImp0aSI6ImFkNGJjMGNhMjQ4MjQ3ODFiN2RkMThjNjUwZDE1NmQ1IiwidWlkIjoiNjZhODk3YWFkMjc3ZDM1NjczZmJkMGJkIiwidHlwZSI6InJlZnJlc2gifQ.BzRKk05ugkbar0gdJWiB5F4-kx3QIpllZPLE0JpzwMQ
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDdlZDVkMDhlY2M0YzFmOGQ1NGU4OGQyMzVmMDYxZCIsImV4cCI6MTczNzg3NzYwNiwibmJmIjoxNzIyMzI1NjA2LCJpYXQiOjE3MjIzMjU2MDYsImp0aSI6ImQxNGNkZTk1ODg2NTRjZjJhZmMzMTYyYzhkOGU3YWZhIiwidWlkIjoiNjYxMTdjNGI1NGIwOTE2NjFjMDZmZWFlIiwidHlwZSI6InJlZnJlc2gifQ.4puphxxCPi5zXIsb1CxuuoJthILYgs9b31Hacq5BePg"""
#     for i in tokens.split():
#         b = arun(check_token(i))
#         if not b:
#             print(i)
