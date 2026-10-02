"""Activity event service implementation (maintainer only)."""

from typing import List, Optional

from ..models.activity_event import (
    ActivityEventFilterOptions,
    PaginatedActivityEventResponse,
)
from ..utils import ApiRequestHandler, TokenSource


class ActivityEventService:
    """Service for querying the activity events audit log.

    Requires maintainer privileges — all methods raise HTTP 403 for
    non-maintainer callers.
    """

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the activity event service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token source
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def list_events(
        self,
        *,
        actor_id: Optional[str] = None,
        domain: Optional[List[str]] = None,
        event_type: Optional[List[str]] = None,
        entity_type: Optional[List[str]] = None,
        entity_id: Optional[str] = None,
        from_dt: Optional[str] = None,
        to_dt: Optional[str] = None,
        sort_dir: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedActivityEventResponse:
        """List activity events with optional filters.

        Multi-value parameters (domain, event_type, entity_type) are serialised
        as repeated query params: e.g. ?domain=user_management&domain=budget_management.

        Args:
            actor_id: Filter by actor user ID
            domain: Filter by domain(s)
            event_type: Filter by event type(s)
            entity_type: Filter by entity type(s)
            entity_id: Filter by entity ID
            from_dt: ISO 8601 lower bound datetime (maps to 'from' query param)
            to_dt: ISO 8601 upper bound datetime (maps to 'to' query param)
            sort_dir: 'asc' or 'desc' (default 'desc')
            limit: Results per page, 1-1000 (default 50)
            offset: Pagination offset (default 0)

        Returns:
            PaginatedActivityEventResponse
        """
        params: dict = {}
        if actor_id is not None:
            params["actor_id"] = actor_id
        if domain is not None:
            params["domain"] = domain
        if event_type is not None:
            params["event_type"] = event_type
        if entity_type is not None:
            params["entity_type"] = entity_type
        if entity_id is not None:
            params["entity_id"] = entity_id
        if from_dt is not None:
            params["from"] = from_dt
        if to_dt is not None:
            params["to"] = to_dt
        if sort_dir is not None:
            params["sort_dir"] = sort_dir
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        return self._api.get(
            "/v1/admin/activity-events",
            PaginatedActivityEventResponse,
            params=params if params else None,
            wrap_response=False,
        )

    def get_filter_options(self) -> ActivityEventFilterOptions:
        """Get distinct filter options available for activity events.

        Returns:
            ActivityEventFilterOptions with distinct domains, event_types,
            and entity_types present in the audit log.
        """
        return self._api.get(
            "/v1/admin/activity-events/filter-options",
            ActivityEventFilterOptions,
            wrap_response=False,
        )
