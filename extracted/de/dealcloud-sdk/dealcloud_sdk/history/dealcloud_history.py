"""
History API operations for DealCloud.

The API exposes three endpoint patterns:

1. **History** – GET .../entrydata/{entryTypeId}/entries/history
   Returns modified/deleted entries since a date, excluding changes from calculations and system triggers.

2. **All History** – GET .../entrydata/{entryTypeId}/entries/allHistory
   Same as History but includes entries updated by calculations and system triggers.

3. **Historical Data** – POST .../entrydata/getHistoricalData
   Returns data as it existed at a specific point in time.

References:
- History or All History: https://api.docs.dealcloud.com/docs/data/history/histallhist
- Historical Data: https://api.docs.dealcloud.com/docs/data/history/historical_data
"""

from datetime import datetime
from enum import IntEnum
from typing import Optional, Union, List

from ..cells.dealcloud_cells import DealCloudCells


class DateTimeBehavior(IntEnum):
    """
    Controls how date-time values are returned by the Historical Data API.

    Used as the ``dateTimeBehavior`` query parameter (0 or 1). Pass this enum,
    the integer (0 or 1), or the string ``"UTC"`` or ``"Local"`` (case-insensitive)
    to ``get_historical_data(..., date_time_behavior=...)``.
    """

    UTC = 0
    """Return date-time in UTC (API default)."""

    LOCAL = 1
    """Return date-time localized to the user/client timezone settings."""


def _normalize_date_time_behavior(
    value: Union[DateTimeBehavior, int, str, None],
) -> Optional[int]:
    """Convert DateTimeBehavior enum, int, or string ('UTC'/'Local') to API int (0 or 1)."""
    if value is None:
        return None
    if isinstance(value, DateTimeBehavior):
        return int(value)
    if isinstance(value, int):
        if value not in (0, 1):
            raise ValueError(f"date_time_behavior must be 0 or 1, got {value}")
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized == "utc":
            return 0
        if normalized == "local":
            return 1
        raise ValueError(
            f"date_time_behavior string must be 'UTC' or 'Local' (case-insensitive), got {value!r}"
        )
    raise TypeError(
        f"date_time_behavior must be DateTimeBehavior, int (0 or 1), or str ('UTC'/'Local'), got {type(value).__name__}"
    )


class DealCloudHistory(DealCloudCells):
    """
    History API operations. Provides access to change history and point-in-time data.
    """

    @property
    def history_url(self) -> str:
        """
        Base URL for history endpoints (entrydata). Append path and query as needed.

        Example:
            GET {history_url}/Company/entries/history?modifiedSince=2020-04-26T01:16:40.030Z
        """
        return self._history_url

    # =========================================================================
    # 1. History / 2. All History (GET .../entries/history or .../allHistory)
    # =========================================================================

    def get_history(
        self,
        object_id: Union[int, str],
        modified_since: Optional[datetime] = None,
        include_calculations: bool = False,
        deleted_only: bool = False,
        **kwargs: object,
    ) -> List[dict]:
        """
        Get modified or deleted entries since a date (History or All History).

        Calls one of:
        - GET .../entrydata/{entryTypeId}/entries/history?modifiedSince=...
        - GET .../entrydata/{entryTypeId}/entries/allHistory?modifiedSince=...

        Per [History or All History](https://api.docs.dealcloud.com/docs/data/history/histallhist):
        - **history**: excludes entries updated by calculations and system triggers.
        - **allHistory**: includes those. Use for delta sync when you need all changes.
        Deleted entries are only returned when `modifiedSince` is set (max 6 months).
        Only modifiedSince is sent; other kwargs are accepted for backward compatibility and ignored.

        Args:
            object_id: Entry type ID or API name (e.g. "Company" or 2011).
            modified_since: ISO 8601 date-time; changes after this time (API param modifiedSince). Required.
            include_calculations: If True, use allHistory; otherwise use history.
            deleted_only: If True, return only entries with isDeleted true (client-side filter).
            **kwargs: Ignored (end_date, entry_ids, field_ids, user_ids, limit, skip not in API spec).

        Returns:
            List of entry objects, e.g. [{"isDeleted": false, "id": 2772624, "name": "...", "entryListId": 2013}].
            When deleted_only is True, only entries with isDeleted true are returned.
        """
        if modified_since is None:
            raise ValueError("modified_since is required")
        path = "allHistory" if include_calculations else "history"
        url = f"{self._history_url}/{object_id}/entries/{path}"
        params = {"modifiedSince": modified_since.isoformat()}
        result = self._client.get(url, params=params)
        if deleted_only and isinstance(result, list):
            result = [e for e in result if isinstance(e, dict) and e.get("isDeleted") is True]
        return result

    # =========================================================================
    # 3. Historical Data (POST .../getHistoricalData)
    # =========================================================================

    def get_historical_data(
        self,
        object_id: Union[int, str],
        entry_ids: List[int],
        as_of_date: datetime,
        fields: Optional[List[str]] = None,
        wrap_into_arrays: bool = True,
        date_time_behavior: Optional[Union[DateTimeBehavior, int, str]] = None,
    ):
        """
        Get data as it existed at a specific point in time.

        Calls POST .../entrydata/getHistoricalData per
        [Historical Data](https://api.docs.dealcloud.com/docs/data/history/historical_data).

        Body: entryTypeId, entries (int[]), fromDate (ISO 8601), optional fields (string[]).
        Query: wrapIntoArrays (boolean), dateTimeBehavior (0=UTC, 1=localized).

        Args:
            object_id: Entry type ID or API name.
            entry_ids: Entry IDs to retrieve.
            as_of_date: Point-in-time for data (sent as fromDate).
            fields: Optional field IDs (strings), e.g. ["12", "34"].
            wrap_into_arrays: Query param; improves consistency for multi-value fields.
            date_time_behavior: How to return date-time. Use :class:`DateTimeBehavior` (e.g.
                ``DateTimeBehavior.UTC`` or ``DateTimeBehavior.LOCAL``), int ``0`` or ``1``,
                or string ``"UTC"`` or ``"Local"`` (case-insensitive). Omit for API default (UTC).

        Returns:
            List of rows when the API returns a result with "rows"; otherwise the raw response.
        """
        url = f"{self._history_url}/getHistoricalData"
        payload = {
            "entryTypeId": object_id,
            "entries": entry_ids,
            "fromDate": as_of_date.isoformat(),
        }
        if fields is not None:
            payload["fields"] = fields
        params = {}
        if wrap_into_arrays:
            params["wrapIntoArrays"] = "true"
        dt_behavior = _normalize_date_time_behavior(date_time_behavior)
        if dt_behavior is not None:
            params["dateTimeBehavior"] = dt_behavior
        response = self._client.post(url, json=payload, params=params if params else None)
        if isinstance(response, dict) and "rows" in response:
            return response["rows"]
        return response

