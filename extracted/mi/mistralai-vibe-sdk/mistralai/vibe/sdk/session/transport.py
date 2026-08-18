"""Transport contract for the stateless Session Protocol."""

from collections.abc import AsyncIterator
from typing import Protocol, runtime_checkable

from .models.base import SessionModel
from .models.events import ClientTransportStreamItem
from .procedures.session import EventsReadParams


@runtime_checkable
class SessionTransport(Protocol):
    """Send typed Session procedures and read one session's ordered event stream."""

    async def request[ResultT: SessionModel](
        self,
        method: str,
        params: SessionModel,
        result_type: type[ResultT],
    ) -> ResultT: ...

    def read_events(self, params: EventsReadParams) -> AsyncIterator[ClientTransportStreamItem]: ...

    async def close(self) -> None: ...


__all__ = ["SessionTransport"]
