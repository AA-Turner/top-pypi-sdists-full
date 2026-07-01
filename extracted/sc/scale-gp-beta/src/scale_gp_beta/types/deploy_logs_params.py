# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["DeployLogsParams"]


class DeployLogsParams(TypedDict, total=False):
    cursor: str
    """Cursor from previous response's next_cursor field"""

    limit: int
    """Maximum number of log lines to return"""
