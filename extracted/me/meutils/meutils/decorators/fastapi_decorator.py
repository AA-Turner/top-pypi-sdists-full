#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : fastapi
# @Time         : 2024/1/8 16:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from functools import wraps, partial
from fastapi import HTTPException


def catch_exceptions(func=None, *, exception_type=Exception, status_code=404):
    if func is None:
        return partial(catch_exceptions, exception_type=exception_type, status_code=status_code)

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except exception_type as e:
            raise HTTPException(status_code=status_code, detail=f"Error: {e}")

    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exception_type as e:
            raise HTTPException(status_code=status_code, detail=f"Error: {e}")

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper


def catch_exceptions_(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except CustomException as e:
            return JSONResponse(
                status_code=418,
                content={"message": f"An error occurred: {str(e)}"},
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"message": "An unexpected error occurred."}
            )

    return wrapper


# 然后在你的路由中使用装饰器：
# @app.get("/items/{item_id}")
# @catch_exceptions
# async def read_item(item_id: int):
#     # 你的业务逻辑
#     pass


if __name__ == '__main__':
    from meutils.serving.fastapi import App
    from fastapi import Depends

    app = App()


    async def catch_exceptions(exception_type=Exception, status_code=404):
        try:
            yield
        except exception_type as e:
            raise HTTPException(status_code=status_code, detail=f"Error: {e}")


    from fastapi import FastAPI, HTTPException, Depends, Request
    from starlette.responses import JSONResponse



    async def catch_exceptions(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except IOError as e:
            return JSONResponse(status_code=500, content={"detail": f"IOError: {e}"})


    @app.middleware("http")
    async def catch_exceptions_middleware(request: Request, call_next):
        return await catch_exceptions(request, call_next)


    @app.get("/test")
    def test_endpoint(file_id: str):
        # Your endpoint logic here
        raise Exception("test")
        # return {"file_id": file_id}



    # @app.get("/test_plus")
    # def test_endpoint(file_id: str, _=Depends(catch_exceptions(exception_type=IOError, status_code=500))):
    #     # Your endpoint logic here
    #     return {"file_id": file_id}


    # @app.get("/test")
    # @catch_exceptions(exception_type=IOError, status_code=500)
    # def f(file_id: str):
    #     logger.debug(file_id)
    #     # raise Exception("test")
    #
    #
    # @app.get("/{file_id}")
    # @catch_exceptions(status_code=1)
    # def f(file_id: str):
    #     logger.debug(file_id)
    #     raise Exception("test")


    app.run(port=9000)
