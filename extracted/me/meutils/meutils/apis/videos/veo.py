#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/6/18 16:34
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.db.redis_db import redis_aclient
from meutils.apis.utils import make_request
from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request, HTTPException, status, BackgroundTasks

base_url = "https://api.gptgod.online"


async def create_task(
        request: dict,
        api_key: Optional[str] = None
):
    response = await make_request(
        base_url=base_url,
        api_key=api_key,
        path="/v1/video/create",
        payload=request,
    )

    if task_id := response.get('id'):
        await redis_aclient.set(task_id, api_key, ex=7 * 24 * 3600)

    return response


async def get_task(task_id: str):
    token = await redis_aclient.get(task_id)  # 绑定对应的 token
    token = token and token.decode()
    if not token:
        raise HTTPException(status_code=404, detail="TaskID not found")

    response = await make_request(
        base_url=base_url,
        api_key=token,
        path=f"/v1/video/query?id={task_id}",
        method="GET",
    )
    return response


if __name__ == '__main__':
    api_key = "sk-h0Cgw9qeyotIUC9WnWSBEB0aO4RbjgEbhZmtg2Ja0kL5npDZ1"
    payload = {
        "prompt": "牛飞上天了",
        "model": "veo3",
        "images": [
            "https://filesystem.site/cdn/20250612/VfgB5ubjInVt8sG6rzMppxnu7gEfde.png",
            "https://filesystem.site/cdn/20250612/998IGmUiM2koBGZM3UnZeImbPBNIUL.png"
        ],
        "enhance_prompt": True
    }

    # arun(create_task(payload, api_key))

    arun(get_task("veo3:2ba161ec-747f-4d5b-b58b-2a610bfc2c31"))



