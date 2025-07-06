#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : headers
# @Time         : 2025/2/23 00:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from fastapi import FastAPI, Request, Depends, HTTPException
from typing import Dict, Optional


def get_headers(request: Request):
    dic = dict(request.headers)
    _dic = {k.replace('-', '_'): v for k, v in dic.items()}

    return {**dic, **_dic}


if __name__ == '__main__':
    def get_headers():
        d = {"upstream-base-url": 'xx'}
        d = {}
        dic = {}
        # upstream_base_url = headers.get('upstream-base-url')
        if d:
            dic = {k.replace('-', '_'): v for k, v in d.items()}

        return {**d, **dic}


    print(get_headers())
