from typing import List, Optional

from anyscale._private.sdk import sdk_command
from anyscale.events._private.events_sdk import PrivateEventsSDK
from anyscale.events.models import Event, EventsFilter, EventsPage


_EVENTS_SDK_SINGLETON_KEY = "events_sdk"

_LIST_EXAMPLE = """
import anyscale
from anyscale.events.models import EventsFilter

events = anyscale.events.list(
    EventsFilter(entity_type="job", entity_id="prodjob_abc123", level=["ERROR"]),
)
for event in events:
    print(event.created_at, event.level, event.source, event.message)
"""

_LIST_ARG_DOCSTRINGS = {
    "events_filter": "Which resource to read events for, and which of its events to keep.",
}


@sdk_command(
    _EVENTS_SDK_SINGLETON_KEY,
    PrivateEventsSDK,
    doc_py_example=_LIST_EXAMPLE,
    arg_docstrings=_LIST_ARG_DOCSTRINGS,
)
def list(  # noqa: A001
    events_filter: EventsFilter,
    *,
    _private_sdk: Optional[PrivateEventsSDK] = None,
) -> List[Event]:
    """List events of a job, service, workspace or cluster. Newest first by default."""
    return _private_sdk.list(events_filter)  # type: ignore


_LIST_PAGE_EXAMPLE = """
import anyscale
from anyscale.events.models import EventsFilter

events_filter = EventsFilter(entity_type="job", entity_id="prodjob_abc123", max_items=100)
page = anyscale.events.list_page(events_filter)
for event in page.results:
    print(event.created_at, event.level, event.source, event.message)
if page.next_page_token is not None:
    # The same filter, continued after the last event of the first page.
    page = anyscale.events.list_page(events_filter, page_token=page.next_page_token)
"""

_LIST_PAGE_ARG_DOCSTRINGS = {
    "events_filter": "Which resource to read events for, and which of its events to keep. "
    "max_items is the page size, at most 1000.",
    "page_token": "The next_page_token of an earlier page, used with the same filter. "
    "None starts at the first event.",
}


@sdk_command(
    _EVENTS_SDK_SINGLETON_KEY,
    PrivateEventsSDK,
    doc_py_example=_LIST_PAGE_EXAMPLE,
    arg_docstrings=_LIST_PAGE_ARG_DOCSTRINGS,
)
def list_page(
    events_filter: EventsFilter,
    *,
    page_token: Optional[str] = None,
    _private_sdk: Optional[PrivateEventsSDK] = None,
) -> EventsPage:
    """List one page of events of a job, service, workspace or cluster, and a next token."""
    return _private_sdk.list_page(events_filter, page_token=page_token)  # type: ignore
