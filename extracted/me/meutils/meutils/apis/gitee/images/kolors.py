#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kolors
# @Time         : 2025/1/6 16:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.io.files_utils import to_url_fal, to_base64
from meutils.schemas.image_types import KolorsRequest, ImagesResponse
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.decorators.retry import retrying
from openai import AsyncOpenAI

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/MekfsfVuohfUf1tsWV0cCvTmn3c?sheet=PDnO6X"


@retrying(title=__name__)
async def generate(request: KolorsRequest, token: Optional[str] = None):
    """kolors-1.0
    controls = {"image": 'xxx'}

    """
    token = token or await get_next_token_for_polling(FEISHU_URL)

    if image := request.controls.get('image'):  # 图生图
        image = await to_base64(image)  # url / base64
        # 1152 * 896
        # request.size = "1024x1024"
        payload = {
            "inputs": request.prompt,
            "image": image,

            "width": 896,
            "height": 896,
            "steps": request.steps or 25,
            "guidance_scale": request.guidance or 7.5,

        }
        headers = {"Authorization": f"Bearer {token}", "X-Failover-Enabled": "true", "X-Package": "1910"}
        async with httpx.AsyncClient(headers=headers, timeout=60) as client:
            response = await client.post(
                url="https://ai.gitee.com/api/serverless/Kolors/text-to-image",
                json=payload,
            )
            response.raise_for_status()

            url = None
            b64_json = response.content
            if request.response_format == "url":
                url = await to_url_fal(b64_json, content_type="image/png")
                b64_json = None
            return ImagesResponse(data=[{"url": url, "b64_json": b64_json}])

        # todo; 不知道为啥报错
        # client = AsyncOpenAI(
        #     base_url="https://ai.gitee.com",
        #     api_key=token,
        #     default_headers={"X-Failover-Enabled": "true", "X-Package": "1910"},
        # )
        # response = await client.post(
        #     "/api/serverless/Kolors/text-to-image",
        #     body=payload,
        #     cast_to=object,
        # )
        # return response

    client = AsyncOpenAI(
        base_url="https://ai.gitee.com/v1",
        api_key=token,
        default_headers={"X-Failover-Enabled": "true", "X-Package": "1910"},
    )

    response = await client.images.generate(
        model="Kolors",
        prompt=request.prompt,

        size=request.size,
        extra_body={
            "steps": request.steps or 25,
            "guidance_scale": request.guidance or 7.5,
        },
    )
    if request.response_format == "url":
        url = await to_url_fal(response.data[0].b64_json, content_type="image/png")
        response.data[0].url = url
        response.data[0].b64_json = None

    return response


if __name__ == '__main__':
    request = KolorsRequest(prompt="一个小女孩举着横幅，上面写着“新年快乐”", size="1024x1024", response_format="url")
    request.controls["image"] = "https://oss.ffire.cc/files/kling_watermark.png"

    arun(generate(request))
