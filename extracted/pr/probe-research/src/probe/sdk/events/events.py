"""`probe.events`: follow Probe's live events from a script, with a callback on a background thread
(`subscribe`) or as an iterator (`stream`). An add-on: `probe.init` never starts one (D79)."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING
from uuid import UUID

from ...generated.live import LiveEvent
from .follower import EventStream
from .query import make_query
from .subscription import Subscription

if TYPE_CHECKING:
    from ..client.client import Client


def subscribe(
    run: str | None = None,
    *,
    on_event: Callable[[LiveEvent], object],
    project: str | None = None,
    experiment: str | None = None,
    kinds: str | Sequence[str] | None = None,
    since: int | None = None,
    writer: str | UUID | None = None,
    client: Client | None = None,
) -> Subscription:
    """Call `on_event(event)` for each live event, on a background thread, until `close()`.

    Follows one run, experiment or project (an id or a slug), or the whole team when none is named; `kinds`
    narrows it (`["samples.live", "run.*"]`). `since` resumes after a seq (a `Subscription.cursor`). A dropped
    connection reconnects with the last seq and misses nothing. `resync` (re-read what you follow) and `lagged`
    reach every subscription. A callback that raises is logged; the subscription goes on.
    """
    stream_ = _open(run=run, project=project, experiment=experiment, kinds=kinds, since=since, writer=writer,
                    client=client)
    return Subscription(stream_, on_event).start()


def stream(
    run: str | None = None,
    *,
    project: str | None = None,
    experiment: str | None = None,
    kinds: str | Sequence[str] | None = None,
    since: int | None = None,
    writer: str | UUID | None = None,
    client: Client | None = None,
) -> EventStream:
    """The same events as an iterator: `for event in probe.events.stream(project="gsm-rl"): ...`. It reconnects
    by itself; a refusal a reconnect cannot fix (a bad credential, an unknown run) raises. `close()` ends it."""
    return _open(run=run, project=project, experiment=experiment, kinds=kinds, since=since, writer=writer,
                 client=client)


def _open(*, run, project, experiment, kinds, since, writer, client) -> EventStream:
    query = make_query(run=run, experiment=experiment, project=project, kinds=kinds, writer=writer)
    return EventStream(_get_transport(client), query, since=since)


def _get_transport(client: Client | None):
    """The given client's transport, else one for this machine's login (env, then the stored context)."""
    if client is not None:
        return client.transport
    from ..delivery.transport.transport import Transport
    from ..settings.settings import resolve

    return Transport(resolve())
