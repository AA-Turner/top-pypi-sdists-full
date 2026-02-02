"""
FortiOS LOG API - Search

Log query endpoints for search logs.

Note: LOG endpoints are read-only (GET only) and return log data.
They use nested classes to represent path parameters.

Example Usage:
    >>> fgt.api.log.search.abort.get(rows=100)
    >>> fgt.api.log.search.status.get(rows=100)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient

from hfortix_fortios.models import FortiObjectList


class Search:
    """Search log operations.
    
    Provides access to search log endpoints with nested classes
    for different log types and subtypes.
    """

    def __init__(self, client: "IHTTPClient"):
        """Initialize Search endpoint."""
        self._client = client
        self.abort = SearchAbort(client)
        self.status = SearchStatus(client)


class SearchAbort:
    """Abort a running log search session."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize SearchAbort."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.search.abort.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "search/abort", params=params if params else None)
        return result

class SearchStatus:
    """Returns status of log search session, if it is active or not."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize SearchStatus."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.search.status.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "search/status", params=params if params else None)
        return result
