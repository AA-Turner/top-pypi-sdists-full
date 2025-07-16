#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : edits
# @Time         : 2025/7/9 15:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.apis.utils import make_request_httpx

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=gg5DNy"


async def create_task(image_url: str, api_key: Optional[str] = None):
    # 构造 multipart/form-data
    files = {
        "model": (None, "AnimeSharp"),
        "model_name": (None, "4x-UltraSharp"),
        "outscale": (None, "4"),
        "output_format": (None, "png"),
        "image_url": (None, image_url),
        "response_format": (None, "url")
    }
    headers = {
        "X-Failover-Enabled": "true",
        "Authorization": f"Bearer {api_key}",
        # "Content-Type": "application/x-www-form-urlencoded"
    }
    response = await make_request_httpx(
        base_url="https://ai.gitee.com/v1",
        path="/images/upscaling",
        files=files,  # todo 兼容性
        headers=headers,
        debug=True
    )

    return response


if __name__ == '__main__':
    image = "https://s3.ffire.cc/files/x.jpg"
    api_key = "AHKZ65ARNFH8QGMUUVCPECDTZVOLRPUXIKPGAC1Y"

    arun(create_task(image, api_key))
