#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : files
# @Time         : 2024/11/11 13:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.io.files_utils import to_url

import fal_client


async def submit():
    handler = await fal_client.submit_async(
        "fal-ai/flux/dev/image-to-image",
        arguments={
            "image_url": "https://fal.media/files/koala/Chls9L2ZnvuipUTEwlnJC.png",
            "prompt": "一只猫带着眼镜"
        },
        # webhook_url="https://optional.webhook.url/for/results",
    )

    request_id = handler.request_id
    print(request_id)


if __name__ == '__main__':
    # 02ec80b4-4bac-42e4-83bb-f4e1c32e77f7

    # arun(submit())

    # fal_client.upload

    with timer():
        pass
        # p = Path("/Users/betterme/PycharmProjects/AI/100.png")
        #
        # print(fal_client.upload_file(p))

        # fal_client.upload()
        import fal_client

        url = fal_client.upload_file(Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_video/douyin.mp4"))

        # arun(to_url(Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_video/douyin.mp4").read_bytes(), content_type=None))

        import mimetypes

        mimetypes.guess_type('x.wav')
