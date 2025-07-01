from pydantic import BaseModel, ConfigDict, Field
from maleo_foundation.utils.logging import MiddlewareLogger, ServiceLogger
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

    application: ServiceLogger = Field(..., description="Application logger")
    repository: ServiceLogger = Field(..., description="Repository logger")
    database: ServiceLogger = Field(..., description="Database logger")
    middleware: MiddlewareLogger = Field(..., description="Middleware logger")