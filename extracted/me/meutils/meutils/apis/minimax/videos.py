#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/8/8 17:32
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""

2x08hnrb@yyu.hdernm.com----uc7jqzax----eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJhYXZ5IHJ5ZGgiLCJVc2VyTmFtZSI6ImFhdnkgcnlkaCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxOTI0MzY5NjUwMjE3MzkwNDMyIiwiUGhvbmUiOiIiLCJHcm91cElEIjoiMTkyNDM2OTY1MDIwOTAwMTgyNCIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6IjJ4MDhobnJiQHl5dS5oZGVybm0uY29tIiwiQ3JlYXRlVGltZSI6IjIwMjUtMDUtMTkgMTY6MzY6MzMiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.ZQ_cSiErTQNHT37w8Ie2nIy4zLfmo0sBXbuIQd0uEU_HDyLn4WBrJ6O-CAnWldtxi9PY53YHZW6zTb33S9zDx4VcXVRO3Nxl5o2WQNYRj3KxxNtHWAGwtA-cCplmgY71m-Xe4kZtN-K25tgXVcWbdze4nev_OGdkDPHBxfhiP462P0wgQ_tqkl5BgTxgUhcskYNs6JogNQUP4c1LFoSR6vYoAYek95K199ehpBuE1jkLFa2JDzNlKlVq_e2LPZkwA7qW67Ih0yONFDEtvM5GXr9ZMjyFIhww4hIeYPGTpqwHnjY00GUzlh4F9e_gpsx-FLqxZn0Xfnhyz8YvUDidfQ

"""

from meutils.pipe import *
from meutils.caches import rcache
from meutils.db.redis_db import redis_aclient

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.apis.utils import make_request_httpx

base_url = "https://api.minimax.io/v1"
feishu_url = "https://xchatllm.feishu.cn/sheets/Z59Js10DbhT8wdt72LachSDlnlf?sheet=oOK2uj"


@rcache(ttl=300)
async def create_task(request: dict, api_key: Optional[str] = None):
    api_key = api_key or await get_next_token_for_polling(feishu_url)

    headers = {"Authorization": f"Bearer {api_key}"}
    path = "/video_generation"
    payload = request

    response = await make_request_httpx(
        base_url=base_url,
        headers=headers,

        path=path,
        payload=payload,
    )
    if task_id := response.get("task_id"):
        await redis_aclient.set(task_id, api_key, ex=7 * 24 * 3600)

    logger.debug(response)
    return response


@alru_cache(ttl=30)
async def get_task(task_id: str):
    token = await redis_aclient.get(task_id)  # 绑定对应的 token
    api_key = token and token.decode()

    headers = {"Authorization": f"Bearer {api_key}"}
    path = f"/query/video_generation?task_id={task_id}"

    response = await make_request_httpx(
        base_url=base_url,
        headers=headers,

        path=path
    )
    if file_id := response.get("file_id"):
        await redis_aclient.set(file_id, api_key, ex=7 * 24 * 3600)

    return response


@alru_cache(ttl=30)
async def get_file(file_id: str):
    token = await redis_aclient.get(file_id)  # 绑定对应的 token
    api_key = token and token.decode()

    headers = {"Authorization": f"Bearer {api_key}"}
    path = f"/files/retrieve?file_id={file_id}"

    response = await make_request_httpx(
        base_url=base_url,
        headers=headers,

        path=path
    )
    """
    {'file': {'file_id': 299393334087796,
  'bytes': 0,
  'created_at': 1754647084,
  'filename': 'output.mp4',
  'purpose': 'video_generation',
  'download_url': 'https://public-cdn-video-data-algeng.oss-cn-wulanchabu.aliyuncs.com/inference_output%2Fvideo%2F2025-08-08%2F5caadc3e-b812-4df2-8153-fa463d7ebab3%2Foutput.mp4?Expires=1754679844&OSSAccessKeyId=LTAI5tAmwsjSaaZVA6cEFAUu&Signature=%2FxSqhj1bI9MY%2FlS8SNrSJWphNTI%3D',
  'backup_download_url': 'https://public-cdn-video-data-algeng-us.oss-us-east-1.aliyuncs.com/inference_output%2Fvideo%2F2025-08-08%2F5caadc3e-b812-4df2-8153-fa463d7ebab3%2Foutput.mp4?Expires=1754679844&OSSAccessKeyId=LTAI5tCpJNKCf5EkQHSuL9xg&Signature=PPvLDVrhqzt%2FXi%2BaBvZRFAr1IEI%3D'},
 'base_resp': {'status_code': 0, 'status_msg': 'success'}}

    """
    return response


if __name__ == '__main__':
    data = {
        "model": "T2V-01",
        "prompt": "男子拿起一本书[上升]，然后阅读[固定]。",
        "duration": 6,
        "resolution": "1080P"
    }  # 299392563388531

    token = """eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJhYXZ5IHJ5ZGgiLCJVc2VyTmFtZSI6ImFhdnkgcnlkaCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxOTI0MzY5NjUwMjE3MzkwNDMyIiwiUGhvbmUiOiIiLCJHcm91cElEIjoiMTkyNDM2OTY1MDIwOTAwMTgyNCIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6IjJ4MDhobnJiQHl5dS5oZGVybm0uY29tIiwiQ3JlYXRlVGltZSI6IjIwMjUtMDUtMTkgMTY6MzY6MzMiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.ZQ_cSiErTQNHT37w8Ie2nIy4zLfmo0sBXbuIQd0uEU_HDyLn4WBrJ6O-CAnWldtxi9PY53YHZW6zTb33S9zDx4VcXVRO3Nxl5o2WQNYRj3KxxNtHWAGwtA-cCplmgY71m-Xe4kZtN-K25tgXVcWbdze4nev_OGdkDPHBxfhiP462P0wgQ_tqkl5BgTxgUhcskYNs6JogNQUP4c1LFoSR6vYoAYek95K199ehpBuE1jkLFa2JDzNlKlVq_e2LPZkwA7qW67Ih0yONFDEtvM5GXr9ZMjyFIhww4hIeYPGTpqwHnjY00GUzlh4F9e_gpsx-FLqxZn0Xfnhyz8YvUDidfQ"""

    arun(
        create_task(data, api_key=token)
    )

    # arun(
    #     get_task('299392563388531')
    # )

    # arun(
    #     get_file('299393334087796')
    # )
