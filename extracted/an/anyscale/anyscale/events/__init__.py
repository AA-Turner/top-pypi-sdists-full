from typing import List, Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.events._private.events_sdk import PrivateEventsSDK
from anyscale.events.commands import (
    _LIST_ARG_DOCSTRINGS,
    _LIST_EXAMPLE,
    list as list,  # noqa: A004
)
from anyscale.events.models import Event, EventsFilter


class EventsSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateEventsSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_LIST_EXAMPLE,
        arg_docstrings=_LIST_ARG_DOCSTRINGS,
    )
    def list(self, events_filter: EventsFilter) -> List[Event]:  # noqa: F811
        """List events of a job, service, workspace or cluster. Newest first by default."""
        return self._private_sdk.list(events_filter)
