#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : textin
# @Time         : 2024/6/26 08:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 重构 https://tools.textin.com/
# https://www.textin.com/console/recognition/robot_enhance?service=watermark-remove

# proxies 取消了 https://github.com/encode/httpx/pull/2879

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.notice.feishu import send_message
from meutils.io.files_utils import to_url_fal as to_url
from meutils.apis.proxy.kdlapi import get_one_proxy

from fake_useragent import UserAgent

ua = UserAgent()

BASE_URL = "https://api.textin.com/home"

proxy = "http://110.42.51.201:38443"


@alru_cache(ttl=3600 * 24)
async def document_process(data: bytes,
                           service: str = "pdf_to_markdown",
                           response_format: str = "url",
                           token: Optional[str] = None,  # 821480df15b637852f7e4a0dabb8a156
                           **kwargs):
    """

    :param data:
    :param service: pdf_to_markdown watermark-remove dewarp
    :param response_format:
    :param kwargs:
    :return:
    """

    params = {
        "service": service,
        **kwargs

        # "page_count": page_count,
        # "get_image": "objects"
        # "apply_document_tree": 0,
    }

    request_kwargs = {}
    # request_kwargs = {"proxies": proxies}

    for i in range(3):

        headers = {
            "token": token or str(uuid.uuid4()).replace("-", ""),
            'User-Agent': ua.random,
        }
        try:
            async with httpx.AsyncClient(base_url=BASE_URL, timeout=60, headers=headers, **request_kwargs) as client:
                response = await client.post('/user_trial_ocr', content=data, params=params)
                response.raise_for_status()

                logger.debug(response.status_code)
                # logger.info(response.json())  # {'msg': '今日请求超过限制次数', 'code': 431}

                _ = response.json()

                if '今日请求超过限制次数' in str(_):
                    # logger.info(response.json())
                    raise Exception("更新请求头或者加代理")
                else:
                    break


        except Exception as e:  # 加代理
            logger.error(e)

            request_kwargs = {
                "proxy": await get_one_proxy(),
                # "proxy": proxy,

            }

    if response_format == "url" and service in {"watermark-remove", "crop_enhance_image"}:
        if "data" not in _:
            send_message(_, title=__name__)

        # _ => {'msg': '今日请求超过限制次数', 'code': 431}
        logger.debug(bjson(_))
        # logger.debug(list(_['data']['result']['image']))

        url = await to_url(_['data']['result']['image'])
        _ = {"data": [{"url": url}]}

        # _['data']['result']['image'] = await to_url(_['data']['result']['image'])

    return _


if __name__ == '__main__':
    from meutils.io.files_utils import to_bytes, to_url

    # data = open("/Users/betterme/PycharmProjects/AI/11.jpg", 'rb').read()
    # # data = open("/Users/betterme/PycharmProjects/AI/蚂蚁集团招股书.pdf", 'rb').read()
    # with timer("解析"):
    #     # arun(textin_fileparser(data))
    #     print(arun(textin_fileparser(data, service="pdf_to_markdown")))

    # response = requests.request("POST", url, data=data)
    data = open("/Users/betterme/PycharmProjects/AI/qun.png", 'rb').read()
    data = open("img.png", 'rb').read()
    # data = arun(to_bytes("https://cdn.meimeiqushuiyin.cn/ori/tmp_e8d6329e1b2c1bc541ca530fcbae14e3ec12f65d8d4ec97d.jpg"))

    from meutils.schemas.task_types import Purpose

    service = Purpose.watermark_remove.value

    # service = "pdf_to_markdown"

    service = 'bill_recognize_v2'


    async def main(n=1):
        for i in tqdm(range(n)):
            try:
                _ = await document_process(data, service=service)
                logger.debug(bjson(_))
            except Exception as e:
                logger.error(f"{i}: {e}")
                break


    # with timer("解析"):
    #
    #     # arun(textin_fileparser(data))
    #     data = arun(document_process(data, service=service))
    #
    #     # b64 = data['data']['result']['image']
    #
    #     # base64_to_file(b64, "demo.png")
    #
    #     # data['data']['result']['image'] = arun(to_url(b64))
    #
    #     logger.debug(data)
    #
    #     # {'msg': 'success',
    #     #  'data': {
    #     #      'result': {
    #     #          'image': 'https://sfile.chatglm.cn/chatglm-videoserver/image/e5/e5d4011c.png'
    #     #      },
    #     #      'file_type': '', 'file_data': ''
    #     #  }, 'code': 200
    #     #  }

    arun(main(1))
