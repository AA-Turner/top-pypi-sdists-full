#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/10/22 11:10
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import httpx

from meutils.pipe import *
from meutils.caches import rcache
from meutils.llm.clients import AsyncClient
from meutils.decorators.retry import retrying, IgnoredRetryException

from meutils.llm.openai_utils import to_openai_params
from meutils.io.files_utils import to_png, to_url_fal, to_url
from meutils.notice.feishu import send_message_for_images
from meutils.schemas.image_types import ImageRequest, ImagesResponse

base_url = "https://api.freepik.com"

"""FPSXc7a13cdcd4893ff3aa053749d05485a7
 curl --request POST \
  --url https://api.freepik.com/v1/ai/gemini-2-5-flash-image-preview \
  --header 'Content-Type: application/json' \
  --header 'x-freepik-api-key: FPSX3e216c84cc281f6f0f5f605334e22ad0' \
  --data '{
  "prompt": "A cat",
  "webhook_url": "https://openai-dev.chatfire.cn/sys/webhook/freepik"
}'


curl --request GET \
  --url https://api.freepik.com/v1/ai/gemini-2-5-flash-image-preview/0ef796f9-1efe-421a-935b-f1dfb4a3cb32 \
  --header 'x-freepik-api-key: FPSX3e216c84cc281f6f0f5f605334e22ad0'
"""


async def generate(request: ImageRequest, api_key: Optional[str] = None, base_url: Optional[str] = None):
    task_id = await create_task(request, api_key)

    for i in tqdm(range(20)):
        if data := await get_task(task_id, api_key, request):
            return data

        await asyncio.sleep(3)


@retrying(ignored_exception_types=IgnoredRetryException)
async def get_task(task_id, api_key, request: ImageRequest):
    headers = {"x-freepik-api-key": api_key}
    client = AsyncClient(api_key=api_key, base_url=base_url, default_headers=headers)

    response = await client.get(f"/v1/ai/{request.model}/{task_id}", cast_to=object)

    logger.debug(bjson(response))

    if (data := response.get("data")) and (images := data.get("generated")):
        return ImagesResponse(image=images)
    elif data.get("status") == "FAILED":
        raise IgnoredRetryException(data)

    """
    {
    "code": 200,
    "result": {
        "task_id": "ddnxnz9cyhyr67vpd4",
        "user_id": 10061,
        "version": "44b9310748ecdccd1dfa60d68efe35b4a6291453d5edfad417075890d55a208f",
        "error": "The input or output was flagged as sensitive. Please try again with different inputs. (E005) (uIJ6l3ruRD)", #####
        "total_time": 5.0,
        "predict_time": null,
        "logs": null,
        "output": [],
        "status": "failed",
        "create_at": null,
        "completed_at": null
    },
    "message": {}
    }

    """


@rcache(ttl=3600)
async def create_task(request: ImageRequest, api_key: Optional[str] = None):
    headers = {"x-freepik-api-key": api_key}
    payload = {
        "prompt": request.prompt,
        "reference_images": request.image_urls,
    }

    client = AsyncClient(api_key=api_key, base_url=base_url, default_headers=headers)

    response = await client.post(
        f"/v1/ai/{request.model}",
        body=payload,
        cast_to=object
    )

    # async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=30) as client:
    #     response = await client.post(f"/v1/ai/{request.model}", json=payload)
    #     response.raise_for_status()
    #     response = response.json()

    logger.debug(bjson(response))

    if task_id := (response.get("data") or {}).get("task_id"):
        return task_id

    raise Exception(f"Create Task Failed: {response}")


if __name__ == '__main__':
    api_key = "FPSXc7a13cdcd4893ff3aa053749d05485a7"
    model = "gemini-2-5-flash-image-preview"

    request = ImageRequest(
        model=model,
        prompt="带个墨镜    ",
        image=["https://s3.ffire.cc/files/jimeng.jpg"],
    )

    # arun(create_task(request, api_key))
    #
    # arun(get_task('bb8c92f1-5af6-420b-a6b7-56d8f4b70faa', api_key, request))

    arun(generate(request, api_key))
