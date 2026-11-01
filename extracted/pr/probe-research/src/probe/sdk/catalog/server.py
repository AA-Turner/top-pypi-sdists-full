"""Read the server's answer to a catalog call: is the catalog there, the sentence for a failure, once-per-site warnings."""

from __future__ import annotations
import sys
import threading
import time
from typing import TYPE_CHECKING, Any

from .. import errors
from ...foundation.safe_warn import safe_warn

if TYPE_CHECKING:  # pragma: no cover
    from ..client.client import Client
from probe.sdk.catalog.refs import CatalogRefused
#: After Probe was unreachable, the catalog probe is not repeated for this long (else every call pays `REQUEST_SECONDS`).
UNREACHABLE_TTL_SECONDS = 60.0
STATED = "human"
#: The limit a hosted-data refusal names (402, C8 D2).
HOSTED_DATA_LIMIT = "hosted_data_bytes"

_warned: set[str] = set()
_warned_lock = threading.Lock()


def _warn_once(key: str, message: str) -> None:
    """One line per kind of trouble per process (a per-step loop must not print every step)."""
    with _warned_lock:
        if key in _warned:
            return
        _warned.add(key)
    safe_warn.warn(message, stacklevel=3)


def _say(message: str) -> None:
    """A line the researcher should see once, on stderr, never raising."""
    try:
        if safe_warn.streams_allowed():
            print(message, file=sys.stderr, flush=True)
    except Exception:  # noqa: BLE001 - a notice never breaks the caller
        pass
#: The fixed forms a refusal or a warning points to.
FIXED_REF_FORMS = "`dataset:<name>@<N>`, `checkpoint:<run>@step<N>`, `source:<key>@<revision>`"


# Talking to the server


def old_server(exc: BaseException) -> bool:
    """No such route (FastAPI's 404, or 405 for a path with other methods): it predates the catalog."""
    from ..client.server_features import _route_absent

    if isinstance(exc, errors.RosError) and exc.status == 405:
        return True
    return isinstance(exc, errors.RosError) and _route_absent(exc)


def hosted_limit_message(exc: errors.LimitReachedError) -> str:
    """The sentence for a 402 over the hosted-data cap (C8, D2)."""
    figure = ""
    if exc.current is not None and exc.maximum is not None:
        figure = f" ({bytes_figure(exc.current)} of {bytes_figure(exc.maximum)} used)"
    return (
        f"the team's hosted datasets and checkpoints are at their cap{figure}, so nothing was "
        "uploaded. Record it as a reference instead (leave out upload / --upload), or free "
        "hosted data by deleting unused versions."
    )


def bytes_figure(value: Any) -> str:
    """A 402 figure as a size: storage refusals send GiB (`storage_guard._gib`); a figure too big for GiB is bytes."""
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return str(value)
    if value >= 1 << 20:
        return human_bytes(int(value))
    return f"{value:g} GB"


def describe(exc: BaseException, what: str) -> str:
    """One warning line for a failed catalog call."""
    if old_server(exc):
        return (
            f"probe: {what}: this Probe server predates the data catalog, so nothing was recorded "
            "(it needs the catalog routes)."
        )
    if isinstance(exc, errors.LimitReachedError):
        if exc.limit == HOSTED_DATA_LIMIT:
            return f"probe: {what}: {hosted_limit_message(exc)}"
        return f"probe: {what}: refused by a plan limit: {exc}"
    if isinstance(exc, errors.TransportError):
        return f"probe: {what}: Probe could not be reached ({type(exc).__name__}: {exc}); nothing was recorded."
    if isinstance(exc, errors.RosError):
        status = f" ({exc.status})" if exc.status else ""
        return f"probe: {what} was refused{status}: {exc}"
    if isinstance(exc, CatalogRefused):
        return f"probe: {what}: {exc}"
    return f"probe: {what} failed ({type(exc).__name__}: {exc}); nothing was recorded."


def _warn_failure(exc: BaseException, what: str) -> None:
    kind = "old" if old_server(exc) else type(exc).__name__
    _warn_once(f"{what.split('(')[0]}:{kind}:{getattr(exc, 'status', '')}", describe(exc, what))


def catalog_available(client: "Client") -> bool | None:
    """Whether this server has the catalog, asked once per client: by the `catalog` feature, else by
    whether the datasets list route exists, within `REQUEST_SECONDS`. None if it could not be asked,
    kept for `UNREACHABLE_TTL_SECONDS` so a run of calls pays the timeout once."""
    from ..delivery.transport.deadlines import deadline_scope

    known = getattr(client, "_catalog_available", None)
    if known is not None:
        return known
    if time.monotonic() < float(getattr(client, "_catalog_unreachable_until", 0.0) or 0.0):
        return None
    try:
        from probe.sdk.catalog import catalog  # call time: catalog imports this module

        with deadline_scope(time.monotonic() + catalog.REQUEST_SECONDS):
            if client.supports_feature("catalog"):
                answer = True
            else:
                client.list_datasets(limit=1)
                answer = True
    except errors.RosError as exc:
        if old_server(exc):
            answer = False
        elif isinstance(exc, (errors.TransportError, errors.ServerError)):
            try:
                client._catalog_unreachable_until = time.monotonic() + UNREACHABLE_TTL_SECONDS  # type: ignore[attr-defined]
            except Exception:  # noqa: BLE001
                pass
            return None
        else:
            answer = True  # the route exists and refused this ask: the catalog is there
    try:
        client._catalog_available = answer  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        pass
    return answer


#: Why a moving ref is never queued, said once in every warning about it.
_NOT_QUEUED = "sent later, a moving ref could name a newer version than this run used"


def could_succeed_later(exc: BaseException) -> bool:
    """A failure the outbox would queue: no answer, or a server error."""
    return isinstance(exc, (errors.TransportError, errors.ServerError))


def _may_have_landed(exc: BaseException | None) -> bool:
    """Request sent, answer lost (read timeout, dropped connection, deadline after sending): the
    server may have applied it. Never for a connect failure or a pre-send deadline (`transport.py`
    sets `unreachable` for the first)."""
    if not isinstance(exc, errors.TransportError) or exc.unreachable:
        return False
    return not isinstance(exc, errors.DeadlineExceeded) or exc.sent


def warn_not_queued(client: Any, what: str, exc: BaseException | None = None) -> None:
    """Once per call site and ref (``what`` names it): a moving-ref write that could not be sent
    now, so is not recorded (D17). ``exc`` is None when the manifest it waits behind failed."""
    from ..delivery.delivery import is_offline_client

    if is_offline_client(client):
        text = (
            f"probe: {what}: not recorded: an offline run needs a fixed ref ({FIXED_REF_FORMS}), because "
            f"`probe sync` sends it later, and {_NOT_QUEUED}."
        )
    elif _may_have_landed(exc):
        text = (
            f"probe: {what}: Probe did not answer in time, so it may or may not be recorded. It was not "
            f"queued: {_NOT_QUEUED}. Name a fixed ref ({FIXED_REF_FORMS}) to be sure."
        )
    else:
        lead = describe(exc, what) if exc is not None else (
            f"probe: {what}: Probe could not take the dataset's manifest now; nothing was recorded."
        )
        text = f"{lead} It was not queued: {_NOT_QUEUED}. Call it again, or name a fixed ref ({FIXED_REF_FORMS})."
    _warn_once(f"moving:{what}:{type(exc).__name__}", text)


# Printing (the CLI's tables)


def human_bytes(n: Any) -> str:
    """`41.2 GB` (decimal units, as the plan's examples print)."""
    if not isinstance(n, (int, float)) or isinstance(n, bool):
        return "-"
    value = float(n)
    for unit in ("B", "kB", "MB", "GB", "TB"):
        if abs(value) < 1000 or unit == "TB":
            return f"{value:.0f} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1000
    return f"{value:.1f} PB"
