"""A request as a handler standing in for the network sees it."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypeAlias

from labqoat.net.headers import Headers
from labqoat.net.url import Url

if TYPE_CHECKING:
    from labqoat.net.response import Response


@dataclass(frozen=True)
class Request:
    """Method, address, the fields that would be sent, the whole body and the seconds each wait may take."""

    method: str
    url: Url
    headers: Headers = field(default_factory=Headers)
    content: bytes = b""
    timeout: float | None = None

    def read(self) -> bytes:
        """The whole body."""
        return self.content


Handler: TypeAlias = Callable[[Request], "Response"]
AsyncHandler: TypeAlias = Callable[[Request], "Response | Awaitable[Response]"]
