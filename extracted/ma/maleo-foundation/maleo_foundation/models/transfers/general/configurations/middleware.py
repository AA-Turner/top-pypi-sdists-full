from pydantic import BaseModel, Field
from typing import List

_ALLOW_METHODS: List[str] = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS"
]
_ALLOW_HEADERS: List[str] = [
    "Authorization",
    "Content-Type",
    "X-Request-Id",
    "X-Requested-At",
    "X-Signature"
]
_EXPOSE_HEADERS: List[str] = [
    "X-New-Authorization",
    "X-Process-Time",
    "X-Request-Id",
    "X-Requested-At",
    "X-Responded-At",
    "X-Signature"
]

class GeneralMiddlewareConfigurations(BaseModel):
    allow_origins: List[str] = Field(default_factory=list, description="Allowed origins")
    allow_methods: List[str] = Field(_ALLOW_METHODS, description="Allowed methods")
    allow_headers: list[str] = Field(_ALLOW_HEADERS, description="Allowed headers")
    allow_credentials: bool = Field(True, description="Allowed credentials")

class CORSMiddlewareConfigurations(BaseModel):
    expose_headers: List[str] = Field(_EXPOSE_HEADERS, description="Exposed headers")

class BaseMiddlewareConfigurations(BaseModel):
    limit: int = Field(10, description="Request limit (per 'window' seconds)")
    window: int = Field(1, description="Request limit window (seconds)")
    cleanup_interval: int = Field(60, description="Interval for middleware cleanup (seconds)")
    ip_timeout: int = Field(300, description="Idle IP's timeout (seconds)")

class MiddlewareConfigurations(BaseModel):
    general: GeneralMiddlewareConfigurations = Field(..., description="Middleware's general configurations")
    cors: CORSMiddlewareConfigurations = Field(..., description="CORS middleware's configurations")
    base: BaseMiddlewareConfigurations = Field(..., description="Base middleware's configurations")