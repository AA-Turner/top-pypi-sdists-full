#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : lora
# @Time         : 2025/7/15 12:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.io.files_utils import to_bytes, to_url
from meutils.apis.utils import make_request_httpx
from meutils.llm.openai_utils import create_chat_completion, create_chat_completion_chunk
from meutils.llm.openai_utils.billing_utils import get_billing_n, billing_for_async_task, billing_for_tokens
from meutils.schemas.image_types import ImageRequest, ImageEditRequest

base_url = "https://ai.gitee.com/v1"


# /images/edits
async def edit_gitee_ai_image(token: Optional[str] = None):
    token = token or "5PJFN89RSDN8CCR7CRGMKAOWTPTZO6PN4XVZV2FQ"  # 替换为您的 Bearer Token

    # --- 请在这里配置您的参数 ---
    image_path = "/path/to/image.png"  # 替换为您的图片实际路径
    # --------------------------

    headers = {
        "Authorization": f"Bearer {token}",
        # httpx 会自动为 multipart/form-data 设置 Content-Type，无需手动指定
    }

    data = {
        'prompt': "A sunlit indoor lounge area with a pool containing a flamingo",
        'model': "FLUX.1-Kontext-dev",
        'size': "1024x1024",
        'steps': "20",
        'guidance_scale': "2.5",
        'return_image_quality': "80",
        'return_image_format': "PNG",
        'lora_weights': json.dumps(lora_weights_data),  # 将字典转换为 JSON 字符串
        'lora_scale': "1",
    }

    # 构建 multipart 数据
    files = {
        'image': ('image.png', image_content, 'image/png'),
    }

    data = await make_request_httpx(
        base_url=upstream_base_url,
        path=f"/v1/{path}",
        payload=payload,
        params=params,
        data=data,
        files=files,
        headers=headers,

        debug=True

    )


# 运行异步函数
if __name__ == "__main__":
    asyncio.run(edit_gitee_ai_image())
