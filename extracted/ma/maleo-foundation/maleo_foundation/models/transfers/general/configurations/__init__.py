from pydantic import BaseModel, ConfigDict, Field
from maleo_foundation.utils.logging import (
    ApplicationLogger,
    CacheLogger,
    DatabaseLogger,
    MiddlewareLogger,
    RepositoryLogger,
    ServiceLogger
)
from .cache import CacheConfigurations
from .client import ClientConfigurations
from .database import DatabaseConfigurations
from .middleware import MiddlewareConfigurations
from .service import ServiceConfigurations

class Configurations(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cache: CacheConfigurations = Field(..., description="Cache's configurations")
    client: ClientConfigurations = Field(..., description="Client's configurations")
    database: DatabaseConfigurations = Field(..., description="Database's configurations")
    middleware: MiddlewareConfigurations = Field(..., description="Middleware's configurations")
    service: ServiceConfigurations = Field(..., description="Service's configurations")

class Loggers(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    application: ApplicationLogger = Field(..., description="Application logger")
    cache: CacheLogger = Field(..., description="Cache logger")
    database: DatabaseLogger = Field(..., description="Database logger")
    middleware: MiddlewareLogger = Field(..., description="Middleware logger")
    repository: RepositoryLogger = Field(..., description="Repository logger")
    service: ServiceLogger = Field(..., description="Service logger")