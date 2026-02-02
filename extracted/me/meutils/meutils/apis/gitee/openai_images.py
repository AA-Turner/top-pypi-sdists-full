#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/8/11 16:04
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from meutils.db.redis_db import redis_aclient
from meutils.io.files_utils import to_bytes

from meutils.apis.utils import make_request_httpx
from meutils.llm.clients import AsyncClient
from meutils.llm.openai_utils import to_openai_params

from meutils.schemas.gitee_types import FEISHU_URL, BASE_URL
from meutils.schemas.image_types import ImageRequest, ImagesResponse, ImageEditRequest

from meutils.config_utils.lark_utils import get_next_token_for_polling


async def generate(request: ImageRequest, api_key: Optional[str] = None):
    api_key = api_key or os.getenv("GITEE_API_KEY")

    client = AsyncClient(base_url=BASE_URL, api_key=api_key)

    data = {
        **request.model_dump(exclude={"extra_fields", "aspect_ratio"}),
        **(request.extra_fields or {})
    }

    if request.image:
        request.model += "-Edit"
        data["image"] = ('x.png', await to_bytes(request.image), 'image/png')

        data = to_openai_params(ImageEditRequest(**data))

        logger.debug(list(data))

        _ = await client.images.edit(**data)
        logger.debug(_)
        return _

    # logger.debug(bjson(data))

    logger.debug(bjson(data))

    response = await client.images.generate(**data)
    return response


if __name__ == '__main__':
    data = {
        "prompt": "A robot sitting on open grassland, painting on a canvas.",
        "model": "FLUX_1-Krea-dev",
        "size": "1024x576",
        "num_inference_steps": 28,
        "guidance_scale": 4.5,
        "seed": 42
    }
    data = {
        "prompt": "一幅精致细腻的工笔画，画面中心是一株蓬勃生长的红色牡丹，花朵繁茂，既有盛开的硕大花瓣，也有含苞待放的花蕾，层次丰富，色彩艳丽而不失典雅。牡丹枝叶舒展，叶片浓绿饱满，脉络清晰可见，与红花相映成趣。一只蓝紫色蝴蝶仿佛被画中花朵吸引，停驻在画面中央的一朵盛开牡丹上，流连忘返，蝶翼轻展，细节逼真，仿佛随时会随风飞舞。整幅画作笔触工整严谨，色彩浓郁鲜明，展现出中国传统工笔画的精妙与神韵，画面充满生机与灵动之感。",
        "model": "Qwen-Image-lora",
        "size": "1024x1024",
        "num_inference_steps": 30,
        "cfg_scale": 4
    }

    model = "LongCat-Image"
    request = ImageRequest(
        model=model,
        prompt="带个墨镜",
        image="https://s3.ffire.cc/files/jimeng.jpg"
    )
    arun(generate(request))
