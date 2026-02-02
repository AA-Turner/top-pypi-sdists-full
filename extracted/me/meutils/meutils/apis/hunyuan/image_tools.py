#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : image
# @Time         : 2024/10/11 15:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json_repair

from meutils.pipe import *
from meutils.decorators.retry import retrying, IgnoredRetryException
from meutils.schemas.yuanbao_types import FEISHU_URL, YUANBAO_BASE_URL
from meutils.schemas.image_types import HunyuanImageProcessRequest

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.io.files_utils import to_url_fal as to_url
from meutils.notice.feishu import send_message


@retrying(min=3, ignored_exception_types=(IgnoredRetryException,))
async def image_process(request: HunyuanImageProcessRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)

    payload = {
        "imageUrl": request.image if request.image.startswith('http') else await to_url(request.image),
    }
    if request.task == 'style':
        payload.update({
            "style": request.style,
            "prompt": f"转换为{request.style}",
        })

    headers = {
        'cookie': token
    }
    async with httpx.AsyncClient(base_url=YUANBAO_BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post(f"/api/image/{request.task}", json=payload)
        response.raise_for_status()
        logger.debug(response.text)

        # 新版本的位置可能不一样 注意
        # data = json_repair.repair_json(
        #     response.text.replace(r'\u0026', '&').rsplit("data: [TRACEID", 1)[0],
        #     return_objects=True
        # )[-1]

        skip_strings = ['DONE', 'TRACEID']
        data = response.text.replace(r'\u0026', '&').splitlines() | xsse_parser(skip_strings=skip_strings)
        data = data and data[-1]
        logger.debug(data)

        # todo: 错误处理
        if isinstance(data, dict) and any(data["code"] == code for code in {"429"}):
            Exception(f"重试: {response.text}")

        elif isinstance(data, list) or any(i in response.text for i in {"当前图片没有检测到水印"}):  # 跳过重试并返回原始错误
            raise IgnoredRetryException(f"忽略重试: \n{response.text}")

        data = {
            "data": [
                {
                    "url": data["imageUrl"],
                    "imageUrl": data["imageUrl"],
                    "thumbnailUrl": data["thumbnailUrl"],
                }
            ]
        }

        return data


if __name__ == '__main__':
    # request = ImageProcessRequest(image="https://oss.ffire.cc/files/kling_watermark.png", task='removewatermark')
    token = "web_uid=ac283ec7-4bf6-40c9-a0ce-5a2e0cd7db06; hy_source=web; hy_user=I09MgMfFcUUyVSIg; hy_token=hevVCi/QuVjQcre5NDRMO7FuiWCZoDMIq3Zp8IwNxrPUofl4zWYazHEdeZ2S5o7q; _qimei_q36=; _qimei_h38=f2d27f50f0f23e085296d28303000006a17a09; _qimei_fingerprint=efbb885a22f7d4e5589008c28bc8e7ba; _qimei_uuid42=18c0310102d1002a082420cd40bb9717523c3c7e12; _gcl_au=1.1.915258067.1733278380; _ga_RPMZTEBERQ=GS1.1.1733722091.3.1.1733722108.0.0.0; _ga=GA1.2.981511920.1725261466; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22100000458739%22%2C%22first_id%22%3A%22191b198c7b2d52-0fcca8d731cb9b8-18525637-2073600-191b198c7b31fd9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%A4%BE%E4%BA%A4%E7%BD%91%E7%AB%99%E6%B5%81%E9%87%8F%22%2C%22%24latest_utm_medium%22%3A%22cpc%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkxYjE5OGM3YjJkNTItMGZjY2E4ZDczMWNiOWI4LTE4NTI1NjM3LTIwNzM2MDAtMTkxYjE5OGM3YjMxZmQ5IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTAwMDAwNDU4NzM5In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22100000458739%22%7D%2C%22%24device_id%22%3A%22191b198c7b2d52-0fcca8d731cb9b8-18525637-2073600-191b198c7b31fd9%22%7D"
    with timer():
        image = "https://sfile.chatglm.cn/chatglm4/3dcb1cc2-22ad-420b-9d16-dc71dffc02b2.png"
        image = "https://oss.ffire.cc/files/kling_watermark.png"
        image = "https://cdn.meimeiqushuiyin.cn/2024-12-05/ori/tmp_0511a4cb2066ffc309fa6f7a733ac1e93236709bf46c9430.jpg"
        image = "https://cdn.meimeiqushuiyin.cn/2024-12-05/ori/tmp_de5e186878b079a87d22c561f17e6853.jpg"
        image = "https://yuanbao.tencent.com/api/resource/download?resourceId=740fed65baed5f763db891b5443b7ee5"
        image = url = "https://oss.ffire.cc/files/shuiyin.jpg"
        # image = url = "https://oss.ffire.cc/files/shuiyin2.jpg"

        request = HunyuanImageProcessRequest(image=image, task='removewatermark')

        arun(image_process(request, token=token))
