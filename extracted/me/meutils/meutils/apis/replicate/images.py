#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2025/11/18 16:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo black-forest-labs/flux-1.1-pro-ultra
# https://replicate.com/black-forest-labs/flux-1.1-pro-ultra/api

from meutils.pipe import *
from meutils.schemas.image_types import ImageRequest, ImagesResponse
from meutils.apis.translator import deeplx

import replicate


async def generate(request: ImageRequest, api_key: str = None, base_url: str = None):
    usage = None

    api_key = api_key or os.getenv("REPLICATE_API_KEY")
    client = replicate.client.Client(api_token=api_key)

    payload = {
        "prompt": request.prompt,
        "aspect_ratio": request.aspect_ratio or "match_input_image" if request.image_urls else request.aspect_ratio or "1:1",
        "output_format": request.output_format or "png",
    }
    if request.resolution:
        payload["resolution"] = request.resolution

    if 'z-image' in request.model:
        if request.size:
            payload['width'], payload['height'] = map(int, request.size.split('x'))

        payload['guidance_scale'] = request.guidance or 0
        payload['num_inference_steps'] = request.steps or 8

    elif request.model.startswith(("google/nano-banana",)):
        payload["image_input"] = request.image_urls

    elif request.model.startswith("black-forest-labs/flux-2"):
        payload["go_fast"] = True
        payload["safety_tolerance"] = request.safety_tolerance or 5
        payload["input_images"] = request.image_urls
        if request.resolution:  # pro
            payload["resolution"] = request.resolution.replace('k', ' MP')

        usage = request.usage


    elif request.model.startswith(("flux-kontext",)):
        payload["prompt"] = await deeplx.llm_translate(request.prompt)

        if request.model.endswith("-max"):
            request.model = "black-forest-labs/flux-kontext-max"
        else:
            request.model = "black-forest-labs/flux-kontext-pro"

        if len(request.image_urls) == 1:
            request.model = "black-forest-labs/flux-kontext-dev"  ##########
            payload["input_image"] = request.image_urls[0]

        elif len(request.image_urls) > 1:
            request.model = request.model.replace("black-forest-labs/flux-", "flux-kontext-apps/multi-image-")

            payload["input_image_1"] = request.image_urls[0]
            payload["input_image_2"] = request.image_urls[1]
            # payload["input_image_1"], payload["input_image_2"], *_ = request.image_urls

    logger.debug(request.model)
    logger.debug(bjson(payload))

    output = await client.async_run(
        request.model,
        input=payload
    )

    return ImagesResponse(image=output.url, usage=usage)
    #
    # for i in range(2):
    #     try:
    #         output = await client.async_run(
    #             request.model,
    #             input=payload
    #         )
    #
    #         return ImagesResponse(image=output.url)
    #     except Exception as e:
    #         logger.error(e)
    #         if "Width * Height must be" in str(e):
    #             payload.pop("aspect_ratio", None)


#
# output = client.async_run(
#     "flux-kontext-apps/multi-image-kontext-pro",
#     input={
#         "prompt": "Put the woman next to the house",
#         "aspect_ratio": "match_input_image",
#         "input_image_1": "https://replicate.delivery/pbxt/N7gRAUNcVF6HarL0hdAQA2JYNMlJD52LP1wyaIWRUXWeHzqT/0_1-1.webp",
#         "input_image_2": "https://replicate.delivery/pbxt/N7gRAK5kbPwdsbOpqgyAIOFQX45U6suTlbL6ws2N74SnGFpo/test.jpg",
#         "output_format": "png",
#         "safety_tolerance": 2
#     }
# )

# To access the file URL:
# print(output.url)
# => "http://example.com"

if __name__ == '__main__':
    # image_request = ImageRequest(
    #     prompt="Put the woman next to the house",
    #     aspect_ratio="match_input_image",
    #     input_image_1="https://replicate.delivery/pbxt/N7gRAUNcVF6HarL0hdAQA2JYNMlJD52LP1wyaIWRUXWeHzqT/0_1-1.webp",
    #     input_image_2="https://replicate.delivery/pbxt/N7gRAK5kbPwdsbOpqgyAIOFQX45U6suTlbL6ws2N74SnGFpo/test.jpg",
    #     output_format="png",
    #     safety_tolerance=2
    # )

    # arun(output)
    model = "flux-kontext-max"
    #     model = "flux-kontext-apps/multi-image-kontext-pro"
    #     model = "flux-kontext-pro"
    #     model = "google/imagen-3"
    #     model = "google/imagen-4"
    #     model = "black-forest-labs/flux-1.1-pro-ultra"
    #     model = "black-forest-labs/flux-2-dev"
    #     model = "black-forest-labs/flux-2-pro"
    #     model = "black-forest-labs/flux-2-pro_4k"
    #     model = "prunaai/z-image-turbo:7ea16386290ff5977c7812e66e462d7ec3954d8e007a8cd18ded3e7d41f5d7cf"
    prompt = """
    手机原相机实拍，无滤镜无修图，33岁素颜少妇(自然皮肤纹理、原生眉形、淡淡唇色，无妆容痕迹)，身材火辣傲人，上围饱满。穿着黑丝透明丝袜，姿态性感又慵懒。表情自然。
穿搭居家性感。随机正在进行式动作。辅导一个18岁女孩作业。
随机家庭日常场景。(自然光，无刻意补光)，轻微过曝，画面颗粒感，随机镜头。构图随意自然，毫无修饰感。 远景/中景。突出生活化抓拍感。时尚摄影。比例 9:16。
    """

    # model = "google/nano-banana-pro_4K"

    request = ImageRequest(
        model=model,
        # prompt="Put the woman next to the house",
        # prompt="一个裸体女人",
        # prompt='带个墨镜',
        prompt=prompt,
        size="2048x2048",

        # aspect_ratio="match_input_image",
        # input_image_1="https://replicate.delivery/pbxt/N7gRAUNcVF6HarL0hdAQA2JYNMlJD52LP1wyaIWRUXWeHzqT/0_1-1.webp",
        # input_image_2="https://replicate.delivery/pbxt/N7gRAK5kbPwdsbOpqgyAIOFQX45U6suTlbL6ws2N74SnGFpo/test.jpg",
        # image="https://s3.ffire.cc/files/jimeng.jpg",
        # image="https://replicate.delivery/pbxt/N7gRAUNcVF6HarL0hdAQA2JYNMlJD52LP1wyaIWRUXWeHzqT/0_1-1.webp"
    )
    print(request)

    arun(generate(request))
