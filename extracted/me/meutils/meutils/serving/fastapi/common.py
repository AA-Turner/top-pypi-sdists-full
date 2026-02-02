#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/5/26 09:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://geek-docs.com/fastapi/fastapi-questions/279_fastapi_uvicorn_python_run_both_http_and_https.html
# 请求限制 https://github.com/Unstructured-IO/pipeline-paddleocr/blob/main/prepline_paddleocr/api/paddleocr.py
# todo: 增加apikey、增加调用频次
# 中间件 https://mp.weixin.qq.com/s/1XS5hSKEVaTeUH8oXik8Hw

# check api https://github.com/eosphoros-ai/DB-GPT/blob/04af30e3db9bf5e7a60ab55ade01dc8ddeba06f8/dbgpt/app/openapi/api_v2.py#L46

from meutils.pipe import *
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException

from meutils.serving.fastapi.exceptions.http_error import http_error_handler, chatfire_api_exception_handler
from meutils.serving.fastapi.exceptions.validation_error import http422_error_handler, validation_exception_handler



class App(FastAPI):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # openapi_url = "/api/v1/openapi.json"
        self.servers = [{"url": ""}]

        self.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

        # 服务器内部错误 500
        self.add_exception_handler(Exception, chatfire_api_exception_handler)  # 500

        # HTTPException
        self.add_exception_handler(HTTPException, http_error_handler)

        # RequestValidationError
        self.add_exception_handler(RequestValidationError, http422_error_handler)
        self.add_exception_handler(RequestValidationError, validation_exception_handler)  # 500

    def include_router(self, router, prefix='', **kwargs):
        """
            from fastapi import FastAPI, APIRouter
            router = APIRouter(route_class=LoggingRoute)

        :param router:
        :param prefix:
        :param kwargs:
        :return:
        """

        super().include_router(router, prefix=prefix, **kwargs)

    def run(self, app=None, host="0.0.0.0", port=8000, workers=1, access_log=True, reload=False, **kwargs):
        """

        :param app:
            f"{Path(__file__).stem}:{app}"
            app字符串可开启热更新 reload
        :param host:
        :param port:
        :param workers:
        :param access_log:
        :param kwargs:
        :return:
        """

        import uvicorn

        uvicorn.config.LOGGING_CONFIG['formatters']['access']['fmt'] = f"""
        🔥 %(asctime)s - %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s
        """.strip()
        uvicorn.run(
            app if app else self,  #
            host=host, port=port, workers=workers, access_log=access_log, reload=reload, app_dir=None,
            **kwargs
        )

    def sentry_init(self):
        """https://qyyshop.com/info/767857.html"""
        import sentry_sdk

        sentry_sdk.init(
            dsn="https://YourPublicKey@o0.ingest.sentry.io/0",
            enable_tracing=True,
        )


if __name__ == '__main__':
    from fastapi import FastAPI, APIRouter, Request
    from meutils.serving.fastapi.utils import limit

    app = App()
    router = APIRouter()  # 怎么限流？


    # @router.get('/xx', name='xxxx')
    # @limit(limit_value='3/minute', error_message='请联系我')
    # def f(request: Request):
    #     return {'1': '11'}

    @app.get("/test")
    def test_endpoint():
        # 这里故意触发一个HTTPException来演示错误处理
        raise HTTPException(status_code=505, detail="Item not found")

        # raise Exception("test")


    app.include_router(router)
    app.run(port=8899)
