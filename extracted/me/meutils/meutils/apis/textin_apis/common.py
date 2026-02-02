#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2025/3/23 11:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.io.files_utils import to_bytes, to_url

from meutils.schemas.textin_types import BASE_URL, WatermarkRemove, PdfToMarkdown, CropEnhanceImage
from meutils.schemas.image_types import ImageRequest, ImagesResponse

from httpx import AsyncClient


class Textin(object):
    def __init__(self, api_key: Optional[str] = None):
        # https://www.textin.com/console/dashboard/setting
        app_id, secret_code = (api_key or os.getenv("TEXTIN_API_KEY")).split("|")

        logger.debug(f"{app_id, secret_code}")

        self.base_url = BASE_URL
        self.headers = {
            'x-ti-app-id': app_id,
            'x-ti-secret-code': secret_code,
            'Content-Type': "text/plain"
        }

    # @rcache(noself=True, ttl=24 * 3600, serializer="pickle")
    async def image_watermark_remove(self, request: Union[WatermarkRemove, ImageRequest]):
        s = time.perf_counter()

        if not request.image.startswith("http"):
            request.image = await to_bytes(request.image)
            # content_type = "application/octet-stream"
            # logger.info(f"image: {type(request.image)}")

        async with AsyncClient(base_url=self.base_url, headers=self.headers, timeout=100) as cilent:
            response = await cilent.post("/image/watermark_remove", content=request.image)
            response.raise_for_status()

            data = response.json()
            data['timings'] = {'inference': time.perf_counter() - s}

            if data.get("code") == 200:
                image = data["result"]["image"]

                if request.response_format != "b64_json":
                    image = await to_url(image, filename=f'{shortuuid.random()}.png')

                if isinstance(request, ImageRequest):
                    data = [{"url": image}]
                    if request.response_format == "b64_json":
                        data = [{"b64_json": image}]

                    return ImagesResponse(data=data)

            data["result"]["image"] = image
            return data

    async def pdf_to_markdown(self, request: PdfToMarkdown, params: Optional[dict] = None):  # crop_enhance_image
        s = time.perf_counter()

        request.data = await to_bytes(request.data)

        params = params or {}
        async with AsyncClient(base_url=self.base_url, headers=self.headers, timeout=100, params=params) as cilent:
            response = await cilent.post("pdf_to_markdown", content=request.data)
            response.raise_for_status()

            data = response.json()
            data['timings'] = {'inference': time.perf_counter() - s}

            logger.debug(bjson(data))

            return data

    async def crop_enhance_image(self, request: CropEnhanceImage, params: Optional[dict] = None):  # crop_enhance_image
        s = time.perf_counter()

        request.data = await to_bytes(request.data)

        params = params or {}
        async with AsyncClient(base_url=self.base_url, headers=self.headers, timeout=100, params=params) as cilent:
            response = await cilent.post("crop_enhance_image", content=request.data)
            response.raise_for_status()

            data = response.json()
            data['timings'] = {'inference': time.perf_counter() - s}

            # {'code': 200,
            #  'duration': 161,
            #  'message': 'success',
            #  'result': {'image_list': [{'angle': 0,
            #                             'cropped_height': 848,
            #                             'cropped_width': 628,
            #                             'image':

            if request.response_format == "url" and data.get("code") == 200:
                for image in data["result"]["image_list"]:
                    image["image"] = await to_url(image["image"], filename=f'{shortuuid.random()}.png')

            logger.debug(bjson(data))

            return data


if __name__ == '__main__':
    # image = "doc_watermark.jpg"

    # image = "https://oss.ffire.cc/files/nsfw.jpg"
    image = "https://s3.ffire.cc/files/pdf_to_markdown.jpg"  # 无水印

    request = WatermarkRemove(
        image=image,
        # response_format="url"，
        response_format="b64_json"

    )
    # arun(Textin().image_watermark_remove(request))

    request = ImageRequest(
        image=image,
        # response_format="b64_json"
    )

    arun(Textin().image_watermark_remove(request))

    # request = PdfToMarkdown(
    #     data="https://s3.ffire.cc/files/pdf_to_markdown.jpg",
    #     response_format="url"
    # )
    #
    # # arun(Textin().pdf_to_markdown(request))
    #
    # request = CropEnhanceImage(
    #     data="https://s3.ffire.cc/files/pdf_to_markdown.jpg",
    #     response_format="url"
    # )

    # arun(Textin().crop_enhance_image(request))
#
