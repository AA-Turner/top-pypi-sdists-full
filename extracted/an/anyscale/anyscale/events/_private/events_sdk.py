from typing import Dict, List, Optional

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.client.openapi_client.models import EntityType, UnifiedEvent
from anyscale.events.models import Event, EventsFilter, EventsPage, MAX_EVENTS_PER_PAGE


# What the CLI/SDK calls a resource -> what the backend calls the same thing.
_ENTITY_TYPE_ON_THE_WIRE: Dict[str, str] = {
    "job": EntityType.PRODUCTION_JOB,
    "service": EntityType.SERVICE,
    "workspace": EntityType.WORKSPACE,
    "cluster": EntityType.SESSION,
}


class PrivateEventsSDK(BaseSDK):
    def list(self, events_filter: EventsFilter) -> List[Event]:
        """Fetch up to max_items events matching `events_filter`, page after page."""
        events: List[Event] = []
        page_token: Optional[str] = None
        while len(events) < events_filter.max_items:
            count = min(events_filter.max_items - len(events), MAX_EVENTS_PER_PAGE)
            page = self._fetch_page(events_filter, count, page_token)
            events.extend(page.results)
            # Stop when no page follows, or when the backend hands back the token it was
            # given: asking again would return the same page forever. A page can be empty
            # and still have a next one (cluster events skip rows without a message).
            if page.next_page_token is None or page.next_page_token == page_token:
                break
            page_token = page.next_page_token

        return events[: events_filter.max_items]

    def list_page(
        self, events_filter: EventsFilter, page_token: Optional[str] = None
    ) -> EventsPage:
        """One page of at most max_items events, from `page_token` on."""
        if events_filter.max_items > MAX_EVENTS_PER_PAGE:
            raise ValueError(
                f"max_items must be at most {MAX_EVENTS_PER_PAGE} for one page, "
                f"got {events_filter.max_items}."
            )
        return self._fetch_page(events_filter, events_filter.max_items, page_token)

    def _fetch_page(
        self, events_filter: EventsFilter, count: int, page_token: Optional[str]
    ) -> EventsPage:
        response = self.client.get_unified_events(
            entity_type=_ENTITY_TYPE_ON_THE_WIRE[events_filter.entity_type],
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
            count=count,
            paging_token=page_token,
        )
        return EventsPage(
            results=[_to_event(raw) for raw in response.results or []],
            next_page_token=response.metadata.next_paging_token if response.metadata else None,
        )


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
