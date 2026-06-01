"""Protocols and type aliases for the auth system."""

from collections.abc import Callable
from typing import Any, Protocol, runtime_checkable

from fastapi import Request
from pydantic import SecretStr

from csrd.models.claims import UserClaims


@runtime_checkable
class Authenticator(Protocol):
    """Protocol for pluggable authentication strategies."""

    def __call__(self, request: Request, token: str) -> UserClaims: ...


@runtime_checkable
class KeyProvider(Protocol):
    """Protocol for pluggable JWT key resolution."""

    def __call__(self, token_headers: dict[str, Any], app: Any) -> Any: ...


AuthCallback = Callable[[Request, str], UserClaims | Any]
KeyCallback = Callable[..., Any]

KeySource = str | bytes | SecretStr | KeyProvider
