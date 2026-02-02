#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : deeplx
# @Time         : 2024/3/1 16:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo doubao-seed-translation-250915

from meutils.pipe import *
from meutils.schemas.translator_types import DeeplxRequest
from meutils.decorators.retry import retrying

from meutils.str_utils.regular_expression import has_chinese

from meutils.apis import niutrans
from meutils.llm.clients import AsyncOpenAI, zhipuai_client  # zhipuai_client


@alru_cache
async def llm_translate(prompt):
    if not has_chinese(prompt):
        # logger.debug("直接返回")
        return prompt
    try:
        response = await zhipuai_client.chat.completions.create(
            model="glm-4.5-flash",
            messages=[
                {"role": "system", "content": "将所有输入的文本翻译成英文。请不用解释，直接翻译。"},
                {"role": "user", "content": f"文本：{prompt}"}
            ],
            temperature=0,
            extra_body={
                "thinking": {"type": "disabled"}
            }
        )

        # logger.debug(response)

        return response.choices[0].message.content
    except Exception as e:
        logger.error(e)
        return prompt


@alru_cache()
@retrying()
async def translate(
        request: DeeplxRequest,
        api_key: Optional[str] = None,
):
    """
    https://fakeopen.org/DeepLX/#%E6%8E%A5%E5%8F%A3%E5%9C%B0%E5%9D%80
    https://linux.do/t/topic/111737
    """
    if not request.text.strip(): return {}

    api_key = api_key or "pOnI-G2dDExp_DdXlDhPH2gbIx1DTBEo3JHZ3dam3bw"  # todo

    url = f"https://api.deeplx.org/{api_key}/translate"

    payload = request.model_dump()
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, json=payload)
            data = response.json()
            # logger.debug(data)
            if not data.get('data'):
                logger.error(data)
                raise Exception('DeeplxRequest error')
            else:
                return data
    except Exception as e:
        logger.error(e)
        _ = await niutrans.translate(request.text, 'auto', request.target_lang.lower())
        return {'data': _}


if __name__ == '__main__':
    request = DeeplxRequest(text='讲个故事', source_lang='ZH', target_lang='EN')
    # with timer():
    #     arun(translate(request))

    # arun(translate_prompt('把小鸭子放在女人的T恤上面。'))

    # arun(llm_translate("这是一个文本"))
    arun(llm_translate("你说yes"))
