import httpx
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
from typing import AsyncGenerator, Generator
from maleo_foundation.types import BaseTypes
from maleo_foundation.utils.logging import ClientLogger, SimpleConfig

class BearerAuth(httpx.Auth):
    def __init__(self, token: str) -> None:
        self._auth_header = self._build_auth_header(token)

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = self._auth_header
        yield request

    def _build_auth_header(self, token: str) -> str:
        return f"Bearer {token}"

class ClientHTTPControllerManager:
    def __init__(self, url: str) -> None:
        self._client = httpx.AsyncClient()
        self._url = url

    async def _client_handler(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        """Reusable generator for client handling."""
        if self._client is None or (self._client is not None and self._client.is_closed):
            self._client = httpx.AsyncClient()
        yield self._client

    async def inject_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        return self._client_handler()

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        """
        Async context manager for manual HTTP client handling.
        Supports `async with HTTPClientManager.get() as client:`
        """
        async for client in self._client_handler():
            yield client

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    @property
    def url(self) -> str:
        return self._url

    async def dispose(self) -> None:
        await self._client.aclose()

class ClientControllerManagers(BaseModel):
    http:ClientHTTPControllerManager = Field(..., description="HTTP Client Controller")

    class Config:
        arbitrary_types_allowed=True

class ClientHTTPController:
    def __init__(self, manager:ClientHTTPControllerManager):
        self._manager = manager

    @property
    def manager(self) -> ClientHTTPControllerManager:
        return self._manager

class ClientServiceControllers(BaseModel):
    http:ClientHTTPController = Field(..., description="HTTP Client Controller")

    class Config:
        arbitrary_types_allowed=True

class ClientControllers(BaseModel):
    #* Reuse this class while also adding all controllers of the client
    class Config:
        arbitrary_types_allowed=True

class ClientService:
    def __init__(self, logger:ClientLogger):
        self._logger = logger

    @property
    def controllers(self) -> ClientServiceControllers:
        raise NotImplementedError()

    @property
    def logger(self) -> ClientLogger:
        return self._logger

class ClientServices(BaseModel):
    #* Reuse this class while also adding all the services of the client
    class Config:
        arbitrary_types_allowed=True

class ClientManager:
    def __init__(
        self,
        key: str,
        name: str,
        log_config: SimpleConfig,
        service_key: BaseTypes.OptionalString = None
    ) -> None:
        self._key = key
        self._name = name
        self._log_config = log_config
        self._service_key = service_key
        self._initialize_logger()
        self._logger.info("Initializing client manager")

    def _initialize_logger(self) -> None:
        self._logger = ClientLogger(
            client_key=self._key,
            service_key=self._service_key,
            **self._log_config.model_dump()
        )

    @property
    def key(self) -> str:
        return self._key

    @property
    def name(self) -> str:
        return self._name

    @property
    def logger(self) -> ClientLogger:
        return self._logger

    def _initialize_services(self) -> None:
        #* Initialize services
        #! This initialied an empty services. Extend this function in the actual class to initialize all services.
        self._services = ClientServices()

    @property
    def services(self) -> ClientServices:
        return self._services

    @property
    def credentials(self):
        raise NotImplementedError()

    @property
    def client(self):
        raise NotImplementedError()