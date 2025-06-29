from pydantic import BaseModel, Field
from maleo_foundation.utils.logging import MiddlewareLogger, ServiceLogger
from .cache import CacheConfigurations
from .client import ClientConfigurations
from .database import DatabaseConfigurations
from .middleware import (
    MiddlewareRuntimeConfigurations,
    MiddlewareStaticConfigurations,
    MiddlewareConfigurations
)
from .service import ServiceConfigurations

class RuntimeConfigurations(BaseModel):
    service: ServiceConfigurations = Field(..., description="Service's configurations")
    middleware: MiddlewareRuntimeConfigurations = Field(..., description="Middleware's runtime configurations")
    database: DatabaseConfigurations = Field(..., description="Database's configurations")

    class Config:
        arbitrary_types_allowed=True

class StaticConfigurations(BaseModel):
    middleware: MiddlewareStaticConfigurations = Field(..., description="Middleware's static configurations")
    client: ClientConfigurations = Field(..., description="Client's configurations")

    class Config:
        arbitrary_types_allowed=True

class Configurations(BaseModel):
    service: ServiceConfigurations = Field(..., description="Service's configurations")
    middleware: MiddlewareConfigurations = Field(..., description="Middleware's configurations")
    cache: CacheConfigurations = Field(..., description="Cache's configurations")
    database: DatabaseConfigurations = Field(..., description="Database's configurations")
    client: ClientConfigurations = Field(..., description="Client's configurations")

    class Config:
        arbitrary_types_allowed=True

class Loggers(BaseModel):
    application: ServiceLogger = Field(..., description="Application logger")
    repository: ServiceLogger = Field(..., description="Repository logger")
    database: ServiceLogger = Field(..., description="Database logger")
    middleware: MiddlewareLogger = Field(..., description="Middleware logger")

    class Config:
        arbitrary_types_allowed=True