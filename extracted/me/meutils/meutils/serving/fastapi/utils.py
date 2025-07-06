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

from starlette.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from fastapi import APIRouter, File, UploadFile, Query, Form, BackgroundTasks, Depends, HTTPException as _HTTPException, \
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


if __name__ == '__main__':
    d = {
        "error": {
            "message": "当前分组 chatfire 下对于模型 ERNIE-Bot 无可用渠道 (request id: 20240314180638675032749TVFiqyF1)",
            "type": "new_api_error"
        }
    }
