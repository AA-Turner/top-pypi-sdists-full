from typing import List, Optional

from anyscale._private.sdk import sdk_command
from anyscale.events._private.events_sdk import PrivateEventsSDK
from anyscale.events.models import Event, EventsFilter


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
