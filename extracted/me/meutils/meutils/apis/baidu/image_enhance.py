#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : image_enhance
# @Time         : 2025/7/4 18:15
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import httpx

from meutils.pipe import *
from meutils.caches import rcache

from meutils.apis.utils import make_request
from meutils.io.files_utils import to_base64, to_url


@rcache(ttl=1 * 24 * 3600)
async def get_baidubce_access_token(token: Optional[str] = None):
    token = token or 'Uj2Q0X4YLGUl7jEj71evIkP2|QRAknDeIKU87ULXHDsf5RQej30Nge4pr'

    ak, sk = token.split('|')
    response = await make_request(
        base_url="https://aip.baidubce.com",
        path="/oauth/2.0/token",
        params={
            "grant_type": "client_credentials",
            "client_id": ak,
            "client_secret": sk
        },
        method="GET"
    )
    return response.get('access_token')


@rcache(ttl=1 * 24 * 3600)
async def image_enhance(image, response_format: str = "url"):
    access_token = await get_baidubce_access_token()

    params = {
        "access_token": access_token
    }
    base_url = "https://aip.baidubce.com"
    path = "/rest/2.0/image-process/v1/image_definition_enhance"

    if image.startswith('http'):
        payload = {'url': image}
    else:
        payload = {'image': await to_base64(image, content_type='image/png')}

    async with httpx.AsyncClient(base_url=base_url, params=params) as client:
        response = await client.post(path, data=payload)
        response.raise_for_status()
        response = response.json()

        if response_format == "url" and response.get('image'):
            response['image'] = await to_url(response['image'], content_type='image/png')

        return response

async def image_enhance_(image, response_format: str = "url"):
    access_token = await get_baidubce_access_token()

    params = {
        "access_token": access_token
    }
    base_url = "https://aip.baidubce.com"
    path = "/rest/2.0/image-process/v1/image_definition_enhance"

    if image.startswith('http'):
        payload = {'url': image}
    else:
        payload = {'image': await to_base64(image, content_type='image/png')}

    async with httpx.AsyncClient(base_url=base_url, params=params) as client:
        response = await client.post(path, data=payload)
        response.raise_for_status()
        response = response.json()

        if response_format == "url" and response.get('image', '').startswith('data:image'):
            response['image'] = await to_url(response['image'], content_type='image/png')

        return response


if __name__ == '__main__':
    image = "https://oss.ffire.cc/files/liu.jpg"
    image = "https://jinhua-1359405894.cos.ap-shanghai.myqcloud.com/mj/2025/06/23/3bc3df77-f413-4a78-a191-31ec5a014ddd.png"
    _ = arun(image_enhance(image))
