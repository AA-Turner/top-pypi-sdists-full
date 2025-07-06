#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/4/18 08:55
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""
https://www.volcengine.com/docs/85128/1526761
Seedream 通用3.0文生图模型是基于字节跳动视觉大模型打造的新一代文生图模型，本次升级模型综合能力（图文，结构，美感）均显著提升。V3.0参数量更大，对语义有更好的理解，实体结构也更加自然真实，支持 2048 以下分辨率直出，各类场景下的效果均大幅提升。
https://www.volcengine.com/docs/6791/1384311
"""
import os

from meutils.pipe import *
from meutils.caches import rcache

from meutils.decorators.retry import retrying
from meutils.db.redis_db import redis_aclient
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.schemas.jimeng_types import VideoRequest, ImageRequest

from volcengine.visual.VisualService import VisualService
from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request, HTTPException, status, BackgroundTasks

FEISHU = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=OiHxsE"


#  and "Access Denied" not in str(r)

@retrying(max_retries=5, predicate=lambda r: "Concurrent Limit" in str(r))  # 限流
async def create_task(request: Union[ImageRequest, VideoRequest, dict], token: Optional[str] = None):
    """https://www.volcengine.com/docs/6791/1399614"""
    token = token or await get_next_token_for_polling(FEISHU)

    logger.debug(token)

    visual_service = VisualService()

    if token:
        ak, sk = token.split('|')
        visual_service.set_ak(ak)
        visual_service.set_sk(sk)

    # request
    if not isinstance(request, dict):
        request = request.model_dump(exclude_none=True)

    response = visual_service.cv_sync2async_submit_task(request)  # 同步转异步

    """
    {'code': 10000,
 'data': {'task_id': '15106285208671192523'},
 'message': 'Success',
 'request_id': '202505291707517FC0D2B135CEE77BC4A5',
 'status': 10000,
 'time_elapsed': '150.967328ms'}
    """

    logger.debug(response)
    if response.get('code') == 10000:
        await redis_aclient.set(response['data']['task_id'], token, ex=7 * 24 * 3600)
    else:
        raise Exception(response)

    return response


#
# @retrying(max_retries=5, predicate=lambda r: "Concurrent Limit" in str(r))  # 限流
# @rcache(ttl=5)
async def get_task(request: dict):
    task_id = request.get("task_id", "")
    token = await redis_aclient.get(task_id)  # 绑定对应的 token
    token = token and token.decode()
    if not token:
        raise HTTPException(status_code=404, detail="TaskID not found")

    visual_service = VisualService()

    if token:
        ak, sk = token.split('|')
        visual_service.set_ak(ak)
        visual_service.set_sk(sk)

    response = visual_service.cv_get_result(request)  # 同步转异步

    logger.debug(response)

    return response


if __name__ == '__main__':
    token = f"""{os.getenv("VOLC_ACCESSKEY")}|{os.getenv("VOLC_SECRETKEY")}"""
    token = "AKLTOWM5ZTc5ZDFhZWNlNDIzODkwYmZiNjEyNzYwNzE0MTI|T0RCbFpHRTJaRFEyWmpjeE5ERXpNR0ptWlRCaU16WmhPRE0wWVdKa01tTQ=="
    prompt = """
    3D魔童哪吒 c4d 搬砖 很开心， 很快乐， 精神抖擞， 背景是数不清的敖丙虚化 视觉冲击力强 大师构图 色彩鲜艳丰富 吸引人 背景用黄金色艺术字写着“搬砖挣钱” 冷暖色对比
    """

    request = ImageRequest(
        req_key="high_aes_general_v30l_zt2i",
        prompt=prompt,
    )

    # request = VideoRequest(
    #     prompt=prompt
    # )

    # arun(create_task(request, token))
    # arun(create_task(request))

    # request = {
    #     "task_id": "141543714223689974",
    #     "req_key": "high_aes_general_v30l_zt2i"
    # }
    # #
    # arun(get_task(request))

    print(bjson(request))

    # {
    #     "req_key": "high_aes_general_v30l_zt2i",
    #     "prompt": "\n    3D魔童哪吒 c4d 搬砖 很开心， 很快乐， 精神抖擞， 背景是数不清的敖丙虚化 视觉冲击力强 大师构图 色彩鲜艳丰富 吸引人 背景用黄金色艺术字写着“搬砖挣钱” 冷暖色对比\n    ",
    #     "seed": -1,
    #     "width": 512,
    #     "height": 512,
    #     "use_pre_llm": true,
    #     "use_sr": false,
    #     "return_url": true,
    #     "logo_info": null
    # }