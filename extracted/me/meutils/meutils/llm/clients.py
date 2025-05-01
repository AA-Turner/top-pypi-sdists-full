#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat
# @Time         : 2024/8/19 14:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 
from openai import Client, AsyncClient, AsyncStream, APIStatusError
from zhipuai import ZhipuAI

from meutils.pipe import *

OpenAI = lru_cache(Client)
AsyncOpenAI = lru_cache(AsyncClient)
ZhipuAI = lru_cache(ZhipuAI)

chatfire_client = AsyncOpenAI()

moonshot_client = AsyncOpenAI(
    api_key=os.getenv("MOONSHOT_API_KEY"),
    # api_key="sk-fWqLGmUtoGgoK9gx5IefO1mWrRF9QHaV7uVRrTcFv1lrJVvJ",
    base_url=os.getenv("MOONSHOT_BASE_URL")
)
zhipuai_client = AsyncOpenAI(
    api_key=os.getenv("ZHIPUAI_API_KEY"),
    base_url=os.getenv("ZHIPUAI_BASE_URL")
)

zhipuai_sdk_client = ZhipuAI(
    api_key=os.getenv("ZHIPUAI_API_KEY"),
    base_url=os.getenv("ZHIPUAI_BASE_URL")
)

# zhipuai_client = OpenAI(
#     api_key=os.getenv("ZHIPUAI_API_KEY"),
#     base_url=os.getenv("ZHIPUAI_BASE_URL")
# )

# ark_bots_client = AsyncOpenAI(
#     api_key=os.getenv("ZHIPUAI_API_KEY"),
#     base_url="https://ark.cn-beijing.volces.com/api/v3/bots"
# )


if __name__ == '__main__':
    from meutils.pipe import *

    # OpenAI().chat.completions.create(messages=[{"role": "user", "content": "hi"}], model='glm-4-flash')

    # arun(zhipuai_client.chat.completions.create(messages=[{"role": "user", "content": "hi"}], model='glm-4-flash'))

    # web-search-pro
    # s = zhipuai_client.chat.completions.create(
    #     messages=[{"role": "user", "content": "《哪吒之魔童闹海》现在的票房是多少"}],
    #     model='web-search-pro',
    #     stream=True
    # )
    #
    # r = arun(zhipuai_client.chat.completions.create(
    #     messages=[{"role": "user", "content": "《哪吒之魔童闹海》现在的票房是多少"}],
    #     model='web-search-pro',
    #     stream=True
    # )
    # )

    # r.model_dump_json()

    # f = zhipuai_client.chat.completions.create(
    #     messages=[{"role": "user", "content": "《哪吒之魔童闹海》现在的票房是多少"}],
    #     model='glm-4-flash',
    # )
    #
    # arun(f)
    #
    # response = zhipuai_client.images.generate(
    #     model="cogview-3-flash",  # 填写需要调用的模型编码
    #     prompt="一只可爱的小猫咪",
    #     n=2,
    #     # size="1024x1024"
    # )
    #
    # arun(response)

    c = zhipuai_client.chat.completions.create(
        messages=[
            {"role": "user", "content": [
                {
                    "type": "text",
                    "text": "总结一下"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://oss.ffire.cc/files/kling_watermark.png"
                    }
                }
            ]
             }],
        model='glm-4v-flash',
    )

    arun(c)
