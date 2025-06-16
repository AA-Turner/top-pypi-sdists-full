import logging
import logging.handlers
import os
import traceback
from abc import ABCMeta, abstractmethod
from contextlib import asynccontextmanager
from functools import lru_cache
from asgi_correlation_id import CorrelationIdMiddleware, CorrelationIdFilter

import dotenv
import watchtower
from beanie import init_beanie
from fastapi import FastAPI, status, Request, APIRouter
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from . import database, cache_redis
from .const import LOG_FMT, LOG_FMT_NO_DT, LOG_DT_FMT, DEFAULT_LOGGER_NAME, CORRELATION_ID_HEADER_KEY_NAME
from .exception.base_exception import InternalBaseException
from .exception.internal_exception import BadGatewayException, GatewayTimeoutException
from .ext.amazon import aws
from .http.requests import async_request
from .http.responses import async_response
from .middleware.log_request import LogRequestMiddleware
from .utils import update_dict_with_cast


class BaseFactory(metaclass=ABCMeta):
    DEFAULT_APP_NAME = ""
    API_VERSION = "v0.0.0"

    @abstractmethod
    def init_modules(self, app):
        """
        Each factory should define what modules it wants.
        """

    @abstractmethod
    async def get_document_model_list(self) -> list:
        """
        Each factory should define what model it wants.
        """

    async def init_redis(self, app, app_config):
        if app_config.REDIS_URL:
            redis_cache = cache_redis.CacheRedis(app_config.REDIS_URL)
            await redis_cache.connect()
            app.state.redis = redis_cache.client
            app.state.logger.info("Initialization redis done")
        else:
            app.state.logger.info("skip initialization redis")

    async def init_state_cache(self, app, app_config):
        """
        Each factory should define what model it wants.
        """
        pass

    async def init_state_scheduler_app(self, app, app_config):
        """
        Each factory should define what model it wants.
        """
        pass

    async def close_scheduler_app(self, app, app_config):
        """
        Each factory should define what model it wants.
        """
        pass

    @abstractmethod
    @lru_cache()
    def get_app_config(self):
        """
        Each factory should define what config it wants.
        """

    def create_app(self, title=None) -> FastAPI:

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # code to execute when app is loading
            await mongodb.connect()
            document_model_list = await self.get_document_model_list()
            await init_beanie(database=app.state.db.get_database(), document_models=document_model_list)
            app.state.logger.info("Database connected")
            await self.init_state_cache(app, self.get_app_config())
            app.state.logger.info("Initialization state cache done")
            await self.init_state_scheduler_app(app, self.get_app_config())
            app.state.logger.info("Initialization state scheduler app done")
            await self.init_redis(app, self.get_app_config())

            yield
            # code to execute when app is shutting down
            await mongodb.close()
            app.state.logger.info("Database disconnected")
            await self.close_scheduler_app(app, self)
            app.state.logger.info("State scheduler closed")

        if title is None:
            title = self.DEFAULT_APP_NAME

        if self.get_app_config().DEBUG:
            app = FastAPI(openapi_url=self.get_app_config().OPEN_API_URL, title=title,
                          debug=self.get_app_config().DEBUG, version=self.API_VERSION, lifespan=lifespan)
        else:
            app = FastAPI(openapi_url=self.get_app_config().OPEN_API_URL, title=title,
                          debug=self.get_app_config().DEBUG, version=self.API_VERSION, lifespan=lifespan, docs_url=None,
                          redoc_url=None)

        self.__load_local_config()
        app.state.config = self.get_app_config()
        self.__setup_main_logger(app, level=logging.DEBUG)
        app.state.aws_session = aws.init_app(app)
        self.__setup_cloud_log(app)
        self.__load_cloud_config(app)

        # 不重要的middleware請加在這之前
        if self.get_app_config().LOGGER_REQUEST_ENABLE:
            app.add_middleware(LogRequestMiddleware, logger=app.state.logger)


        origins = ["*"]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=[CORRELATION_ID_HEADER_KEY_NAME]
        )

        app.add_middleware(
            CorrelationIdMiddleware,
            header_name=CORRELATION_ID_HEADER_KEY_NAME,
            update_request_header=True
        )

        mongodb = database.MongoDB(self.get_app_config().DATABASE_USERNAME, self.get_app_config().DATABASE_PASSWORD,
                                   self.get_app_config().DATABASE_HOST, self.get_app_config().DATABASE_PORT,
                                   self.get_app_config().DATABASE_NAME,
                                   self.get_app_config().DATABASE_SERVER_SELECTION_TIMEOUT_MS,
                                   self.get_app_config().DATABASE_CONNECT_TIMEOUT_MS,
                                   self.get_app_config().DATABASE_AUTH_SOURCE,
                                   self.get_app_config().DATABASE_SSL, self.get_app_config().DATABASE_SSL_CA_CERTS)

        app.state.db = mongodb
        app.state.config = self.get_app_config()
        self.__init_modules(app)
        self.__init_builtin_api(app)

        @app.exception_handler(InternalBaseException)
        async def http_exception_handler(request: Request, exc: InternalBaseException):
            detail = exc.detail

            if isinstance(exc, BadGatewayException):
                if self.get_app_config().WEBHOOK_BASE_URL:
                    message = f"【{self.DEFAULT_APP_NAME}】Bad gateway, request:{request.__dict__}, exc:{exc}"
                    payload = {"text": message}
                    try:
                        await async_request(app, "POST", self.get_app_config().WEBHOOK_BASE_URL, json=payload)
                    except Exception as e:
                        app.state.logger.warn(f"Notify failure, Exception:{e}")
            elif isinstance(exc, GatewayTimeoutException):
                if self.get_app_config().WEBHOOK_BASE_URL:
                    message = f"【{self.DEFAULT_APP_NAME}】Gateway timeout, request:{request.__dict__}, exc:{exc}"
                    payload = {"text": message}
                    try:
                        await async_request(app, "POST", self.get_app_config().WEBHOOK_BASE_URL, json=payload)
                    except Exception as e:
                        app.state.logger.warn(f"Notify failure, Exception:{e}")

            return await async_response(data=detail.get("data"), code=detail.get("code"), message=detail.get("message"),
                                        status_code=exc.status_code)

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            data = {"detail": exc.errors()}
            if exc.body:
                data["body"] = exc.body
            return await async_response(data=data,
                                        code="error_unprocessable_entity", message="Validation failed",
                                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

        @app.exception_handler(Exception)
        async def http_exception_handler(request: Request, exc: Exception):
            app.state.logger.warn(f"Exception, request:{request.__dict__}, exc:{exc}")
            app.state.logger.warn(traceback.format_exc())
            if self.get_app_config().WEBHOOK_BASE_URL:
                message = f"【{self.DEFAULT_APP_NAME}】Unprocessed Exception, request:{request.__dict__}, exc:{exc}"
                payload = {"text": message}
                try:
                    await async_request(app, "POST", self.get_app_config().WEBHOOK_BASE_URL, json=payload)
                except Exception as e:
                    app.state.logger.warn(f"Notify failure, Exception:{e}")

            return await async_response(code="error_internal_server", message="Internal server error",
                                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return app

    def __load_local_config(self):
        dotenv.load_dotenv(override=True)
        update_dict_with_cast(self.get_app_config(), os.environ)

    def __load_cloud_config(self, app):
        if not app.state.aws_session or not self.get_app_config().AWS_PARAMETER_PATH_PREFIX:
            app.state.logger.warn("No AWS session or Parameter Storage configuration, ignore cloud config")
            return

        cloud_conf = {}

        params = {
            "Path": self.get_app_config().AWS_PARAMETER_PATH_PREFIX,
            "Recursive": True,
            "WithDecryption": True
        }

        # AWS only give us 10 parameters per api call
        ssm_client = app.state.aws_session.client("ssm")
        while True:
            result = ssm_client.get_parameters_by_path(**params)
            cloud_conf.update({para["Name"].split("/")[-1]: para["Value"] for para in result["Parameters"]})
            if not result.get("NextToken"):
                break
            params.update({"NextToken": result["NextToken"]})

        update_dict_with_cast(self.get_app_config(), cloud_conf)

    def __init_modules(self, app):
        self.init_modules(app)

    def __setup_main_logger(self, app, logger_name=DEFAULT_LOGGER_NAME, level=logging.INFO):
        logger = self.__setup_logger(app, logger_name, level)
        app.state.logger = logger

    #
    def __setup_logger(self, app, logger_name, level=logging.INFO):
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(fmt=LOG_FMT))
        stream_handler.addFilter(CorrelationIdFilter())
        logger.addHandler(stream_handler)

        return logger

    def __setup_cloud_log(self, app):
        if app.state.aws_session and self.get_app_config().AWS_LOGGROUP_NAME:
            logs_client = app.state.aws_session.client("logs")
            watchtower_handler = watchtower.CloudWatchLogHandler(
                log_group_name=self.get_app_config().AWS_LOGGROUP_NAME,
                boto3_client=logs_client, create_log_group=False)
            watchtower_handler.setFormatter(logging.Formatter(fmt=LOG_FMT_NO_DT, datefmt=LOG_DT_FMT))
            watchtower_handler.addFilter(CorrelationIdFilter())
            app.state.logger.addHandler(watchtower_handler)

    def __init_builtin_api(self, app):
        router = APIRouter(prefix=f"/system", tags=["system"])

        @router.get('/health')
        async def health():
            return await async_response()

        @router.get('/hello')
        async def hello():
            return await async_response(data={"API version": app.version})

        app.include_router(router)
