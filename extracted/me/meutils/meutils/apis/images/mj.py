#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : mj
# @Time         : 2025/7/25 15:57
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import asyncio
import json

from meutils.pipe import *
from meutils.apis.utils import make_request_httpx, make_request
from meutils.schemas.openai_types import CompletionRequest


async def generate(request: CompletionRequest,
                   api_key: Optional[str] = None):
    response = await make_request(
        base_url='https://api.chatfire.cn',
        path='mj-relax/mj/submit/imagine',
        api_key=api_key,
        method='POST',

        payload={
            "prompt": request.last_user_content,
        }
    )

    yield f"""
> 🖌️正在绘画

```json\n{json.dumps(response, indent=4, ensure_ascii=False)}\n```\n\n

"""

    yield "[PROGRESSING]("

    if task_id := response.get("result"):

        for i in range(100):
            await asyncio.sleep(3)
            yield '🔥'

            response = await make_request(
                base_url='https://api.chatfire.cn',
                path=f'{request.model}/task/{task_id}/fetch',
                api_key=api_key,
                method='GET',
                debug=False
            )
            if response.get("status") == "SUCCESS" and (image_url := response.get("imageUrl")):
                yield '100%)\n\n'
                yield f"![]({image_url})\n\n"

                for i, image_url in enumerate(response.get("imageUrls", []), 1):
                    yield f"""![{i}]({image_url.get("url")})\n\n"""
                break

            if response.get("status", "").lower().startswith(("fail",)):
                yield ')'
                yield f"""```json\n{json.dumps(response, indent=4)}\n```"""
                break
