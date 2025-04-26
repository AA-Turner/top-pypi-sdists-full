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
from meutils.str_utils.regular_expression import parse_url

from meutils.schemas.image_types import ImageRequest, FluxImageRequest, SDImageRequest, ImagesResponse
from meutils.schemas.fal_types import FEISHU_URL
from meutils.config_utils.lark_utils import get_next_token_for_polling, get_series

from fal_client.client import AsyncClient, SyncClient, Status, FalClientError

recraft_styles = "any, realistic_image, digital_illustration, vector_illustration, realistic_image/b_and_w, realistic_image/hard_flash, realistic_image/hdr, realistic_image/natural_light, realistic_image/studio_portrait, realistic_image/enterprise, realistic_image/motion_blur, realistic_image/evening_light, realistic_image/faded_nostalgia, realistic_image/forest_life, realistic_image/mystic_naturalism, realistic_image/natural_tones, realistic_image/organic_calm, realistic_image/real_life_glow, realistic_image/retro_realism, realistic_image/retro_snapshot, realistic_image/urban_drama, realistic_image/village_realism, realistic_image/warm_folk, digital_illustration/pixel_art, digital_illustration/hand_drawn, digital_illustration/grain, digital_illustration/infantile_sketch, digital_illustration/2d_art_poster, digital_illustration/handmade_3d, digital_illustration/hand_drawn_outline, digital_illustration/engraving_color, digital_illustration/2d_art_poster_2, digital_illustration/antiquarian, digital_illustration/bold_fantasy, digital_illustration/child_book, digital_illustration/child_books, digital_illustration/cover, digital_illustration/crosshatch, digital_illustration/digital_engraving, digital_illustration/expressionism, digital_illustration/freehand_details, digital_illustration/grain_20, digital_illustration/graphic_intensity, digital_illustration/hard_comics, digital_illustration/long_shadow, digital_illustration/modern_folk, digital_illustration/multicolor, digital_illustration/neon_calm, digital_illustration/noir, digital_illustration/nostalgic_pastel, digital_illustration/outline_details, digital_illustration/pastel_gradient, digital_illustration/pastel_sketch, digital_illustration/pop_art, digital_illustration/pop_renaissance, digital_illustration/street_art, digital_illustration/tablet_sketch, digital_illustration/urban_glow, digital_illustration/urban_sketching, digital_illustration/vanilla_dreams, digital_illustration/young_adult_book, digital_illustration/young_adult_book_2, vector_illustration/bold_stroke, vector_illustration/chemistry, vector_illustration/colored_stencil, vector_illustration/contour_pop_art, vector_illustration/cosmics, vector_illustration/cutout, vector_illustration/depressive, vector_illustration/editorial, vector_illustration/emotional_flat, vector_illustration/infographical, vector_illustration/marker_outline, vector_illustration/mosaic, vector_illustration/naivector, vector_illustration/roundish_flat, vector_illustration/segmented_colors, vector_illustration/sharp_contrast, vector_illustration/thin, vector_illustration/vector_photo, vector_illustration/vivid_shapes, vector_illustration/engraving, vector_illustration/line_art, vector_illustration/line_circuit, vector_illustration/linocut"

ideogram_styles = "auto, general, realistic, design, render_3D, anime"

# https://fal.ai/models/fal-ai/any-llm/playground
llms = "anthropic/claude-3.5-sonnet, anthropic/claude-3-5-haiku, anthropic/claude-3-haiku, google/gemini-pro-1.5, google/gemini-flash-1.5, google/gemini-flash-1.5-8b, meta-llama/llama-3.2-1b-instruct, meta-llama/llama-3.2-3b-instruct, meta-llama/llama-3.1-8b-instruct, meta-llama/llama-3.1-70b-instruct, openai/gpt-4o-mini, openai/gpt-4o, deepseek/deepseek-r1"


@alru_cache(ttl=600)
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


async def generate(request: ImageRequest, token: Optional[str] = None):
    """https://fal.ai/models/fal-ai/flux-pro/v1.1-ultra/api#api-call-submit-request
    """
    logger.debug(request)

    s = time.time()
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True, check_token=check)

    arguments = request.model_dump(exclude_none=True)
    width, height = request.size.split("x")
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
    elif request.model.startswith(
            "fal-ai/flux/dev/image-to-image"):  # https://fal.ai/models/fal-ai/flux-pro/v1.1-ultra/api
        urls = parse_url(request.prompt)
        image_url = urls[-1]
        prompt = request.prompt.replace(image_url, "")

        arguments = {
            **arguments,
            "image_size": {
                "width": width,
                "height": height
            },
            "num_images": request.n,

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
    elif request.model.startswith("fal-ai/flux"):  # https://fal.ai/models/fal-ai/flux-pro/v1.1-ultra/api

        arguments = {
            **arguments,
            "num_images": request.n,

            "enable_safety_checker": False,
            "safety_tolerance": "6",
            "output_format": "png",
            "seed": request.seed,

            "aspect_ratio": request.aspect_ratio or "1:1"  # 21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21

        }

    elif request.model.startswith("fal-ai/ideogram"):
        arguments = {
            **arguments,
            "style": request.style if str(request.style) in ideogram_styles else "auto",

            # 10:16, 16:10, 9:16, 16:9, 4:3, 3:4, 1:1, 1:3, 3:1, 3:2, 2:3
            "aspect_ratio": request.aspect_ratio or "1:1",

            "seed": request.seed,

        }
    try:

        data = await AsyncClient(key=token).run(
            application=request.model,
            arguments=arguments,
        )
        logger.debug(data)
        return ImagesResponse(data=data.get("images"), timings={"inference": time.time() - s})

    except Exception as exc:  #
        logger.error(exc)
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate image: {exc}",
        )


if __name__ == '__main__':
    mapper = \
        {
            "flux-pro-1.1": "fal-ai/flux-pro/v1.1",
            "flux-pro-1.1-ultra": "fal-ai/flux-pro/v1.1-ultra",
            "ideogram-ai/ideogram-v2-turbo": "fal-ai/ideogram/v2/turbo",
            "ideogram-ai/ideogram-v2": "fal-ai/ideogram/v2",
            "recraftv3": "fal-ai/recraft-v3",
        }

    # model = "fal-ai/flux-pro/v1.1"  # 0.04
    model = "fal-ai/flux-pro/v1.1-ultra"  # 0.06
    # model = "fal-ai/flux/dev/image-to-image"  # 0.03 图生图
    # model = "fal-ai/recraft-v3"  # 0.04 变清晰
    # model = "fal-ai/ideogram/v2" # 0.08
    # model = "fal-ai/ideogram/v2/turbo"  # 0.05
    # model = "fal-ai/flux/schnell"

    # request = ImageRequest(prompt='https://oss.ffire.cc/files/kling_watermark.png The woman smiled', model=model)
    request = ImageRequest(prompt='a cat', model=model)

    # token = "77fcfad2-aadc-4158-8e11-b30a5668dfad:ea5f38d864bde6707561d348436d2cea"
    # token = "5116af3f-1aa5-4c1b-b505-fd49f701dccc:7f4278d69d069cec4794fe658a09bd9d"

    # arun(generate(request))

    # arun(AsyncClient(key=token).key)

    tokens = arun(get_series(FEISHU_URL))
    # tokens = [token]

    r = []
    for t in tokens:
        if arun(check(t)):
            r.append(t)
