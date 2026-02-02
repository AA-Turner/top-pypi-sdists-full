#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/12/2 15:34
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *

from openai import AsyncOpenAI
from meutils.llm.openai_utils import to_openai_params
from meutils.schemas.image_types import ImageRequest, ImagesResponse

BASE_URL = 'https://api-inference.modelscope.cn/v1'


async def generate(request: ImageRequest, api_key: Optional[str] = None, base_url: Optional[str] = None, ):
    base_url = base_url or BASE_URL
    api_key = api_key or os.getenv("MODELSCOPE_API_KEY")

    if request.image:
        if 'qwen-image' in request.model.lower():
            if "2509" in request.model:
                request.model = "juyunapi/Qwen-Image-Edit-2509"
            else:
                request.model = "Qwen/Qwen-Image-Edit-2511"

            request.image_url = request.image_urls


    headers = {
        "X-ModelScope-Task-Type": "image_generation",
    }
    data = to_openai_params(request)
    logger.debug(bjson(data))

    client = AsyncOpenAI(base_url=base_url, api_key=api_key, default_headers=headers)

    task_id = None # or "caffccb8-7999-41e7-8222-5dfff9bdaccb"
    for i in range(2):
        try:
            response = await client.images.generate(**data, extra_headers=headers)

            logger.debug(bjson(response))

            if images := response.model_dump().get("images"):
                return ImagesResponse(images=images)
            else:
                task_id = response.model_dump().get("task_id")
                assert task_id, "task_id is None"
        except Exception as e:
            logger.error(e)
            if "submit image generation task error" in str(e):
                headers.update({"X-ModelScope-Async-Mode": "true"})

            if i: raise e

    for i in range(100):
        await asyncio.sleep(3)
        #     "task_id": "caffccb8-7999-41e7-8222-5dfff9bdaccb",

        # result = requests.get(
        #     f"{base_url}/tasks/{task_id}",
        #     headers={"Authorization": f"Bearer {api_key}", "X-ModelScope-Task-Type": "image_generation"},
        # )
        # result.raise_for_status()
        # data = result.json()
        # logger.debug(bjson(data))

        try:
            response = await client.get(
                f"/tasks/{task_id}",
                cast_to=object,
                # cast_to=httpx.Response,

            )
            logger.debug(bjson(response))
            if response["task_status"] == "SUCCEED":  # PENDING PROCESSING
                return ImagesResponse(**response)
            elif response["task_status"] == "FAILED":
                raise Exception("Image Generation Failed.")

        except Exception as e:
            logger.debug(e)


#
# task_id = response.json()["task_id"]
#
# while True:
#     result = requests.get(
#         f"{base_url}v1/tasks/{task_id}",
#         headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
#     )
#     result.raise_for_status()
#     data = result.json()
#
#     if data["task_status"] == "SUCCEED":
#         image = Image.open(BytesIO(requests.get(data["output_images"][0]).content))
#         image.save("result_image.jpg")
#         break
#     elif data["task_status"] == "FAILED":
#         print("Image Generation Failed.")
#         break
#
#     time.sleep(5)


if __name__ == '__main__':
    model = "Tongyi-MAI/Z-Image-Turbo"  # todo size
    # model = "black-forest-labs/FLUX.2-dev"
    # model = "Qwen/Qwen-Image"  # 异步
    # model = "Qwen/Qwen-Image-Edit-2511"
    model = "Qwen/Qwen-Image-2512"
    request = ImageRequest(
        model=model,
        prompt="给图中的狗戴上一个生日帽",
        # size="2048x2048",  # 64,2048

        image="https://modelscope.oss-cn-beijing.aliyuncs.com/Dog.png",
    )
    arun(generate(request))


