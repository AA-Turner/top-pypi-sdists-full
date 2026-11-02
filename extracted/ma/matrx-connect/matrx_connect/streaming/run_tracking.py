"""Host-injected durable run seam — no stream runs untracked.

Every NDJSON response built by ``create_streaming_response`` asks the host to
open a durable run for its request before the work starts, and settles that run
on every exit. matrx-connect owns WHEN (task start, task end, cancel); the host
owns HOW (its runtime spine, its database) — exactly like the journal seam in
``journal.py``. A package-only consumer that installs no opener streams as
before.

A route names what its run is about with :class:`StreamRun` (passed as
``create_streaming_response(..., run=StreamRun(...))``). Without one the host
still opens a run, labeled with the route path.

Outcome words handed to :meth:`StreamRunHandle.settle`:
``"completed"`` | ``"failed"`` | ``"cancelled"``. A cancelled TASK (process
shutdown) is never settled — :meth:`StreamRunHandle.abandon` stops keeping the
run alive and the host's lease reaper records it as failed.
"""

from __future__ import annotations

import functools
import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Protocol

from matrx_connect.context.app_context import AppContext

STREAM_RUN_COMPLETED = "completed"
STREAM_RUN_FAILED = "failed"
STREAM_RUN_CANCELLED = "cancelled"


@dataclass(frozen=True)
class StreamRun:
    """What a streaming route's durable run is about.

    ``feature`` — a stable label for the work (never carries an id); defaults to
    the route path with id segments replaced by ``{id}``.
    ``link_kind`` / ``link_id`` — the feature record the run works on, so a
    returning client finds the run by that record
    (``GET /runtime/operations/by-link/{link_kind}/{link_id}``). Without a link
    the request itself is the handle (``X-Request-ID``).

    ``opens_own_root`` — the route declares that its work opens its OWN root run
    for this request (chat, workflow, agent runs), so the platform's auto run
    would only duplicate it (~3 reads + 4-5 writes per turn). The host then
    opens nothing up front and WATCHES instead: a stream that completes without
    its work ever opening that root is reported loudly. Prefer marking the task
    function with :func:`opens_own_root` — every route using it inherits the
    declaration.
    """

    feature: str | None = None
    link_kind: str | None = None
    link_id: str | None = None
    opens_own_root: bool = False


@dataclass(frozen=True)
class StreamRunRequest:
    """What the host opener receives: the route's declaration, resolved."""

    feature: str
    link_kind: str | None
    link_id: str | None
    # True when the route passed a StreamRun: the route owns this run, so the
    # host may make it the request's nesting parent and refuse to start work it
    # cannot track. False: the platform default, opened beside whatever run the
    # work opens for itself.
    declared: bool
    debug_label: str
    # The work opens its own root run: open nothing, watch that it does.
    own_root: bool = False


class StreamRunHandle(Protocol):
    execution_id: str | None

    async def settle(
        self,
        outcome: str,
        *,
        error_type: str | None = None,
        message: str | None = None,
    ) -> None:
        """Record the terminal outcome. Idempotent; never raises."""

    def abandon(self) -> None:
        """Stop keeping the run alive without settling it (task canceled)."""


StreamRunOpener = Callable[[AppContext, StreamRunRequest], Awaitable[StreamRunHandle | None]]

_opener: StreamRunOpener | None = None


def configure_stream_run_opener(opener: StreamRunOpener | None) -> None:
    """Install the host seam once at startup; ``None`` disables run tracking."""
    global _opener
    _opener = opener


def stream_run_opener_configured() -> bool:
    return _opener is not None


# Host-injected shutdown probe. A stream whose response generator is torn down while its
# task still runs is ambiguous: the CLIENT left, or the SERVER is going away (deploy
# drain, lifespan shutdown). The first is a deliberate stop ("cancelled"); the second
# must be left to the host's lease reaper (failed + system_error), exactly like a
# canceled task. matrx-connect cannot know which — the host says, through this probe.
_shutdown_probe: Callable[[], bool] | None = None


def configure_shutdown_probe(probe: Callable[[], bool] | None) -> None:
    """Install the host's "is this process shutting down?" probe (``None`` removes it)."""
    global _shutdown_probe
    _shutdown_probe = probe


def host_is_shutting_down() -> bool:
    """True when the host reports the process is shutting down. Never raises; with no
    probe installed nothing is shutting down (a package-only consumer is unchanged)."""
    probe = _shutdown_probe
    if probe is None:
        return False
    try:
        return bool(probe())
    except Exception:  # noqa: BLE001 - a broken probe must not break stream teardown
        return False


_ID_SEGMENT = re.compile(
    r"^(?:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    r"|[0-9a-fA-F]{16,}|\d+)$"
)


def default_stream_feature(route: str | None, debug_label: str) -> str:
    """The route path with id segments collapsed, so one route is one feature."""
    if route:
        parts = [("{id}" if _ID_SEGMENT.match(p) else p) for p in route.split("/")]
        normalized = "/".join(parts).strip()
        if normalized.strip("/"):
            return normalized[:120]
    return (debug_label or "stream")[:120]


#: Attribute :func:`opens_own_root` stamps on a task function.
OPENS_OWN_ROOT_ATTR = "__stream_opens_own_root__"
#: Qualified names of every task function declared as root-opening (for the guard).
OWN_ROOT_TASKS: dict[str, Callable[..., Any]] = {}


def opens_own_root(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Declare that this streaming task function opens its own root run for the
    request (through the host front door) on every normal path. Streams running
    it skip the platform's auto run; the host watches that the root really opens."""
    setattr(fn, OPENS_OWN_ROOT_ATTR, True)
    OWN_ROOT_TASKS[f"{fn.__module__}.{fn.__qualname__}"] = fn
    return fn


def task_opens_own_root(task_fn: object) -> bool:
    """True when ``task_fn`` (looking through partials and ``functools.wraps``
    wrappers) was declared with :func:`opens_own_root`."""
    seen = 0
    cur: object = task_fn
    while cur is not None and seen < 8:
        if getattr(cur, OPENS_OWN_ROOT_ATTR, False):
            return True
        if isinstance(cur, functools.partial):
            cur = cur.func
        else:
            cur = getattr(cur, "__wrapped__", None)
        seen += 1
    return False


def resolve_stream_run(
    ctx: AppContext,
    run: StreamRun | None,
    debug_label: str,
    task_fn: object | None = None,
) -> StreamRunRequest:
    feature = (run.feature if run is not None else None) or default_stream_feature(
        getattr(ctx, "route", None), debug_label
    )
    return StreamRunRequest(
        feature=feature,
        link_kind=run.link_kind if run is not None else None,
        link_id=run.link_id if run is not None else None,
        declared=run is not None,
        debug_label=debug_label,
        own_root=bool(run is not None and run.opens_own_root) or task_opens_own_root(task_fn),
    )


async def open_stream_run(
    ctx: AppContext,
    run: StreamRun | None,
    debug_label: str,
    task_fn: object | None = None,
) -> StreamRunHandle | None:
    """Ask the host to open this stream's run. May raise when a DECLARED run
    cannot be opened — the caller treats that as the task failing."""
    opener = _opener
    if opener is None:
        return None
    return await opener(ctx, resolve_stream_run(ctx, run, debug_label, task_fn))


__all__ = [
    "OPENS_OWN_ROOT_ATTR",
    "OWN_ROOT_TASKS",
    "STREAM_RUN_CANCELLED",
    "STREAM_RUN_COMPLETED",
    "STREAM_RUN_FAILED",
    "StreamRun",
    "StreamRunHandle",
    "StreamRunOpener",
    "StreamRunRequest",
    "configure_shutdown_probe",
    "configure_stream_run_opener",
    "default_stream_feature",
    "host_is_shutting_down",
    "open_stream_run",
    "opens_own_root",
    "resolve_stream_run",
    "stream_run_opener_configured",
    "task_opens_own_root",
]
