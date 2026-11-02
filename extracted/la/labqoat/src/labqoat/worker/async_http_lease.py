"""Reference-counted client lifetime confined to one asynchronous event loop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from labqoat.net.async_http_client import AsyncHttpClient


@dataclass
class AsyncHttpLease:
    """Keep concurrent operations attached until the last owner releases their shared transport."""

    client: AsyncHttpClient | None = None
    users: int = 0
