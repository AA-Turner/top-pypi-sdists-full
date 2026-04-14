"""Desktop Agent API SDK - v1.0.0"""

from . import api, errors, models
from .client import AsyncClient, Client
from .errors import (
    APIError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    RateLimitError,
    ServiceUnavailableError,
    UnauthorizedError,
    UnprocessableEntityError,
)

__version__ = "1.0.0"
__generator_version__ = None

__all__ = [
    # Clients
    "Client",
    "AsyncClient",
    # Modules
    "api",
    "models",
    "errors",
    # Version info
    "__version__",
    "__generator_version__",
    # Error types for convenience
    "APIError",
    "BadRequestError",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
    "ServiceUnavailableError",
]
