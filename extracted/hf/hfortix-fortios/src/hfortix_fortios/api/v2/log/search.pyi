"""Type stubs for LOG search endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient

from hfortix_fortios.models import FortiObjectList


class Search:
    """Search log operations."""
    abort: SearchAbort
    status: SearchStatus

    def __init__(self, client: IHTTPClient) -> None: ...


class SearchAbort:
    """Abort a running log search session."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get abort logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class SearchStatus:
    """Returns status of log search session, if it is active or not."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get status logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...
