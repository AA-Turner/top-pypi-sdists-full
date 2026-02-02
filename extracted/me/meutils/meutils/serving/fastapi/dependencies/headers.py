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

# from meutils.pipe import *
from meutils.str_utils.json_utils import repair_json


def get_headers(request: Request):
    dic = dict(request.headers)
    _dic = {k.replace('-', '_'): v for k, v in dic.items()}  # 增强兼容性
    dic = {**dic, **_dic}

    if x_headers := dic.get('x-headers'):  # -H 'x-headers: {a: 1}' todo
        dic['x-headers'] = repair_json(x_headers, return_objects=True)

        # logger.debug(dic['x-headers'])
    if x_model_mapper := dic.get('x-model-mapper'):  #
        dic['x-model-mapper'] = eval(f"lambda r: {x_model_mapper}")

    if _ := dic.get("param_override"):
        dic["param_override"] = repair_json(_, return_objects=True)

    return dic


if __name__ == '__main__':
    def get_headers():
        dic = {
            "x-headers": "{a:1}",

            'x-model-mapper': "r.get('a')"
        }
        # upstream_base_url = headers.get('upstream-base-url')
        if x_headers := dic.get('x-headers'):  # -H 'x-headers: {a: 1}' todo
            dic['x-headers'] = repair_json(x_headers, return_objects=True)

        if x_model_mapper := dic.get('x-model-mapper'):  #
            dic['x-model-mapper'] = eval(f"lambda r: {x_model_mapper}")

        return dic


    print(get_headers())
