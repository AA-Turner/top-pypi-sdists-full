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
from meutils.io.files_utils import to_url
from meutils.schemas.jimeng_types import VideoRequest, ImageRequest

from volcengine.visual.VisualService import VisualService


def create_task(request: Union[ImageRequest, VideoRequest], token: Optional[str] = None):
    visual_service = VisualService()

    if token:
        ak, sk = token.split('|')
        visual_service.set_ak(ak)
        visual_service.set_sk(sk)

    # request
    payload = request.model_dump(exclude_none=True)

    response = visual_service.cv_submit_task(payload)
    return response


if __name__ == '__main__':
    token = f"""{os.getenv("VOLC_ACCESSKEY")}|{os.getenv("VOLC_SECRETKEY")}"""
    prompt = """
    3D魔童哪吒 c4d 搬砖 很开心， 很快乐， 精神抖擞， 背景是数不清的敖丙虚化 视觉冲击力强 大师构图 色彩鲜艳丰富 吸引人 背景用黄金色艺术字写着“搬砖挣钱” 冷暖色对比
    """

    request = ImageRequest(
        prompt=prompt,
    )

    request = VideoRequest(
        prompt=prompt
    )



    print(create_task(request, token))
