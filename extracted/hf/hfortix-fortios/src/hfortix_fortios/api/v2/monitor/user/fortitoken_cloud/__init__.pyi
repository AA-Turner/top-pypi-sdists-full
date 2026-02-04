"""Type stubs for FORTITOKEN_CLOUD category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .status import Status
    from .trial import Trial

__all__ = [
    "Status",
    "Trial",
    "FortitokenCloud",
]


class FortitokenCloud:
    """FORTITOKEN_CLOUD API category.
    
    All endpoints return FortiObject instances with:
    - Attribute access: response.field
    - Dictionary access: response["field"]
    - Convert to dict: response.dict or response.json
    """
    
    status: Status
    trial: Trial

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortitoken_cloud category with HTTP client."""
        ...
