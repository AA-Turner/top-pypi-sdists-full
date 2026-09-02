"""Shared provider protocol, transport seam, and request policy."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Protocol, runtime_checkable

from ..generation import GenerationRequest, GenerationResult, ModelInfo


@dataclass(frozen=True, slots=True)
class RequestPolicy:
    """Bounded HTTP behavior for an explicit provider operation."""

    timeout: float = 120.0
    max_attempts: int = 1
    backoff_seconds: float = 0.5
    max_backoff_seconds: float = 8.0
    max_retry_after_seconds: float = 30.0
    max_response_bytes: int = 8 * 1024 * 1024

    def __post_init__(self) -> None:
        for field_name in (
            "timeout",
            "backoff_seconds",
            "max_backoff_seconds",
            "max_retry_after_seconds",
        ):
            value = getattr(self, field_name)
            if type(value) not in (int, float):
                raise TypeError(f"{field_name} must be a number")
            normalized = float(value)
            if not math.isfinite(normalized):
                raise ValueError(f"{field_name} must be finite")
            if field_name == "timeout" and normalized <= 0:
                raise ValueError("timeout must be greater than zero")
            if field_name != "timeout" and normalized < 0:
                raise ValueError(f"{field_name} must not be negative")
            object.__setattr__(self, field_name, normalized)

        if type(self.max_attempts) is not int:
            raise TypeError("max_attempts must be an integer")
        if self.max_attempts < 1 or self.max_attempts > 10:
            raise ValueError("max_attempts must be between 1 and 10")
        if self.max_backoff_seconds < self.backoff_seconds:
            raise ValueError(
                "max_backoff_seconds must be at least backoff_seconds"
            )
        if type(self.max_response_bytes) is not int:
            raise TypeError("max_response_bytes must be an integer")
        if self.max_response_bytes < 1:
            raise ValueError("max_response_bytes must be greater than zero")


@dataclass(frozen=True, slots=True)
class HttpResponse:
    """A bounded raw HTTP response returned by an injected transport."""

    status: int
    headers: Mapping[str, str]
    body: bytes

    def __post_init__(self) -> None:
        if type(self.status) is not int:
            raise TypeError("status must be an integer")
        if not isinstance(self.headers, Mapping):
            raise TypeError("headers must be a mapping")
        copied_headers: dict[str, str] = {}
        for name, value in self.headers.items():
            if type(name) is not str or type(value) is not str:
                raise TypeError("headers must map strings to strings")
            copied_headers[name] = value
        object.__setattr__(
            self,
            "headers",
            MappingProxyType(copied_headers),
        )
        if not isinstance(self.body, bytes):
            raise TypeError("body must be bytes")

    def __deepcopy__(self, memo: dict[int, object]) -> HttpResponse:
        memo[id(self)] = self
        return self


@runtime_checkable
class HttpTransport(Protocol):
    """Testable synchronous transport used by built-in providers."""

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout: float,
        max_response_bytes: int,
    ) -> HttpResponse:
        """Perform one bounded HTTP request without retrying."""


@runtime_checkable
class GenerationProvider(Protocol):
    """Thread-safe generation interface accepted by concurrent live runners."""

    @property
    def name(self) -> str:
        """Return the stable, non-secret provider label."""

    def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate one non-streaming model response."""


@runtime_checkable
class ModelProvider(GenerationProvider, Protocol):
    """Generation provider that also supports model discovery."""

    def list_models(self) -> tuple[ModelInfo, ...]:
        """Return the models reported by the configured endpoint."""


Provider = ModelProvider
