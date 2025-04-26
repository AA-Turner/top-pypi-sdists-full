#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2024/12/12 08:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.caches import rcache
from meutils.io.files_utils import to_url, to_url_fal, to_base64
from meutils.llm.check_utils import check_token_for_siliconflow
from meutils.schemas.task_types import TaskResponse
from meutils.schemas.siliconflow_types import FEISHU_URL, FEISHU_URL_FREE, BASE_URL, VideoRequest
from meutils.config_utils.lark_utils import get_next_token_for_polling

from openai import OpenAI, AsyncOpenAI

check_token = partial(check_token_for_siliconflow, threshold=0.01)

MODELS_MAP = {
    "hunyuan-video": "tencent/HunyuanVideo",
    "hunyuanvideo": "tencent/HunyuanVideo",
    "mochi-1-preview": "genmo/mochi-1-preview",
    "ltx-video": "Lightricks/LTX-Video",
}
"""
Wan-AI/Wan2.1-T2V-14B
Wan-AI/Wan2.1-T2V-14B-Turbo

Wan-AI/Wan2.1-I2V-14B-720P
Wan-AI/Wan2.1-I2V-14B-720P-Turbo

16:9 👉 1280×720
9:16 👉 720×1280
1:1 👉 960×960

"""


# @rcache(ttl=0.5 * 24 * 3600, serializer="pickle")
async def create_task(request: VideoRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL_FREE, check_token=check_token, from_redis=True)

    if request.image:
        request.image = await to_base64(request.image)

    if request.model == "Wan-AI/Wan2.1-T2V-14B":
        request.model = "Wan-AI/Wan2.1-T2V-14B-Turbo"

    elif request.model == "Wan-AI/Wan2.1-I2V-14B-720P":
        request.model = "Wan-AI/Wan2.1-I2V-14B-720P-Turbo"

    else:
        request.model = "Wan-AI/Wan2.1-I2V-14B-720P-Turbo" if request.image else "Wan-AI/Wan2.1-T2V-14B-Turbo"

    payload = request.model_dump(exclude_none=True)

    logger.debug(payload)

    client = AsyncOpenAI(
        base_url=BASE_URL,
        api_key=token
    )

    response = await client.post("/video/submit", body=payload, cast_to=object)
    task_id = response.get('requestId')

    return TaskResponse(task_id=task_id, system_fingerprint=token)


async def get_task(task_id, token: str):
    client = AsyncOpenAI(
        base_url=BASE_URL,
        api_key=token
    )
    payload = {"requestId": task_id}
    response = await client.post(f"/video/status", cast_to=object, body=payload)
    logger.debug(response)

    data = response.get("results") or {}

    # for video in data.get("videos", []):
    #     video["url"] = await to_url_fal(video.get("url"), content_type="video/mp4")  # 异步执行

    return TaskResponse(
        task_id=task_id,
        data=data,
        status=response.get("status"),
        message=response.get("reason"),
    )


if __name__ == '__main__':
    token = None
    token = "sk-raapiguffsnsxgkfiwfusjmbpcyqoxhcohhxaybflrnvpqjw"

    request = VideoRequest(
        model="x",
        prompt="这个女人笑起来 ",
        image='https://oss.ffire.cc/files/kling_watermark.png'  # 1148f2e4-0a62-4208-84de-0bf2c88f740d
    )

    r = arun(create_task(request))

    # tokens_ = arun(check_token_for_siliconflow(tokens, threshold=0.01))

    # arun(create_task(request, token=token))

    # arun(get_task("fa248aac-00ec-4b00-a2f8-3d6bf1cea6d3", token))
    # arun(get_task("c716a328-438e-4612-aff2-a669034499cb", token))
    # arun(get_task("1148f2e4-0a62-4208-84de-0bf2c88f740d", token))

    # token = "sk-oeptckzkhfzeidbtsqvbrvyrfdtyaaehubfwsxjytszbgohd"
    # arun(get_task(r.task_id, r.system_fingerprint))

    # arun(get_task("c6zxjtpsyywj", "sk-lavdsoaybczrfygqdbbqmdgmdktvdztfvwnfmwnbusewjkwb"))

    # arun(create_task(VideoRequest(model="tencent/HunyuanVideo", prompt="a dog in the forest."), token=token))
