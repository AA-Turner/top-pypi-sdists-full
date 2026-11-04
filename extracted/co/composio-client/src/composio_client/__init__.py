"""The official Python library for the Composio API.

Generated from the v3.1 OpenAPI spec with hey-api (pydantic models) over a
hand-written httpx runtime. Drop-in-shaped against the Stainless
``composio-client`` package with relaxed types — see MIGRATION.md.
"""

from __future__ import annotations

from . import types as types
from ._auth import (
    AsyncCredential,
    Auth,
    AuthMode,
    AutoAuth,
    Credential,
    NoAuth,
    OrganizationAuth,
    ProjectAuth,
    Scope,
    UserAuth,
    auth_from_credentials,
)
from ._base_model import BaseModel
from ._client import ENVIRONMENTS, AsyncComposio, Composio, EnvironmentMap
from ._deprecation import ComposioDeprecationWarning
from ._exceptions import (
    APIConnectionError,
    APIError,
    APIResponseValidationError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ComposioError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    UnprocessableEntityError,
)
from ._files import file_from_path
from ._identity import ClientIdentity
from ._types import (
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    NOT_GIVEN,
    DefaultAsyncHttpxClient,
    DefaultHttpxClient,
    NoneType,
    NotGiven,
    Omit,
    RequestOptions,
    Timeout,
    not_given,
    omit,
)
from ._version import __version__

__title__ = "composio_client"

__all__ = [
    "types",
    "Composio",
    "AsyncComposio",
    "ClientIdentity",
    "Auth",
    "AuthMode",
    "NoAuth",
    "ProjectAuth",
    "UserAuth",
    "OrganizationAuth",
    "AutoAuth",
    "Credential",
    "AsyncCredential",
    "Scope",
    "auth_from_credentials",
    "RequestOptions",
    "NoneType",
    "NotGiven",
    "NOT_GIVEN",
    "not_given",
    "Omit",
    "omit",
    "Timeout",
    "BaseModel",
    "DEFAULT_TIMEOUT",
    "DEFAULT_MAX_RETRIES",
    "DefaultHttpxClient",
    "DefaultAsyncHttpxClient",
    "ENVIRONMENTS",
    "EnvironmentMap",
    "file_from_path",
    "__title__",
    "__version__",
    "ComposioDeprecationWarning",
    "ComposioError",
    "APIError",
    "APIStatusError",
    "APIConnectionError",
    "APITimeoutError",
    "APIResponseValidationError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
]
