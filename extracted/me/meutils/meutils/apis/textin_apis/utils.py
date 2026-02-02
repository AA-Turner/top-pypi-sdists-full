#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2025/3/23 11:06
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from openai import AsyncClient


class BaseTextin(object):
    def __init__(self, api_key: Optional[str]):
        # https://www.textin.com/console/dashboard/setting
        app_id, secret_code = api_key or os.getenv("TEXTIN_API_KEY").split("|")

        self.base_url="https://api.textin.com/ai/service/v1"
        self.headers = {
            'x-ti-app-id': app_id,
            'x-ti-secret-code': secret_code
        }
        # self.client = AsyncClient(
        #     base_url="https://api.textin.com/ai/service/v1",  # /image/watermark_remove
        #     default_headers=headers
        # )


    def image_watermark_remove(self, image):
        """

        :param image: text/plain or application/octet-stream
        :return:
        """
        pass


if __name__ == "__main__":
    pass
