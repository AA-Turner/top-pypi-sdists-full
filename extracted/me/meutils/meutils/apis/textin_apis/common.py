#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2025/3/23 11:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import shortuuid

from meutils.pipe import *
from meutils.io.files_utils import to_bytes, to_url
from meutils.caches import rcache

from meutils.schemas.textin_types import WatermarkRemove, BASE_URL

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
    async def image_watermark_remove(self, request: WatermarkRemove):
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

            logger.debug(data)

            if request.response_format == "url" and data.get("code") == 200:
                data["result"]["image"] = await to_url(data["result"]["image"], filename=f'{shortuuid.random()}.png')

            return data


if __name__ == '__main__':
    # image = "doc_watermark.jpg"

    # image = "https://oss.ffire.cc/files/nsfw.jpg"
    image = "https://oss.ffire.cc/files/kling_watermark.png"  # 无水印

    request = WatermarkRemove(
        image=image,
        response_format="url"
    )
    arun(Textin().image_watermark_remove(request))
