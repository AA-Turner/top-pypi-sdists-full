#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : got_ocr
# @Time         : 2024/9/26 18:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 尝试异步任务

from meutils.pipe import *

from meutils.decorators.retry import retrying

from meutils.schemas.ocr_types import OCRRequest
from meutils.io.files_utils import to_tempfile

from meutils.apis.hf.gradio import create_client, handle_file

ENDPOINT = "stepfun-ai/GOT_official_online_demo"

ENDPOINT = "https://s5k.cn/api/v1/studio/stepfun-ai/GOT_official_online_demo/gradio/"


# httpx_kwargs


@retrying(max_retries=3)
async def create(request: OCRRequest):
    client = await create_client(ENDPOINT)

    async with to_tempfile(request.image) as file:
        # client.predict
        job = client.submit(
            image=handle_file(file),
            got_mode=request.mode,
            fine_grained_mode=request.fine_grained_mode,
            ocr_color=request.ocr_color,
            ocr_box=request.ocr_box,
            api_name="/run_GOT",

        )
        text, rendered_html = job.result(timeout=100)
        return text, rendered_html


if __name__ == '__main__':
    url = 'https://oss.ffire.cc/images/vertical-text.jpg'

    # for mode in [
    #     'plain texts OCR', 'plain multi-crop OCR', 'plain fine-grained OCR',
    #     'format texts OCR', 'format multi-crop OCR', 'format fine-grained OCR']:
    #     for i in range(100):
    #         request = OCRRequest(image=url)
    #
    #

    # request = OCRRequest(image=url, mode="format multi-crop OCR")
    # arun(create(request))

    request = OCRRequest(image=url, mode="plain texts OCR")
    texts = arun(create(request))

    print(type(texts))
