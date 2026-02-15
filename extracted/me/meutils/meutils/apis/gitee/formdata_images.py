#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : formdata_images
# @Time         : 2026/2/14 23:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from openai import AsyncOpenAI
from meutils.schemas.image_types import ImageRequest, ImagesResponse

"""

curl https://ai.gitee.com/v1/images/mattings \
	-X POST \
	-H "X-Failover-Enabled: true" \
	-H "Authorization: Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
	-F "image=@path/to/image.webp" \
	-F "model=RMBG-2.0"
	
files = [
        ('file', file_bytes),
        ('security', (None, 'true')),
        ('type', (None, 'image')),
        ('modelName', (None, 'doubao-seedance-2-0')),
        ('modelVersion', (None, '260128')),
        ('biz', (None, 'experience_video')),
    ]

extra_headers = {
    "Content-Type": "multipart/form-data",
    "cookie": api_key
}
client = AsyncOpenAI(base_url=base_url, default_headers=extra_headers)
response = await client.post("/UploadArkTosFile", files=files, cast_to=object)

"""

BASE_URL = "https://ai.gitee.com/v1"


async def generate(request: ImageRequest, api_key: Optional[str] = None):
    # reuqest.image
    if isinstance(request.image, list):
        request.image = request.image[0]

    files = [
        ('model', (None, request.model)),
        ('response_format', (None, request.response_format)),
        # ('image', await to_bytes(request.image)),
        # ('image', (None, request.image)),
    ]
    if request.image.startswith("http"):
        files.append(('image', (None, request.image)))

    default_headers = {
        "X-Failover-Enabled": "true",
        "Content-Type": "multipart/form-data",
    }
    client = AsyncOpenAI(base_url=BASE_URL, api_key=api_key, default_headers=default_headers)

    response = await client.post(
        "/images/mattings",
        files=files,
        cast_to=object
    )

    return response


if __name__ == '__main__':
    api_key = os.getenv("GITEE_API_KEY")
    request = ImageRequest(
        model="RMBG-2.0",
        # image="http://mxrnetfiles.oss-cn-beijing.aliyuncs.com/AI_IMAGE/773920428888133.jpeg"
        image = "https://s3.ffire.cc/files/jimeng.jpg"
    )

    _ = arun(generate(request, api_key=api_key))
