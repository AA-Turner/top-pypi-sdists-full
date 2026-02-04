"""Type stubs for TACACS_PLUS_ACCOUNTING category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .filter import Filter
    from .setting import Setting

__all__ = [
    "Filter",
    "Setting",
    "TacacsPlusAccounting",
]


class TacacsPlusAccounting:
    """TACACS_PLUS_ACCOUNTING API category.
    
    All endpoints return FortiObject instances with:
    - Attribute access: response.field
    - Dictionary access: response["field"]
    - Convert to dict: response.dict or response.json
    """
    
    filter: Filter
    setting: Setting

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize tacacs_plus_accounting category with HTTP client."""
        ...
