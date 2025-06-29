from fastapi import FastAPI
from maleo_foundation.client.manager import MaleoFoundationClientManager
from maleo_foundation.models.schemas import BaseGeneralSchemas
from maleo_foundation.models.transfers.general.configurations.middleware \
    import MiddlewareConfigurations
from maleo_foundation.middlewares.authentication import add_authentication_middleware
from maleo_foundation.middlewares.base import add_base_middleware
from maleo_foundation.middlewares.cors import add_cors_middleware
from maleo_foundation.utils.logging import MiddlewareLogger

class MiddlewareManager:
    def __init__(
        self,
        app: FastAPI,
        configurations: MiddlewareConfigurations,
        keys: BaseGeneralSchemas.RSAKeys,
        logger: MiddlewareLogger,
        maleo_foundation: MaleoFoundationClientManager
    ):
        self._app = app
        self._configurations = configurations
        self._keys = keys
        self._logger = logger
        self._maleo_foundation = maleo_foundation

    def add_all(self):
        self.add_cors()
        self.add_base()
        self.add_authentication()

    def add_cors(self) -> None:
        add_cors_middleware(
            app=self._app,
            allow_origins=self._configurations.general.allow_origins,
            allow_methods=self._configurations.general.allow_methods,
            allow_headers=self._configurations.general.allow_headers,
            allow_credentials=self._configurations.general.allow_credentials,
            expose_headers=self._configurations.cors.expose_headers
        )

    def add_base(self):
        add_base_middleware(
            app=self._app,
            keys=self._keys,
            logger=self._logger,
            maleo_foundation=self._maleo_foundation,
            allow_origins=self._configurations.general.allow_origins,
            allow_methods=self._configurations.general.allow_methods,
            allow_headers=self._configurations.general.allow_headers,
            allow_credentials=self._configurations.general.allow_credentials,
            limit=self._configurations.base.limit,
            window=self._configurations.base.window,
            cleanup_interval=self._configurations.base.cleanup_interval,
            ip_timeout=self._configurations.base.ip_timeout
        )

    def add_authentication(self):
        add_authentication_middleware(
            app=self._app,
            keys=self._keys,
            maleo_foundation=self._maleo_foundation
        )