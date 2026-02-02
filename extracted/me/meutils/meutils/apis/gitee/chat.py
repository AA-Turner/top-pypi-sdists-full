#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat
# @Time         : 2025/12/4 17:50
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo 增加 pdf  报错走 kimi 兜底 + vl

from meutils.pipe import *
from openai import AsyncOpenAI
from meutils.io.files_utils import to_bytes
from meutils.schemas.openai_types import CompletionRequest

BASE_URL = "https://ai.gitee.com/v1"

"""
支持 .jpg、.jpeg、.png、.gif、.webp 格式，图片分辨率不超过 2048x2048

curl https://ai.gitee.com/v1/images/ocr \
	-X POST \
	-H "Authorization: Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
	-F "image=@path/to/image.webp" \
	-F "model=HunyuanOCR" \
	-F "prompt=检测并识别图片中的文字，将文本坐标格式化输出。"
	
	
curl https://ai.gitee.com/v1/async/documents/parse \
	-X POST \
	-H "X-Failover-Enabled: true" \
	-H "Authorization: Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
	-F "file=@path/to/file.pdf" \
	-F "model=PaddleOCR-VL" \
	-F "include_image=true" \
	-F "include_image_base64=true" \
	-F "output_format=md"
"""


class Completions(object):
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 http_url: Optional[Any] = None):
        self.base_url = base_url or BASE_URL
        self.api_key = api_key or os.environ.get("GITEE_API_KEY")

        self.http_url = http_url

    async def create(self, request: CompletionRequest):
        client = AsyncOpenAI(base_url=self.base_url, api_key=self.api_key)

        payload = {
            "model": request.model,
            "prompt": request.last_user_content,
            "output_format": request.response_format or "md"
        }
        # client.files.create()

        extra_headers = {
            "Content-Type": "multipart/form-data",
            # **(extra_headers or {})
        }

        if images := request.last_urls.get("image_url"):
            # logger.debug(await to_bytes(image[0]))
            image = images[0]

            response = await client.post(
                path="/images/ocr",
                body=payload,
                files={
                    "image": await to_bytes(image),
                },
                cast_to=object,
                options={
                    "headers": extra_headers,
                }
            )
            logger.debug(response)
            return response.get("text_result") or ""

        elif files := request.last_urls.get("file_url"): # kimi paddle ocr
            file = files[0]

            payload["include_image"] = True
            payload['include_image_base64'] = True
            response = await client.post(
                path="/images/ocr",
                body=payload,
                files={
                    "file": await to_bytes(file),
                },
                cast_to=object,
                options={
                    "headers": extra_headers,
                }
            )

        # paddle kimi


if __name__ == '__main__':
    request = CompletionRequest(
        model="HunyuanOCR",  # https://s3.ffire.cc/files/pdf_to_markdown.jpg
        # response_format="json",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://s3.ffire.cc/files/pdf_to_markdown.jpg"
                        }
                    },
                    {
                        "type": "text",
                        "text": "描述内容"
                    }
                ]
            }
        ]
    )
    completions = Completions()
    response = arun(completions.create(request))
    logger.debug(response)
