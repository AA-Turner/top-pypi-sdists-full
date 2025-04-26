#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : json_utils
# @Time         : 2021/4/22 1:51 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : pd.io.json.json_normalize

# https://mangiucugna.github.io/json_repair/
# https://jsonpath.com/

import jsonpath

# json https://blog.csdn.net/freeking101/article/details/103048514
# https://github.com/ijl/orjson#quickstart
# https://jmespath.org/tutorial.html
# https://goessner.net/articles/JsonPath/
# https://www.jianshu.com/p/3f5b9cc88bde

# todo: jsonpath jmespath
# https://blog.csdn.net/be5yond/article/details/118976017
# https://blog.csdn.net/weixin_44799217/article/details/127590589

from meutils.pipe import *
from json_repair import repair_json


def json2class(dic, class_name='Test'):
    s = f"""class {class_name}(BaseModel):"""
    for k, v in dic.items():
        _type = type(v).__name__
        if isinstance(_type, str):
            v = f"'{v}'"
        s += f"\n\t{k}: {_type} = {v}"

    print(s)


@lru_cache(1024)
def json_loads(s):
    if isinstance(s, bytes):
        s = s.decode()
    try:
        return json.loads(s.replace("'", '"'))

    except Exception as e:
        logger.warning(e)

        return eval(s)


def json_path(obj, expr):  # todo: 缓存
    """$..["keywords","query","search_result"]"""
    if isinstance(obj, dict):
        pass
    elif isinstance(obj, str):
        obj = json_repair.loads(obj)
    elif isinstance(obj, bytes):
        obj = json_repair.loads(obj.decode())
    elif isinstance(obj, BaseModel):
        obj = obj.dict()

    return jsonpath.jsonpath(obj, expr=expr)


if __name__ == '__main__':
    print(json_path({"a": 1}, expr='$.a'))
    print(json_path("""{"a": 1}""", expr='$.a'))

    json_string = """{"a": 1}"""


    class A(BaseModel):
        a: int = 1


    print(json_path(A(), '$.a'))
