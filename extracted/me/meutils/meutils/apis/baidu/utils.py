#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2025/7/4 17:34
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import httpx

from meutils.pipe import *
from meutils.apis.utils import make_request
from meutils.io.files_utils import to_base64
from urllib.parse import urlencode, quote

base_url = "https://image.baidu.com/aigc"


async def pic_upload(
        image: Union[str, bytes],
        token: Optional[str] = None,
):
    # data = {
    #     "token": token or "2df26",
    #     "scene": "pic_edit",
    #     "picInfo": quote(await to_base64(image)),
    #     "timestamp": 1751605857221,
    #     # "pageFr": None
    # }

    token = token or "2df26"
    image = await to_base64(image, content_type='image/png')
    # logger.debug(image)
    image = quote(image)
    data = f'token={token}&scene=pic_edit&timestamp=1751605857221&picInfo={image}&pageFr='
    # logger.debug(data)
    #
    # data = urlencode(data)
    # logger.debug(data)
    headers = {
        # 'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    response = requests.post(base_url, data=data, headers=headers)
    response.raise_for_status()
    print(response.text)
    return response.json()

    # async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=100) as client:
    #     response = await client.post("/pic_upload", data=data)
    #     response.raise_for_status()
    #
    #
    #     return response.json()


async def upload(image):
    # image = await to_base64(image, content_type='image/png')
    # image = quote(image)

    import requests

    url = "https://image.baidu.com/aigc/pic_upload"

    payload = f'token=fbf4c&scene=pic_edit&picInfo={image}&timestamp=1751622550663&pageFr='

    # data = {
    #     "token": "fbf4c",
    #     "scene": "pic_edit",
    #     "picInfo": await to_base64(image),
    #     "timestamp": 1751605857221,
    #     "pageFr": None
    # }
    # payload = urlencode(data)
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

if __name__ == '__main__':
    image = "/Users/betterme/PycharmProjects/AI/img.png"

    # arun(to_base64(image))
    # arun(pic_upload(image))

    arun(upload(image))

    # print(urlencode({"base:xx": ":"}))
