#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : meta
# @Time         : 2024/11/11 17:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from urllib import parse

import requests
import requests
import json

url = "https://metaso.cn/api/session"

question = "东北证券"

payload = json.dumps({
    "question": question,
    "mode": "detail",
    "engineType": "",
    "scholarSearchDomain": "all",
    "searchTopicId": None,
    "searchTopicName": None
})
headers = {
    # 'token': 'wr8+pHu3KYryzz0O2MaBSNUZbVLjLUYC1FR4sKqSW0p19vmcZAoEmHC72zPh/fHt4VdW84WZEx4CbSUTO9sLBF48wX95yi9MJTWNNw3kbBSs6V4qv8FOocFD2ThCrWwXPwROPpwUqLnM2uWfwtUwaw==',
    # 'Cookie': 'JSESSIONID=2A41A2D4F163AA1534CA7B2B152A1C60; tid=b103b947-be89-40b8-b162-80fdcda60807; __eventn_id_UMO2dYNwFz=jdt3ua9m4t; __eventn_id_UMO2dYNwFz_usr=%7B%22email%22%3A%22undefined%40metasota.ai%22%2C%22created_at%22%3A%22Wed%2C%2004%20Sep%202024%2006%3A55%3A57%20GMT%22%7D; aliyungf_tc=8cfbed3e5fd53c2a81605c7dcb63d45d3114b94750922ef63e04cb5a6ceccba1; s=bdpc; usermaven_id_UMO2dYNwFz=4d3f1r1j6i; hideLeftMenu=1; newSearch=false',
    # 'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

logger.debug(response.text)

session_id = response.json()['data']['id']
#
# # dict(parse.parse_qsl(url)[1:])
# url = "https://metaso.cn/api/searchV2"
#
# params = {
#     'question': question,
#     "sessionId": session_id,
#     'lang': 'zh',
#     'mode': 'detail',
#     # 'url': f'https://metaso.cn/search/{sessionId}?q={q}',
#     'enableMix': 'true',
#     'scholarSearchDomain': 'all',
#     'expectedCurrentSessionSearchCount': '1',
#     'newEngine': 'true',
#     'enableImage': 'true',
#     'token': 'wr8+pHu3KYryzz0O2MaBSNUZbVLjLUYC1FR4sKqSW0p19vmcZAoEmHC72zPh/fHt4VdW84WZEx4CbSUTO9sLBF48wX95yi9MJTWNNw3kbBSs6V4qv8FOocFD2ThCrWwXPwROPpwUqLnM2uWfwtUwaw=='
# }
# payload = {}
# headers = {
#     # 'Cookie': 'JSESSIONID=4ED87E5C0CD2AF6875227D279DFFBB16; tid=b103b947-be89-40b8-b162-80fdcda60807; __eventn_id_UMO2dYNwFz=jdt3ua9m4t; __eventn_id_UMO2dYNwFz_usr=%7B%22email%22%3A%22undefined%40metasota.ai%22%2C%22created_at%22%3A%22Wed%2C%2004%20Sep%202024%2006%3A55%3A57%20GMT%22%7D; aliyungf_tc=8cfbed3e5fd53c2a81605c7dcb63d45d3114b94750922ef63e04cb5a6ceccba1; s=bdpc; usermaven_id_UMO2dYNwFz=4d3f1r1j6i; hideLeftMenu=1; newSearch=false',
#     # 'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
# }
# #
# response = requests.request("GET", url, headers=headers, data=payload, params=params)
# #
# print(response.text)
# async with httpx.AsyncClient(base_url=YUANBAO_BASE_URL, headers=headers, timeout=300) as client:
#     # chatid = (await client.post(API_GENERATE_ID)).text
#     chatid = uuid.uuid4()
#
#     async with client.stream(method="POST", url=f"{API_CHAT}/{chatid}", json=payload) as response:
#         logger.debug(response.status_code)
#         response.raise_for_status()
#
#         async for chunk in response.aiter_lines():