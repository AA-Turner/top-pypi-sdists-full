#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2024/9/20 17:59
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from meutils.config_utils.lark_utils import aget_spreadsheet_values, get_next_token_for_polling



if __name__ == '__main__':
    feishu_url = 'https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=hxVlQw'
    d = arun(aget_spreadsheet_values(feishu_url=feishu_url, to_dataframe=True))
    # d = arun(aget_spreadsheet_values(feishu_url=feishu_url))






