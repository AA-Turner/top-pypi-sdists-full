from typing import Dict, List, Optional

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.client.openapi_client.models import EntityType, UnifiedEvent
from anyscale.events.models import Event, EventsFilter


# What the CLI/SDK calls a resource -> what the backend calls the same thing.
_ENTITY_TYPE_ON_THE_WIRE: Dict[str, str] = {
    "job": EntityType.PRODUCTION_JOB,
    "service": EntityType.SERVICE,
    "workspace": EntityType.WORKSPACE,
    "cluster": EntityType.SESSION,
}

# The backend caps every page at this many events.
_MAX_PAGE_SIZE = 1000

# Only service and workspace events page: their backend helpers forward `paging_token` to
# the DB query (`get_service_events` / `get_workspace_events` in events_router.py). The job
# helper hard-codes `paging_token=None` and the cluster helper passes only a limit, so for
# those two a second request would return the first page again; we make one call instead.
_ENTITIES_WITH_CURSOR_PAGING = frozenset({"service", "workspace"})


class PrivateEventsSDK(BaseSDK):
    def list(self, events_filter: EventsFilter) -> List[Event]:
        """Fetch the events matching `events_filter`, newest first unless asked otherwise."""
        entity_type = events_filter.entity_type
        if (
            entity_type not in _ENTITIES_WITH_CURSOR_PAGING
            and events_filter.max_items > _MAX_PAGE_SIZE
        ):
            self.logger.warning(
                f"{entity_type} events are returned as a single batch of at most "
                f"{_MAX_PAGE_SIZE}; max_items={events_filter.max_items} cannot be fully honoured."
            )

        events: List[Event] = []
        paging_token: Optional[str] = None
        while len(events) < events_filter.max_items:
            response = self.client.get_unified_events(
                entity_type=_ENTITY_TYPE_ON_THE_WIRE[entity_type],
                entity_id=events_filter.entity_id,
                # None means "no filter". Never send an empty list: the backend reads it
                # as "match nothing" and returns zero events.
                origin=events_filter.source or None,
                level=events_filter.level or None,
                message=events_filter.message_contains,
                start_time=events_filter.start_time,
                end_time=events_filter.end_time,
                ascending_order=events_filter.ascending,
                include_verbose_events=events_filter.verbose,
                instance_id=events_filter.instance_id,
                instance_node_ip=events_filter.node_ip,
                autoscaler_resource_bundles=events_filter.resource_bundles,
                count=min(events_filter.max_items - len(events), _MAX_PAGE_SIZE),
                paging_token=paging_token,
            )
            page = response.results or []
            events.extend(_to_event(raw) for raw in page)

            paging_token = response.metadata.next_paging_token if response.metadata else None
            if not page or paging_token is None or entity_type not in _ENTITIES_WITH_CURSOR_PAGING:
                break

        return events[: events_filter.max_items]


def _to_event(raw: UnifiedEvent) -> Event:
    # `message` and `level` are optional on the wire: job and service events can arrive
    # without them. One such event must not fail the whole listing, so keep a missing
    # message as None and report a missing level as UNKNOWN, a value of the API's own
    # EventLevel enum, rather than the string "None".
    return Event(
        id=raw.id,
        created_at=raw.created_at,
        level=str(raw.level) if raw.level else "UNKNOWN",
        source=str(raw.origin),
        message=raw.message,
        cluster_id=raw.cluster_id,
    )
