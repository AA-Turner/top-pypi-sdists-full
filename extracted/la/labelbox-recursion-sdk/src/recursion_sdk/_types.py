"""Shared request, response, and exception types."""

from dataclasses import dataclass
from typing import BinaryIO

import httpx

from ._generated.models import RecursionApiError


class Unset:
    """An omitted optional parameter or body, distinct from explicit null."""

    __slots__ = ()


UNSET = Unset()


@dataclass(frozen=True)
class Upload:
    """A multipart file, retaining its filename and media type."""

    filename: str
    content: bytes | BinaryIO
    content_type: str = "application/octet-stream"


@dataclass(frozen=True)
class ApiResponse[T]:
    """Typed response data and the original HTTPX response."""

    data: T
    response: httpx.Response


class RecursionAPIError(Exception):
    """A declared API error whose envelope passed canonical validation."""

    def __init__(self, error: RecursionApiError, response: httpx.Response) -> None:
        self.error = error
        self.response = response
        super().__init__(f"HTTP {response.status_code}: {self.code}: {self.message}")

    @property
    def status_code(self) -> int:
        return self.response.status_code

    @property
    def code(self) -> str:
        return self.error.root.code

    @property
    def message(self) -> str:
        return self.error.root.message


class RecursionContractError(ValueError):
    """A request or response that cannot inhabit the canonical API contract."""

    def __init__(
        self,
        operation_id: str,
        message: str,
        *,
        response: httpx.Response | None = None,
    ) -> None:
        self.operation_id = operation_id
        self.response = response
        super().__init__(f"{operation_id}: {message}")
