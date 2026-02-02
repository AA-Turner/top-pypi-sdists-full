#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/9/26 15:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from meutils.decorators.retry import retrying

url = "https://api.siliconflow.cn/v1/user/info"


# todo: 付费不付费模型优化
@retrying()
async def check_token(api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    try:
        async with httpx.AsyncClient(headers=headers, timeout=60) as client:
            response: httpx.Response = await client.get(url)
            response.raise_for_status()

            logger.debug(response.text)
            logger.debug(response.status_code)

            if response.is_success:
                balance = response.json()['data']['balance']
                return float(balance) > 0
    except Exception as e:
        logger.error(e)
        return False


if __name__ == '__main__':
    from meutils.pipe import *
    from openai import OpenAI

    api_key = os.getenv("SILICONFLOW_API_KEY")  # sk-fbumsiflwnsgdvegjksroqsgejocgigbnvltqiwhrasixnra

    feishu_url = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=InxiCF"
    feishu_url = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=GSHr1U"
    from meutils.config_utils.lark_utils import aget_spreadsheet_values

    df = arun(aget_spreadsheet_values(feishu_url=feishu_url, to_dataframe=True))

    for i in df[0]:
        if i:
            try:
                r = OpenAI(api_key=i,
                           # base_url=os.getenv("SILICONFLOW_BASE_URL"),
                           base_url="http://siliconflow.ffire.cc/v1"
                           ).chat.completions.create(
                    messages=[{"role": "user", "content": "你是谁"}], model="Qwen/Qwen2.5-7B-Instruct")
                print(r)
            except Exception as e:
                logger.error(e)
                print(i)


