#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : reranker
# @Time         : 2024/8/13 10:08
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from meutils.schemas.siliconflow_types import BASE_URL, RerankRequest, EXAMPLES
from meutils.config_utils.lark_utils import get_spreadsheet_values, get_next_token_for_polling

FEISHU_URL = 'https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=InxiCF'


@alru_cache()
async def rerank(request: RerankRequest, api_key: Optional[str] = None):
    api_key = api_key or await get_next_token_for_polling(feishu_url=FEISHU_URL)

    payload = request.model_dump()
    payload['model'] = "BAAI/bge-reranker-v2-m3"  # 写死

    headers = {
        "authorization": f"Bearer {api_key}"
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post("/rerank", json=payload)
        # logger.debug(response.text)

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()


if __name__ == '__main__':
    arun(rerank(RerankRequest(**EXAMPLES[0])))
