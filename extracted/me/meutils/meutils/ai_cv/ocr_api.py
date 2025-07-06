#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ocr_api
# @Time         : 2023/8/23 13:16
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://ai.baidu.com/ai-doc/OCR/9k3h7xuv6

from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from aip import AipOcr


class OCR(AipOcr):

    def __init__(self, app_id=None, api_key=None, secret_key=None, predicate=lambda r: r is None or 'error_code' in r):
        """

        :param app_id:
        :param api_key:
        :param secret_key:
        :param predicate: 增加重试条件，有错误代码时重试
        """

        _ = os.getenv('BAIDU_AI', '').split(':') or (app_id, api_key, secret_key)
        assert any(_), "请配置正确的key"

        super().__init__(*_)

        self._request = retrying(ttl_cache()(self._request), predicate=predicate)  # todo: 异步

    @classmethod
    @lru_cache
    def basic_accurate(cls, image, options=None, return_json=False):
        """
            with timer('basic_accurate'):
                img = Path("/Users/betterme/PycharmProjects/AI/aizoo/aizoo/api/港澳台通行证.webp").read_bytes()
                rprint(OCR.basic_accurate(img))
        """
        options = options or {}
        # options["language_type"] = "CHN_ENG"
        # options["detect_direction"] = "true"
        # options["detect_language"] = "true"
        # options["probability"] = "true"

        _ = cls().basicAccurate(image, options)  # todo: 增加错误处理
        # super(OCR, cls()).basicAccurate(url, options)
        if return_json:
            _ = json.dumps(_, ensure_ascii=False)
        return _


if __name__ == '__main__':
    pass
    # url = 'https://tva1.sinaimg.cn/large/e6c9d24egy1h36evn3pcoj20af06tq3c.jpg'
    #
    # with timer(1):
    #     rprint(OCR().basicAccurateUrl(url))
    #
    # with timer(2):
    #     rprint(OCR().basicAccurateUrl(url))

    rprint(OCR().basicAccurate(Path('img.png').read_bytes()))

    # with timer('basic_accurate'):
    #     img = Path("/Users/betterme/PycharmProjects/AI/aizoo/aizoo/api/港澳台通行证.webp").read_bytes()
    #     rprint(OCR.basic_accurate(img))


from modelscope import AutoModelForCausalLM, AutoTokenizer, snapshot_download
from modelscope import GenerationConfig