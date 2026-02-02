"""Type stubs for interactive help system."""

from __future__ import annotations

from typing import Any

def help(endpoint: Any, show_fields: bool = False) -> None:
    """
    Display comprehensive help for any FortiOS API endpoint.

    Args:
        endpoint: The API endpoint object
        show_fields: Whether to list all available fields (default: False)
    """
    ...
