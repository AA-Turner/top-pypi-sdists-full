#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : niutrans
# @Time         : 2024/4/29 10:55
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import requests

from meutils.pipe import *

import json
import urllib.error
import urllib.parse
import urllib.request
from openai import OpenAI, AsyncOpenAI

base_url = 'http://api.niutrans.com'

client = AsyncOpenAI(base_url=base_url)


@lru_cache()
def _translate(sentence, src_lan, tgt_lan, apikey="f77c833dc48cf93e1e85bea2d6f17459"):
    url = 'http://api.niutrans.com/NiuTransServer/translation?'
    data = {"from": src_lan, "to": tgt_lan, "apikey": apikey, "src_text": sentence}
    data_en = urllib.parse.urlencode(data)
    req = url + "&" + data_en
    res = urllib.request.urlopen(req)
    res = res.read()
    res_dict = json.loads(res)
    if "tgt_text" in res_dict:
        result = res_dict['tgt_text']
    else:
        result = res
    return result


@alru_cache
async def translate(sentence, src_lan, tgt_lan, **kwargs):
    apikey = "f77c833dc48cf93e1e85bea2d6f17459"

    payload = {"from": src_lan, "to": tgt_lan, "apikey": apikey, "src_text": sentence}

    response = await client.post(path="/NiuTransServer/translation", cast_to=object, body=payload)

    logger.debug(response)

    if isinstance(response, str) and "tgt_text" in response:
        data = json.loads(response)
        return data.get('tgt_text')


if __name__ == "__main__":
    # print(translate("你好", 'auto', 'ti'))
    # print(translate("ཁྱོད་བདེ་མོ།", 'auto', 'zh'))
    # print(translate("藏语", 'auto', 'ti'))
    # print(translate("讲个故事吧", 'auto', 'ti'))
    # print(translate("གཏམ་རྒྱུད་ཅིག་བཤད་དང་།", 'auto', 'zh'))

    # in_src = open("zh.txt", "r", encoding='utf-8')
    # out_src = open("zh.txt.big.test", "w", encoding='utf-8')
    # lines = in_src.readlines()
    # for line in lines:
    #     line = line.strip()
    #     trans = translate(line, 'zh', 'en', '您的apikey')
    #     try:
    #         trans = trans.decode('utf-8')
    #     except:
    #         trans = trans
    #     out_src.write(trans + "")

    r = arun(translate("你好", 'auto', 'en'))
