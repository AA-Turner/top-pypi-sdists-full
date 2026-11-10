# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SessionListParams"]


class SessionListParams(TypedDict, total=False):
    created_after: Annotated[Union[str, datetime], PropertyInfo(alias="createdAfter", format="iso8601")]
    """Only sessions created at or after this ISO 8601 timestamp, e.g.

    2026-10-01T00:00:00Z.
    """

    created_before: Annotated[Union[str, datetime], PropertyInfo(alias="createdBefore", format="iso8601")]
    """Only sessions created before this ISO 8601 timestamp."""

    cursor_id: Annotated[str, PropertyInfo(alias="cursorId")]
    """Cursor ID for pagination"""

    limit: int
    """Number of sessions to return. Default is 50, max is 100."""

    metadata: Dict[str, str]
    """Exact-match metadata filters, e.g.

    metadata[environment]=production. All entries must match. Values match the
    stored string exactly; numbers and booleans are stored as strings, so
    metadata[attempt]=3 matches attempt sent as 3 or "3".
    """

    project_id: Annotated[str, PropertyInfo(alias="projectId")]
    """Filter sessions by project"""

    release_reason: Annotated[
        Literal[
            "user_requested",
            "timeout",
            "inactivity_timeout",
            "creation_timeout",
            "startup_failed",
            "browser_closed",
            "browser_crashed",
        ],
        PropertyInfo(alias="releaseReason"),
    ]
    """Filter released sessions by why they ended.

    Live sessions have no release reason and are excluded whenever this is set.
    Without an explicit status, matching failed sessions are included.
    """

    signal: List[
        Literal[
            "captcha_encountered",
            "proxy_connection_failed",
            "session_timeout_exceeded",
            "bot_detection_triggered",
            "context_restored",
        ]
    ]
    """Signals the session must carry; repeat the parameter to require several.

    All must match. Derived signals are finalized at release.
    """

    status: Literal["live", "released", "failed"]
    """Filter sessions by current status"""
