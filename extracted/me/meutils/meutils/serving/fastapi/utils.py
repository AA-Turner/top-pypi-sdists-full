#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2023/11/28 16:51
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from starlette.datastructures import UploadFile
from starlette.requests import Request, FormData
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from fastapi import APIRouter, File, Query, Form, BackgroundTasks, Depends, HTTPException as _HTTPException, \
    Request, status


class HTTPException(_HTTPException):
    message: str = ""
    type: str = "error"
    param: Optional[Any] = None
    code: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.detail = self.detail or {
            "error": {
                "message": self.message,
                "type": self.type,
                "param": self.param,
                "code": self.code or self.status_code,
            }
        }


def get_ipaddr(request: Request) -> str:
    """
    Returns the ip address for the current request (or 127.0.0.1 if none found)
     based on the X-Forwarded-For headers.
     Note that a more robust method for determining IP address of the client is
     provided by uvicorn's ProxyHeadersMiddleware.
    """
    if "X_FORWARDED_FOR" in request.headers:
        return request.headers["X_FORWARDED_FOR"]
    else:
        if not request.client or not request.client.host:
            return "127.0.0.1"

        return request.client.host


def get_remote_address(request: Request) -> str:
    """
    Returns the ip address for the current request (or 127.0.0.1 if none found)
    """
    if not request.client or not request.client.host:
        return "127.0.0.1"

    return request.client.host


def limit(limit_value='3/second', error_message: Optional[str] = None, **kwargs):
    """
        @limit(limit_value='3/minute')
        def f(request: Request):
            return {'1': '11'}
    :return:
    """
    from slowapi.errors import RateLimitExceeded
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address

    limiter = Limiter(key_func=get_remote_address)
    return limiter.limit(limit_value=limit_value, error_message=error_message, **kwargs)


def check_api_key(auth: HTTPAuthorizationCredentials):
    api_key = auth
    if api_key is None:
        detail = {
            "error": {
                "message": "invalid_api_key",
                "type": "invalid_request_error",
                "param": None,
                "code": None,
            }
        }
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


# def parse_formdata(formdata: FormData):
#     request = formdata._dict
#     logger.debug(bjson(request))
#     # if images := form_data.getlist("image[]"):  # 数组
#     #     request["image"] = images
#     files = []
#     data = {}
#     for k, v in formdata.multi_items():  # images
#         data.setdefault(k, []).append(v)
#         # logger.debug(type(v))
#         if isinstance(v, UploadFile):
#             files.append(v)
#         else:
#             logger.debug(f"{k}: {v}")
#
#     return data

def form_to_dict(formdata: FormData, file2json: bool = False) -> Dict[str, Union[str, List[str]]]:
    """
    把表单转换成 dict；出现同名 key 时自动变成 list。
    """
    # request.form() 返回的是 FormData，它本质是个 immutable-multidict
    result: Dict[str, Union[str, List[str]]] = {}
    for key, value in formdata.multi_items():  # multi_items 会保留所有值
        if file2json and isinstance(value, UploadFile):
            _value = value.__dict__.copy()
            _value.pop('file', None)
            _value.pop('headers', None)
            logger.debug(_value)
            result[key] = _value
            continue

        if key in result:  # 出现重复 key → 转 list
            if isinstance(result[key], list):
                result[key].append(value)
            else:
                result[key] = [result[key], value]
        else:
            result[key] = value
    return result


if __name__ == '__main__':
    d = {
        "error": {
            "message": "当前分组 chatfire 下对于模型 ERNIE-Bot 无可用渠道 (request id: 20240314180638675032749TVFiqyF1)",
            "type": "new_api_error"
        }
    }
