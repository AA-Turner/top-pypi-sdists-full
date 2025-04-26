#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : logger
# @Time         : 2023/8/21 09:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/

from fastapi import Request, Response
from fastapi.routing import APIRoute
from gunicorn.glogging import Logger

from starlette.background import BackgroundTask
from starlette.responses import Response, StreamingResponse

from meutils.pipe import *
from loguru import logger


####################################################################################
class LoggerSettings(BaseModel):
    sink: Any = os.getenv("LOG_SINK")  # todo: 邮件 飞书等等

    level: str = logging.getLevelName(os.getenv("LOG_LEVEL", "DEBUG"))
    serialize: bool = True if os.getenv("LOG_SERIALIZE", '0') != '0' else False
    rotation: str = os.getenv("LOG_ROTATION", '00:00')
    retention: str = os.getenv("LOG_RETENTION", '7 days')


settings = LoggerSettings()


####################################################################################

def init_logger() -> None:
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(settings.level)

    # Remove all log handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        # Do not remove gunicorn loggers
        if "gunicorn" not in name:
            logging.getLogger(name).handlers = []
            logging.getLogger(name).propagate = True

    # Configure sqlalchemy engine logger, which by default is set to WARNING level
    logging.getLogger("sqlalchemy.engine").setLevel(settings.level)

    # Configure logger (again) if gunicorn is not used
    handlers = [{"sink": sys.stdout}]
    if settings.sink:  # 覆盖
        handlers = [
            {
                "sink": settings.sink,
                "level": settings.level,
                "serialize": settings.serialize,
                "enqueue": True,
                "rotation": settings.rotation,
                "retention": settings.retention
            }
        ]
    logger.configure(handlers=handlers)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class GunicornLogger(Logger):
    def setup(self, cfg) -> None:
        handler = InterceptHandler()

        # Add log handler to logger and set log level
        self.error_log.addHandler(handler)
        self.error_log.setLevel(settings.level)
        self.access_log.addHandler(handler)
        self.access_log.setLevel(settings.level)

        # Configure logger before gunicorn starts logging
        handlers = [{"sink": sys.stdout, "level": settings.level, "serialize": settings.serialize}]
        if settings.sink:  # 覆盖
            handlers = [
                {
                    "sink": settings.sink,
                    "level": settings.level,
                    "serialize": settings.serialize,
                    "enqueue": True,
                    "rotation": settings.rotation,
                    "retention": settings.retention
                }
            ]
        logger.configure(handlers=handlers)


class LoggingRoute(APIRoute):
    """
    # Use this for
    # router = APIRouter(route_class=LoggingRoute)
    # when you want to split up your routes and use include_router()
    # https://fastapi.tiangolo.com/advanced/custom-request-and-route/#custom-apiroute-class-in-a-router
    """

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            id = str(uuid.uuid4())
            req_body = await request.body()
            req_info = {
                "request": {
                    "id": id,
                    "method": request.method,
                    "path": request.url.path,
                    "ip": request.client.host,
                    "body": req_body
                }
            }

            before = time.perf_counter()
            response = await original_route_handler(request)
            duration = (time.perf_counter() - before) * 1000
            duration = f"{duration:0.2f}ms"
            response.headers["X-Response-Time"] = duration

            res_info = {
                "response": {
                    "id": id,
                    "status": "successful" if response.status_code < 400 else "failed",
                    "status_code": response.status_code,
                    "duration": duration,
                }
            }

            if isinstance(response, StreamingResponse):  # todo: body_iterator
                res_body = b''
                async for item in response.body_iterator:
                    res_body += item
                res_info["response"]["body"] = res_body

                task = BackgroundTask(self.log_request_response_info, req_info, res_info)

                return Response(
                    content=res_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type,
                    background=task
                )
            else:
                res_body = response.body
                res_info["response"]["body"] = res_body
                response.background = BackgroundTask(self.log_request_response_info, req_info, res_info)

                return response

        return custom_route_handler

    def log_request_response_info(self, req_info, res_info):
        logger.info(req_info)
        logger.info(res_info)
