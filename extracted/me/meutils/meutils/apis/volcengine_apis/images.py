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
from meutils.decorators.retry import retrying

from meutils.io.files_utils import to_url
from meutils.schemas.image_types import ImageRequest, ImagesResponse

from volcengine.visual.VisualService import VisualService


@retrying(min=3, max=5)
async def generate(request: ImageRequest, token: Optional[str] = None):
    """

    :param request: byteedit_v2.0 high_aes_general_v30l_zt2i Seedream
    :param token:
    :return:
    """
    visual_service = VisualService()

    if token:
        ak, sk = token.split('|')
        visual_service.set_ak(ak)
        visual_service.set_sk(sk)

    # request byteedit_v2.0 high_aes_general_v30l_zt2i
    payload = {
        "req_key": "high_aes_general_v30l_zt2i",
        # "req_key": "jimeng_high_aes_general_v21_L",

        "prompt": request.prompt,
        "seed": request.seed,
        "width": 1328,
        "height": 1328,
        "return_url": request.response_format == "url",  # 24小时

        # # prompt进行扩写优化
        # "use_pre_llm": True,
        # "use_rephraser": True
    }

    image, prompt = request.image_and_prompt
    width, height = map(int, request.size.split('x'))

    if image:
        payload["image_urls"] = [image]
        payload["req_key"] = "byteedit_v2.0"

    payload['width'] = width
    payload['height'] = height

    if request.response_format == "oss_url":
        payload["return_url"] = False

    response = visual_service.cv_process(payload)
    logger.debug(bjson(response))

    if request.response_format == "b64_json":
        data = [{"b64_json": b64_json} for b64_json in response['data'].get('binary_data_base64', [])]

    elif request.response_format == "oss_url":
        urls = await to_url(response['data'].get('binary_data_base64', []), filename='.png')
        data = [{"url": url} for url in urls]
    else:
        data = [{"url": url.replace(r'\u0026', '&')} for url in response['data'].get('image_urls', [])]

    response['data'].pop("binary_data_base64", None)
    response = ImagesResponse(
        data=data,
        metadata=response
    )

    return response


if __name__ == '__main__':
    token = f"""{os.getenv("VOLC_ACCESSKEY")}|{os.getenv("VOLC_SECRETKEY")}"""
    prompt = """
    3D魔童哪吒 c4d 搬砖 很开心， 很快乐， 精神抖擞， 背景是数不清的敖丙虚化 视觉冲击力强 大师构图 色彩鲜艳丰富 吸引人 背景用黄金色艺术字写着“搬砖挣钱” 冷暖色对比
    """

    prompt = """
    https://oss.ffire.cc/files/kling_watermark.png
    让这个女人带上眼镜 衣服换个颜色
    """

    request = ImageRequest(
        model="high_aes_general_v30l_zt2i",
        prompt=prompt,
        response_format="url",
        size="512x1328",
    )

    arun(generate(request, token=token))

    # with timer():
    #     visual_service = VisualService()
    #     visual_service.set_ak('your ak')  # AKLTZmU5OTA1NTk2MTNmNGQ0MTgxZjQ1NzI0Y2MzYjlhMDQ
    #     visual_service.set_sk('your sk')

    # call below method if you don't set ak and sk in $HOME/.volc/config
    # visual_service.set_ak('your ak') # AKLTZmU5OTA1NTk2MTNmNGQ0MTgxZjQ1NzI0Y2MzYjlhMDQ
    # visual_service.set_sk('your sk')

    # 请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
    # form = {
    #     "req_key": "xxx",
    #     # ...
#     # }
#     "high_aes_scheduler_svr_controlnet_v2.0"
#     prompt = """
# 3D魔童哪吒 c4d 搬砖 很开心， 很快乐， 精神抖擞， 背景是数不清的敖丙虚化 视觉冲击力强 大师构图 色彩鲜艳丰富 吸引人 背景用黄金色艺术字写着“搬砖挣钱” 冷暖色对比
#     """
#     form = {
#         "req_key": "high_aes_general_v30l_zt2i",
#
#         "req_key": "byteedit_v2.0",
#         "prompt": "让这个女人笑起来",
#         "image_urls": ["https://oss.ffire.cc/files/kling_watermark.png"],  # binary_data_base64
#
#         "scale": 0.5,  # [1, 10]
#
#         # "prompt": prompt,
#         # "use_pre_llm": True,  # prompt进行扩写优化
#         # "use_rephraser": True,  # prompt进行扩写优化
#         "seed": -1,
#         # "scale": 2.5,  # [1, 10]
#         "width": 1328,  # [512, 2048]
#         "height": 1328,
#         "return_url": True,  # 24小时
#         # "logo_info": {
#         #     "add_logo": False,
#         #     "position": 0,
#         #     "language": 0,
#         #     "opacity": 0.3,
#         #     "logo_text_content": "这里是明水印内容"
#         # }
#     }
#     with timer():
#         resp = visual_service.cv_process(form)
#         print(resp)
