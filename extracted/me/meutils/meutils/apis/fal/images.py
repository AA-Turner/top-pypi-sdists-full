#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2024/11/13 15:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://fal.ai/models/fal-ai/flux-pro/v1.1-ultra/api

from meutils.pipe import *
from meutils.str_utils import parse_url, validate_url
from meutils.io.files_utils import to_url, to_url_fal

from meutils.schemas.image_types import ImageRequest, FluxImageRequest, SDImageRequest, ImagesResponse
from meutils.schemas.fal_types import FEISHU_URL
from meutils.config_utils.lark_utils import get_next_token_for_polling, get_series

from meutils.apis.translator import deeplx

from fal_client.client import AsyncClient, SyncClient, Status, FalClientError

recraft_styles = "any, realistic_image, digital_illustration, vector_illustration, realistic_image/b_and_w, realistic_image/hard_flash, realistic_image/hdr, realistic_image/natural_light, realistic_image/studio_portrait, realistic_image/enterprise, realistic_image/motion_blur, realistic_image/evening_light, realistic_image/faded_nostalgia, realistic_image/forest_life, realistic_image/mystic_naturalism, realistic_image/natural_tones, realistic_image/organic_calm, realistic_image/real_life_glow, realistic_image/retro_realism, realistic_image/retro_snapshot, realistic_image/urban_drama, realistic_image/village_realism, realistic_image/warm_folk, digital_illustration/pixel_art, digital_illustration/hand_drawn, digital_illustration/grain, digital_illustration/infantile_sketch, digital_illustration/2d_art_poster, digital_illustration/handmade_3d, digital_illustration/hand_drawn_outline, digital_illustration/engraving_color, digital_illustration/2d_art_poster_2, digital_illustration/antiquarian, digital_illustration/bold_fantasy, digital_illustration/child_book, digital_illustration/child_books, digital_illustration/cover, digital_illustration/crosshatch, digital_illustration/digital_engraving, digital_illustration/expressionism, digital_illustration/freehand_details, digital_illustration/grain_20, digital_illustration/graphic_intensity, digital_illustration/hard_comics, digital_illustration/long_shadow, digital_illustration/modern_folk, digital_illustration/multicolor, digital_illustration/neon_calm, digital_illustration/noir, digital_illustration/nostalgic_pastel, digital_illustration/outline_details, digital_illustration/pastel_gradient, digital_illustration/pastel_sketch, digital_illustration/pop_art, digital_illustration/pop_renaissance, digital_illustration/street_art, digital_illustration/tablet_sketch, digital_illustration/urban_glow, digital_illustration/urban_sketching, digital_illustration/vanilla_dreams, digital_illustration/young_adult_book, digital_illustration/young_adult_book_2, vector_illustration/bold_stroke, vector_illustration/chemistry, vector_illustration/colored_stencil, vector_illustration/contour_pop_art, vector_illustration/cosmics, vector_illustration/cutout, vector_illustration/depressive, vector_illustration/editorial, vector_illustration/emotional_flat, vector_illustration/infographical, vector_illustration/marker_outline, vector_illustration/mosaic, vector_illustration/naivector, vector_illustration/roundish_flat, vector_illustration/segmented_colors, vector_illustration/sharp_contrast, vector_illustration/thin, vector_illustration/vector_photo, vector_illustration/vivid_shapes, vector_illustration/engraving, vector_illustration/line_art, vector_illustration/line_circuit, vector_illustration/linocut"

ideogram_styles = "auto, general, realistic, design, render_3D, anime"

# https://fal.ai/models/fal-ai/any-llm/playground
llms = "anthropic/claude-3.5-sonnet, anthropic/claude-3-5-haiku, anthropic/claude-3-haiku, google/gemini-pro-1.5, google/gemini-flash-1.5, google/gemini-flash-1.5-8b, meta-llama/llama-3.2-1b-instruct, meta-llama/llama-3.2-3b-instruct, meta-llama/llama-3.1-8b-instruct, meta-llama/llama-3.1-70b-instruct, openai/gpt-4o-mini, openai/gpt-4o, deepseek/deepseek-r1"


@alru_cache(ttl=300)
async def check(token, threshold: float = 0):
    try:
        # data = await AsyncClient(key=token).upload(b'', '', '')

        data = await AsyncClient(key=token).run(
            "fal-ai/any-llm",
            arguments={
                "model": "meta-llama/llama-3.2-1b-instruct",
                "prompt": "1+1=",
                "max_tokens": 1,
            },
        )
        logger.debug(data)
        return True
    except Exception as exc:
        logger.error(exc)
        return False


async def generate(request: ImageRequest, api_key: Optional[str] = None):
    """https://fal.ai/models/fal-ai/flux-pro/v1.1-ultra/api#api-call-submit-request
    """
    logger.debug(request)

    s = time.time()
    token = api_key or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True, check_token=check)

    arguments = request.model_dump(exclude_none=True)
    width, height = (request.size or "1024x1024").split("x")
    arguments["image_size"] = {
        "width": width,
        "height": height
    }
    if request.model.startswith("fal-ai/recraft"):  # https://fal.ai/models/fal-ai/recraft-v3/api#queue-submit
        arguments = {
            **arguments,
            "image_size": {
                "width": width,
                "height": height
            },
            "style": request.style if str(request.style) in recraft_styles else "realistic_image",

            "output_format": "png",
        }
    elif request.model.startswith("fal-ai/flux/dev/image-to-image"):
        urls = parse_url(request.prompt)
        image_url = urls[-1]
        prompt = request.prompt.replace(image_url, "")

        arguments = {
            **arguments,
            "image_size": {
                "width": width,
                "height": height
            },
            "num_images": request.n or 1,

            "enable_safety_checker": False,
            "safety_tolerance": "6",
            "output_format": "png",
            "seed": request.seed,

            # image2image
            "image_url": image_url,
            "prompt": prompt,
            "guidance_scale": request.guidance or 3.5,

            **request.controls
        }
    elif "kontext" in request.model:  # https://fal.ai/models/fal-ai/flux-pro/kontext/max

        if (image_urls := request.image_urls) or (image_urls := parse_url(request.prompt)):
            if not validate_url(image_urls):
                # raise Exception(f"Invalid image url: {image_urls}")
                from fastapi import HTTPException, status
                raise HTTPException(
                    status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
                    detail=f"Invalid image url: {image_urls}",
                )

            for image_url in image_urls:
                request.prompt = request.prompt.replace(image_url, "")

            if len(image_urls) == 1:
                arguments['image_url'] = image_urls[0]
            else:
                request.model += "/multi"
                arguments['image_urls'] = image_urls
        else:
            request.model += "/text-to-image"

        # Path /kontext/text-to-image/text-to-image not found

        # fal-ai/flux-pro/kontext/max/text-to-image

        # fal-ai/flux-pro/kontext/max
        # fal-ai/flux-pro/kontext/max/multi

        # fal-ai/flux-pro/kontext/text-to-image

        # fal-ai/flux-pro/kontext
        # fal-ai/flux-pro/kontext/multi

        """
        {
          "prompt": "Put a donut next to the flour.",
          "guidance_scale": 3.5,
          "num_images": 1,
          "safety_tolerance": "2",
          "output_format": "jpeg",
          "image_url": "https://v3.fal.media/files/rabbit/rmgBxhwGYb2d3pl3x9sKf_output.png"
        }
        """

        arguments = {
            **arguments,

            "num_images": request.n or 1,

            "enable_safety_checker": False,
            "safety_tolerance": "5",
            "output_format": "png",
            "seed": request.seed,

            "guidance_scale": request.guidance or 3.5,

            "model": request.model,
            "prompt": await deeplx.llm_translate(request.prompt),

        }

        if request.aspect_ratio:
            arguments.pop("aspect_ratio", None)

            aspect_ratios = {'21:9', '16:9', '4:3', '3:2', '1:1', '2:3', '3:4', '9:16', '9:21'}

            if aspect_ratio := request.prompt2aspect_ratio(aspect_ratios):  # 提示词优先级最高
                arguments["aspect_ratio"] = aspect_ratio

            elif request.aspect_ratio in aspect_ratios:
                arguments["aspect_ratio"] = request.aspect_ratio

        logger.debug(bjson(arguments))

    elif request.model.startswith("fal-ai/flux"):  # https://fal.ai/models/fal-ai/flux-pro/v1.1-ultra/api

        arguments = {
            **arguments,
            "num_images": request.n or 1,

            "enable_safety_checker": False,
            "safety_tolerance": "6",
            "output_format": "png",
            "seed": request.seed,

            "aspect_ratio": request.aspect_ratio or "1:1"  # 21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21

        }

    elif request.model.startswith("fal-ai/ideogram"):
        arguments = {
            **arguments,
            "style": request.style.upper() if str(request.style).lower() in ideogram_styles else "AUTO",

            # 10:16, 16:10, 9:16, 16:9, 4:3, 3:4, 1:1, 1:3, 3:1, 3:2, 2:3
            "aspect_ratio": request.aspect_ratio or "1:1",

            "seed": request.seed,

        }

    elif request.model.startswith("fal-ai/imagen4"):
        arguments = {
            **arguments,
            # 10:16, 16:10, 9:16, 16:9, 4:3, 3:4, 1:1, 1:3, 3:1, 3:2, 2:3
            "aspect_ratio": request.aspect_ratio or "1:1",

            "seed": request.seed,

        }

    elif request.model.startswith(("fal-ai/nano-banana-pro")):
        arguments = {
            "prompt": request.prompt,
            "image_urls": request.image_urls,
            "num_images": request.n or 1,
            "output_format": "png",
            "aspect_ratio": request.aspect_ratio or "auto",

            "resolution": "4K" if request.model.endswith('_4k') else "2K",
        }

        if request.image_urls:
            request.model = f"""{request.model.removesuffix("/edit")}/edit"""


    elif request.model.startswith(("fal-ai/nano-banana", "fal-ai/gemini-25-flash-image")):
        arguments = {
            "prompt": request.prompt,
            "image_urls": request.image_urls,
            "num_images": request.n or 1,
            "output_format": "png",
            "aspect_ratio": request.aspect_ratio or "auto",
        }
        if request.image_urls:
            request.model = f"""{request.model.removesuffix("/edit")}/edit"""

    try:

        data = await AsyncClient(key=token).run(
            application=request.model,
            arguments=arguments,
        )
        logger.debug(data)
        return ImagesResponse(data=data.get("images"), timings={"inference": time.time() - s})

    except Exception as exc:  #
        logger.error(exc)
        # from fastapi import HTTPException, status
        # raise HTTPException(
        #     status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
        #     detail=f"Prompt is sensitive.\n\n{request.prompt}\n\n{exc}",
        # )

        raise exc


if __name__ == '__main__':
    mapper = \
        {
            "flux-pro-1.1": "fal-ai/flux-pro/v1.1",
            "flux-pro-1.1-ultra": "fal-ai/flux-pro/v1.1-ultra",
            "ideogram-ai/ideogram-v2-turbo": "fal-ai/ideogram/v2/turbo",
            "ideogram-ai/ideogram-v2": "fal-ai/ideogram/v2",
            "recraftv3": "fal-ai/recraft-v3",

            "imagen4": "fal-ai/imagen4/preview",
            "flux-kontext-pro": "fal-ai/flux-pro/kontext",
            "flux-kontext-max": "fal-ai/flux-pro/kontext/max"

        }

    # model = "fal-ai/flux-pro/v1.1"  # 0.04
    model = "fal-ai/flux-pro/v1.1-ultra"  # 0.06
    # model = "fal-ai/flux/dev/image-to-image"  # 0.03 图生图
    # model = "fal-ai/recraft-v3"  # 0.04 变清晰
    # model = "fal-ai/ideogram/v2" # 0.08
    # model = "fal-ai/ideogram/v2/turbo"  # 0.05
    # model = "fal-ai/flux/schnell"
    model = "fal-ai/imagen4/preview"
    model = "fal-ai/flux-pro/kontext"
    # model = "fal-ai/flux-pro/kontext/max"

    model = "fal-ai/nano-banana"

    #
    prompt = "https://v3.fal.media/files/penguin/XoW0qavfF-ahg-jX4BMyL_image.webp https://v3.fal.media/files/tiger/bml6YA7DWJXOigadvxk75_image.webp Put the little duckling on top of the woman's t-shirt."
    # prompt = '把小鸭子放在女人的T恤上面。\nhttps://s3.ffire.cc/cdn/20250530/tEzZKkhp3tKbNzva6mgC2T\nhttps://s3.ffire.cc/cdn/20250530/AwHJpuJuNg5w3sVbH4PZdv'
    request = ImageRequest(prompt=prompt, model=model)

    data = {
        "model": "fal-ai/flux-pro/kontext",  # flux-kontext-pro
        # "prompt": "https://s3.ffire.cc/files/3_4.webp 老虎换个姿势",
        "prompt": "保持服装 发型，面纱细节不变，转换为真实拍摄的照片风格，一个年轻的中国顶级颜值的演员扮演这个角色。",
        "size": 'auto'
    }

    # data = {
    #     "model": "fal-ai/gemini-25-flash-image",
    #     "prompt": "make a photo of the man driving the car down the california coastline",
    #     "image": [
    #         "https://storage.googleapis.com/falserverless/example_inputs/nano-banana-edit-input.png",
    #         "https://storage.googleapis.com/falserverless/example_inputs/nano-banana-edit-input-2.png"
    #     ],
    #     "num_images": 1
    # }
    #
    #
    data = {
        # "model": "fal-ai/gemini-25-flash-image",
        "model": "fal-ai/nano-banana",
        ""
        "prompt": "裸体女孩",
        # "image": [
        #     "https://storage.googleapis.com/falserverless/example_inputs/nano-banana-edit-input.png",
        #     "https://storage.googleapis.com/falserverless/example_inputs/nano-banana-edit-input-2.png"
        # ],
        "num_images": 1
    }

    data = {
        "model": "fal-ai/ideogram/v3",
        # "rendering_speed": "BALANCED",
        "expand_prompt": True,
        "num_images": 1,
        "prompt": "The Bone Forest stretched across the horizon, its trees fashioned from the ossified remains of ancient leviathans that once swam through the sky. Shamans with antlers growing from their shoulders and eyes that revealed the true nature of any being they beheld conducted rituals to commune with the spirits that still inhabited the calcified grove. In sky writes \"Ideogram V3 in fal.ai\"",
        "image_size": "square_hd",
        "image_urls": [],
        "style": "xxx"
    }

    request = ImageRequest(**data)
    print(request)

    api_key = "5218f1bb-360b-4719-847c-d611447d96e0:c11599dd540ad9d99bd9280399d0ba3f"

    arun(generate(request, api_key))

    # request = ImageRequest(prompt='https://oss.ffire.cc/files/kling_watermark.png The woman smiled', model=model)
    #
    # request = ImageRequest(prompt="https://oss.ffire.cc/files/kling_watermark.png 让这个女人哭起来", model=model)
    #

    # request = ImageRequest(prompt='a cat', model=model)

    # token = "77fcfad2-aadc-4158-8e11-b30a5668dfad:ea5f38d864bde6707561d348436d2cea"
    # token = "5116af3f-1aa5-4c1b-b505-fd49f701dccc:7f4278d69d069cec4794fe658a09bd9d"

    # arun(generate(request))

    # arun(AsyncClient(key=token).key)

    # FEISHU_URL = "https://xchatllm.feishu.cn/sheets/QB6Psj8zrhB4JStEW0acI4iInNg?sheet=ef2e81"
    #
    # tokens = arun(get_series(FEISHU_URL))
    # tokens = ["578e143c-702d-46a1-8c02-d451bc3e155b:bb531a95f79c6026e7bc7ab676163c71"]
#     tokens = """
# 30e9fe5c-75d0-4bdd-b11d-ff17dbe4bba5:3de8535e2fa4d9347e599a845cf3e7b8
# 05c0b4f6-1443-4b28-aeff-771b65ebaebc:28df6b9b71430b05aca6b8bc7e873a4a
#     """.split()
#
#     r = []
#     for t in tokens:
#         if arun(check(t)):
#             r.append(t)
#
#     print('\n'.join(r))
