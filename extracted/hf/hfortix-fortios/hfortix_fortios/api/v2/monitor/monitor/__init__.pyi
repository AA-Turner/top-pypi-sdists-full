"""Type stubs for MONITOR category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient


class Monitor:
    """Type stub for Monitor."""


    def __init__(self, client: IHTTPClient) -> None: ...
