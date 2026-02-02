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
from json_repair import repair_json as _repair_json


@lru_cache()
def repair_json(json_str, **kwargs):
    return _repair_json(json_str, **kwargs)


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
    """
    $..["keywords","query","search_result"]

    python =>     $..[keywords,query,search_result]

    """
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
    # print(json_path({"a": 1}, expr='$.a'))
    # print(json_path("""{"a": 1}""", expr='$.a'))
    #
    # json_string = """{"a": 1}"""

    class A(BaseModel):
        a: int = 1


    data = {
        "id": "cgt-20250613173405-qnpqg",
        "model": "doubao-seedance-1-0-pro-250528",
        "status": "succeeded",
        "content": {
            "video_url": "https://ark-content-generation-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-1-0-pro/02174980724664200000000000000000000ffffac182c177b9d12.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYjg3ZjNlOGM0YzQyNGE1MmI2MDFiOTM3Y2IwMTY3OTE%2F20250613%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20250613T093454Z&X-Tos-Expires=86400&X-Tos-Signature=bc080dc9e02282dbe10c82e04c59ac1ed4afb67cbec8aa0506357540f9d47fc4&X-Tos-SignedHeaders=host"
        },
        "usage": {
            "completion_tokens": 245388,
            "total_tokens": 245388
        },
        "created_at": 1749807246,
        "updated_at": 1749807294
    }

    # print(json_path(data, expr='$..[url,image_url,video_url]'))

    # print(repair_json('{a: 1}', return_objects=True))
    # print(type(repair_json('{a: 1}', return_objects=True)))
    # print(repair_json('{\\"thinking\\":{\\"type\\":\\"enabled\\"}}', return_objects=True)) # 错

    data =  {
        "data": [
            {
                "taskType": "videoInference",
                "taskUUID": "8a5a1c09-d0a5-4b1b-9b67-8943cacc935f"
            }
        ]
    }


    # print(json_path(data, expr='$..taskUUID'))



    repair_json("{a:b;a:c}")
    from toon_python import encode
