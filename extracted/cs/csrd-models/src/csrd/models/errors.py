"""Minimal REST API error models extracted from REST API error models."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from pydantic import ConfigDict, TypeAdapter
from pydantic.alias_generators import to_camel

CONFIG = ConfigDict(alias_generator=to_camel, populate_by_name=True, arbitrary_types_allowed=True)


class SerializerMixin:
    def as_dict(self, **kwargs: Any) -> dict[str, Any]:
        result = TypeAdapter(type(self)).dump_python(self, **kwargs)
        return dict(result)  # type: ignore[arg-type]


@dataclass
class APIVersion:
    """API version information for error responses."""

    requested: str | None = None
    served: str | None = None

    __pydantic_config__ = CONFIG


@dataclass
class ErrorMeta:
    """Metadata for error responses."""

    status: int = field(metadata={"description": "HTTP status code"})
    error: str = field(metadata={"description": "Error message"})
    path: str = field(metadata={"description": "Request path"})
    api_version: APIVersion = field(metadata={"description": "API version information"})
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC), metadata={"description": "Error timestamp"}
    )
    method: str | None = field(default=None, metadata={"description": "HTTP method"})
    request_id: str | None = field(
        default=None, metadata={"description": "Unique request identifier"}
    )

    __pydantic_config__ = CONFIG


@dataclass
class Error:
    """Individual error details."""

    title: str = field(metadata={"description": "Error title"})
    detail: str | None = field(default=None, metadata={"description": "Detailed error description"})
    code: str | None = field(
        default=None, metadata={"description": "Application-specific error code"}
    )

    __pydantic_config__ = CONFIG


@dataclass
class APIErrorResponse(SerializerMixin):
    """Standard API error response format."""

    meta: ErrorMeta = field(metadata={"description": "Error metadata"})
    errors: list[Error] = field(metadata={"description": "List of errors"})

    __pydantic_config__ = CONFIG


__all__ = ("APIErrorResponse", "APIVersion", "Error", "ErrorMeta", "SerializerMixin")
