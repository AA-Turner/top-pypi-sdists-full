#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : generations
# @Time         : 2025/6/11 17:06
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 统一收口 todo 硅基

from meutils.pipe import *
from meutils.apis.utils import create_http_client
from meutils.llm.clients import AsyncClient
from meutils.llm.openai_utils import to_openai_params
from meutils.io.files_utils import to_url_fal, to_url
from meutils.notice.feishu import send_message_for_images

from meutils.schemas.image_types import ImageRequest, RecraftImageRequest, ImagesResponse

from meutils.apis.fal.images import generate as fal_generate

from meutils.apis.gitee.image_to_3d import generate as image_to_3d_generate
from meutils.apis.gitee.openai_images import generate as gitee_images_generate
from meutils.apis.volcengine_apis.images import generate as volc_generate
from meutils.apis.images.recraft import generate as recraft_generate
from meutils.apis.jimeng.images import generate as jimeng_generate
# from meutils.apis.google.images import generate as google_generate

from meutils.apis.qwen.chat import Completions as QwenCompletions
from meutils.apis.google.chat import Completions as GoogleCompletions
from meutils.apis.google.images import openai_generate
from meutils.apis.ppio.images import generate as ppio_generate
from meutils.apis.runware.images import generate as runware_generate
from meutils.apis.vmodel.images import generate as vmodel_generate
from meutils.apis.freepik.images import generate as freepik_generate
from meutils.apis.siliconflow.images_pro import generate as siliconflow_generate
from meutils.apis.replicate.images import generate as replicate_generate
from meutils.apis.aiml.images import generate as aiml_generate
from meutils.apis.modelscope_api.images import generate as modelscope_generate
from meutils.apis.netmind.images import generate as netmind_generate
from meutils.apis.hailuoai.openai_images import generate as hailuo_generate
# 工具类
from meutils.apis.textin_apis import Textin
from meutils.apis.images.edits import edit_image as baidu_generate


async def generate(
        request: ImageRequest,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        http_url: Optional[Any] = None,
):
    if len(str(request)) < 1024: logger.debug(request)

    base_url = base_url or ""

    if 'hailuo' in base_url:
        return await hailuo_generate(request, api_key)

    if 'baidu' in base_url:
        return await baidu_generate(request)

    if 'gitee' in base_url:  # textin todo apikey
        # return await Textin(api_key).image_watermark_remove(request)
        return await Textin().image_watermark_remove(request)

    if 'textin' in base_url:  # textin todo apikey
        # return await Textin(api_key).image_watermark_remove(request)
        return await Textin().image_watermark_remove(request)

    if "netmind" in base_url:  # modelscope
        return await netmind_generate(request, api_key)

    if "modelscope" in base_url:  # modelscope
        return await modelscope_generate(request, api_key)

    if 'v1beta' in base_url:  # google
        request.prompt = f"According my description, output image:\n\n {request.prompt}"
        return await GoogleCompletions(base_url=base_url, api_key=api_key).generate(request)  # 原生接口

    if "aimlapi" in base_url:  # aiml
        return await aiml_generate(request, api_key)

    if any(i in base_url for i in {"cherry", "siliconflow"}):  # 硅基
        return await siliconflow_generate(request, api_key, base_url)

    if "replicate" in base_url:  # 硅基
        return await replicate_generate(request, api_key, base_url)

    if api_key and api_key.startswith("FPS"):  # freepik
        return await freepik_generate(request, api_key)

    if len(request.model) == 64 and request.model.islower():  # 粗糙
        return await vmodel_generate(request, api_key)

    if request.model.startswith("fal-ai"):  # 国外fal
        request.image = await to_url_fal(request.image, content_type="image/png")
        response = await fal_generate(request, api_key)

        # https://fal.media/files/panda/FlN5Gk0KnHe4AXU6Jeyvo_c5795dc52214423cb6465dae8eeaa1f0.png
        # https://s3ai.cn/fal/files/panda/FlN5Gk0KnHe4AXU6Jeyvo_c5795dc52214423cb6465dae8eeaa1f0.png

        # """https://fal.media/files/b/rabbit/-Cvx3pnaB0p6p_RLXlfuo.png
        # """
        # 转存
        # if response.data and request.response_format == "oss_url":
        #     urls = [dict(image_data).get("url") for image_data in response.data]
        #     urls = await to_url(urls, filename=f"{shortuuid.random()}.png")
        #
        #     response.data = [{"url": url} for url in urls]
        #
        #     return response

        if response.data and request.response_format == "oss_url":
            urls = [
                f"""https://s3ai.cn/fal/files/panda/{Path(dict(image_data).get("url", "")).name}"""

                for image_data in response.data
            ]

            response.data = [{"url": url} for url in urls] + response.data

        send_message_for_images(response.data, title=__file__)

        return response

    if request.model.startswith(("recraft",)):
        request = RecraftImageRequest(**request.model_dump(exclude_none=True))
        return await recraft_generate(request)

    if request.model.startswith(
            ("jimeng", "seed", "seededit_v3.0", "byteedit_v2.0", "i2i_portrait_photo")):  # seededit seedream
        return await volc_generate(request, api_key)

    if request.model.startswith(("jimeng")):  # 即梦 逆向
        return await jimeng_generate(request)

    if request.model in {"Hunyuan3D-2", "Hi3DGen", "Step1X-3D"}:
        return await image_to_3d_generate(request, api_key)

    if request.model in {"Qwen-Image", "FLUX_1-Krea-dev"} and request.model.endswith(("lora",)):  # todo gitee
        return await gitee_images_generate(request, api_key)

    if request.model.startswith("qwen-image"):
        return await QwenCompletions(api_key=api_key).generate(request)

    if request.model.startswith(("google/gemini", "gemini")):  # openrouter
        if "ppi" in base_url:
            if request.size == "auto":  # 不兼容
                request.size = "1024x1024"

            return await ppio_generate(request, api_key, base_url)

        elif api_key.endswith("-openai"):
            api_key = api_key.removesuffix("-openai")
            request.prompt = f"According my description, output image:\n\n {request.prompt}"
            return await openai_generate(request, base_url=base_url, api_key=api_key)
        else:
            request.prompt = f"According my description, output image:\n\n {request.prompt}"
            return await GoogleCompletions(base_url=base_url, api_key=api_key).generate(request)  # 原生接口

    if request.model.startswith("runware") or all(i in request.model for i in {":", "@"}):
        return await runware_generate(request, api_key)

    # 其他
    data = {
        **request.model_dump(exclude={"extra_fields", "aspect_ratio"}),
        **(request.extra_fields or {})
    }
    request = ImageRequest(**data)
    if request.model.startswith("doubao"):
        base_url = base_url or os.getenv("VOLC_BASE_URL")
        api_key = api_key or os.getenv("VOLC_API_KEY")

        request.stream = False
        request.watermark = False
        if request.model.startswith("doubao-seedream"):

            if request.n > 1:
                request.sequential_image_generation = "auto"
                request.sequential_image_generation_options = {
                    "max_images": min(request.n, 15 - len(request.image_urls))
                }

                request.prompt = f"生成{request.n}张具有关联性的图像，每张图像都应包含核心主题元素，并通过色彩、构图和元素的巧妙组合，形成一个完整的视觉故事\n\n{request.prompt}"
                request.prompt += f" --size {request.size}"
                if str(request.size).lower() not in {"1k", "2k", "4k"}:
                    request.size = "2k"


        elif request.image and isinstance(request.image, list):
            request.image = request.image[0]

        if "ppi" in base_url:  # 派欧 https://ppio.com/docs/models/reference-seedream4.0 images => image
            request.images = request.image

            data = to_openai_params(request)

            client = AsyncClient(api_key=api_key, base_url=base_url)
            try:
                response = await client.images.generate(**data)
            except Exception as e:
                if "Image width range" in str(e):
                    data["size"] = "1K"
                    response = await client.images.generate(**data)
                else:
                    raise e
            if images := response.model_dump(exclude_none=True).get("images"):
                response.data = [{"url": image} for image in images]
                return response
            raise Exception(f"生成图片失败: {response} \n\n{request}")

    data = to_openai_params(request)
    if len(str(data)) < 1024:
        logger.debug(bjson(data))

    client = AsyncClient(
        api_key=api_key,
        base_url=base_url,
        http_client=await create_http_client(http_url)
    )
    response = await client.images.generate(**data)
    return response


# "flux.1-krea-dev"

if __name__ == '__main__':
    # arun(generate(ImageRequest(model="flux", prompt="笑起来")))
    # arun(generate(ImageRequest(model="FLUX_1-Krea-dev", prompt="笑起来")))

    token = f"""{os.getenv("VOLC_ACCESSKEY")}|{os.getenv("VOLC_SECRETKEY")}"""
    # arun(generate(ImageRequest(model="seed", prompt="笑起来"), api_key=token))

    request = ImageRequest(model="doubao-seedream-4-0-250828", prompt="a dog", size="1K")

    request = ImageRequest(
        model="doubao-seedream-4-0-250828",
        prompt="将小鸭子放在t恤上,生成1:2比例图",
        size="1k",
        # image=[
        #     "https://v3.fal.media/files/penguin/XoW0qavfF-ahg-jX4BMyL_image.webp",
        #     "https://v3.fal.media/files/tiger/bml6YA7DWJXOigadvxk75_image.webp"
        # ]
    )

    request = ImageRequest(
        **{"model": "doubao-seedream-4-0-250828", "prompt": "a cat", "n": 2, "size": "1024x1024",
           "response_format": "url"}

    )

    # todo: tokens 4096 1张

    # 组图
    # request = ImageRequest(
    #     model="doubao-seedream-4-0-250828",
    #     prompt="参考这个LOGO，做一套户外运动品牌视觉设计，品牌名称为GREEN，包括包装袋、帽子、纸盒、手环、挂绳等。绿色视觉主色调，趣味、简约现代风格",
    #     image="https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imageToimages.png",
    #     n=3
    # )

    # arun(generate(request, api_key=os.getenv("FFIRE_API_KEY"), base_url=os.getenv("FFIRE_BASE_URL")))  # +"-29494"

    # print(not any(i in str(request.image) for i in {".png", ".jpeg", "image/png", "image/jpeg"}))

    api_key = "sk_fRr6ieXTMfym7Q6cnbj0YBlB1QsE74G8ygqIE2AyGz0"
    base_url = "http://all.chatfire.cn/ppinfra/v1"

    # arun(generate(request, api_key=api_key, base_url=base_url))

    api_key = "FPSXc7a13cdcd4893ff3aa053749d05485a7"
    model = "gemini-2-5-flash-image-preview"

    api_key = os.getenv("SILICONFLOW_API_KEY")
    base_url = 'https://api.siliconflow.cn/v1'
    model = "qwen/qwen-image"

    request = ImageRequest(
        model=model,
        size=None,
        prompt="带个墨镜",
        image=["https://s3.ffire.cc/files/jimeng.jpg"],
    )

    base_url = 'textin'
    model = "textin/watermark-remove"
    request = ImageRequest(
        model=model,
        size=None,
        prompt="带个墨镜",
        image="https://s3.ffire.cc/files/jimeng.jpg",
    )

    base_url = 'baidu'
    model = "baidu/watermark-remove"
    model = "remove-watermark"

    base_url = 'hailuo'
    model = "nano-banana2"

    request = ImageRequest(
        model=model,
        size=None,
        prompt="去水印",
        image="https://s3.ffire.cc/files/jimeng.jpg",
    )
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzIyODE1NzcsInVzZXIiOnsiaWQiOiI0NDQyMjk2MDAzMzA0OTgwNTUiLCJuYW1lIjoibWZ1aiBiamhuIiwiYXZhdGFyIjoiIiwiZGV2aWNlSUQiOiIzMzkxMTQ5Mjg4NjU1Mjk4NjQiLCJpc0Fub255bW91cyI6ZmFsc2V9fQ.__NDyZQQqyYb7TLrumo944EfuCmrbzYngQloNBK4CmM"

    logger.debug(request)

    arun(generate(request, api_key=api_key, base_url=base_url))
