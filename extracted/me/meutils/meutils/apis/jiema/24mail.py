#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : mail
# @Time         : 2024/7/26 10:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : http://24mail.chacuo.net/
import jsonpath

from meutils.decorators.retry import retrying
from meutils.pipe import *

BASE_URL = "http://24mail.chacuo.net/"

url = "http://24mail.chacuo.net/"

headers = {
    'Proxy-Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'sid=766b7f090e655c5d25862065119c206ff95e75ce',  # 会变
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}


# payload = {
#     'data': 'gmzavp71582',
#     'type': 'refresh',
#     'arg': '',
#
# }

# response = requests.request("POST", url, headers=headers, data=payload)
# pprint(response.text)
#
# pprint(response.json())


@retrying(5)
def get_mail():
    params = {
        'type': 'renew',
        'arg': 'd=chacuo.net_f=313303303@qq.com'
    }

    response = httpx.post(url, headers=headers, params=params)
    if response.is_success:
        data = response.json()  # {'status': 1, 'info': 'ok', 'data': ['mphbkx61540']}
        return f"{data.get('data')[0]}@chacuo.net"

    response.raise_for_status()


@retrying(8, min=3, max=5)
def get_message(mail: str = 'gmzavp71582'):
    params = {
        'data': mail.split('@')[0],
        'type': 'refresh',
        'arg': 'd=chacuo.net_f=313303303@qq.com'
    }

    response = httpx.post(url, headers=headers, params=params)
    if response.is_success:
        data = response.json()

        logger.debug(data)

        mail_data = data.get('data')[0]['list'][0]
        mail_id = mail_data['MID']
        params = {
            'data': mail,
            'type': 'mailinfo',
            'arg': f'f={mail_id}'
        }
        response = httpx.post(url, headers=headers, params=params)
        if response.is_success:
            data = jsonpath.jsonpath(response.json(), "$..DATA.0")
            logger.debug(data)
            if isinstance(data, list):
                codes = re.compile(r'[0-9]{6}').findall(str(data))
                return codes and codes[0]  # [0-9]{6} 6位数
            raise Exception(response.text)
        response.raise_for_status()
    response.raise_for_status()


# uodqvl17068@chacuo.net

if __name__ == '__main__':
    mail = get_mail()
    get_message(mail)
    # print(get_message('alijoy09318'))
    # get_message("dkqavh03792@chacuo.net")
    # message = get_message('dkqavh03792')
