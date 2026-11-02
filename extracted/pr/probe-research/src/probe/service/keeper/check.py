"""one keeper check: is the service down, settle, start it again, report."""

from __future__ import annotations

import contextlib
import os
import time

from ...foundation.service_api import paths
from probe.service.keeper.scheduler import INTERVAL_S


#: The keeper's record of a service that does not answer (crash-report plan B3).
STATE_NAME = "keeper.json"
#: A service answers when its `service.hello` reply comes within this: a
#: connect alone passes a wedged loop, whose socket still queues connections.
HELLO_TIMEOUT_S = 2.0
#: Needed and not answering this long: one `service_down` report ...
DOWN_REPORT_S = 300.0
#: ... and at most one in this long (the report's own dedupe window).
REPORT_EVERY_S = 6 * 3600.0


class Down:
    """Why no service answers (`service_down`'s `reason`)."""

    NO_SERVICE = "no_service"  # nothing to connect to
    WEDGED = "wedged"  # it takes the connection, never answers the hello
    BACKOFF = "backoff"  # `ensure` started 3 in a minute already: it starts none


def _answers() -> str | None:
    """None when a service replies to `service.hello` within HELLO_TIMEOUT_S;
    else why not (Down)."""
    from ...foundation import service_api as client
    from ...foundation.service_api.vocabularies import Client

    conn = client.connect(HELLO_TIMEOUT_S)
    if conn is None:
        return Down.NO_SERVICE
    try:
        conn.hello(Client.CLI, "keeper")
        return None
    except client.ServiceError:
        return None  # it answered (another API, a refusal): it is up
    except (OSError, ValueError):
        return Down.WEDGED
    finally:
        conn.close()


def _log(message: str) -> None:
    """One line in service.log, with the keeper's own prefix (its stdout goes
    nowhere under launchd). Never raises."""
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with contextlib.suppress(OSError):
        fd = os.open(paths.log_path(), os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0), 0o600)
        try:
            os.write(fd, f"[{stamp}] probe-service-keeper[{os.getpid()}]: {message}\n".encode("utf-8", "replace"))
        finally:
            os.close(fd)


def _state() -> dict:
    from ..watch.files import read_json

    data = read_json(paths.service_dir() / STATE_NAME)
    return data if isinstance(data, dict) else {}


def _save(state: dict) -> bool:
    """False when it could not be written (a full disk): nothing that depends
    on it being kept (the last report's time) may go on as if it were."""
    from ..watch.files import write_json

    with contextlib.suppress(OSError):
        paths.private_dir(paths.service_dir())
    return write_json(paths.service_dir() / STATE_NAME, state)


#: The keeper's runs this far apart in wall OR monotonic time (a sleep, which
#: monotonic time does not count; a reboot, which restarts it; a timer that
#: stopped) do not add up: the minutes down are counted again from there.
GAP_S = 3 * INTERVAL_S
#: Monotonic time (the system's, shared by every process of one boot), a seam for tests.
_monotonic = time.monotonic


def _settle(down: str | None, started: str | None = None, *, now: float | None = None) -> None:
    """Keep `keeper.json`: since when a needed service has not answered, why,
    and for how long while the machine was awake (`down_for`: consecutive runs
    at most GAP_S apart in both clocks); one log line per change; past
    DOWN_REPORT_S of that, the `service_down` report (at most every
    REPORT_EVERY_S, and only once that is saved)."""
    now = time.time() if now is None else now
    mono = _monotonic()
    state = _state()
    since = state.get("down_since")
    if down is None:
        if isinstance(since, (int, float)):
            _log(f"the service answers again (after {max(0.0, now - since) / 60:.0f} min)")
            reported = state.get("reported_at")
            _save({"reported_at": reported} if isinstance(reported, (int, float)) else {})
        return
    checked, checked_mono, down_for = state.get("checked_at"), state.get("checked_mono"), state.get("down_for")
    numbers = all(isinstance(v, (int, float)) for v in (since, checked, checked_mono, down_for))
    if numbers and 0 <= now - checked <= GAP_S and 0 <= mono - checked_mono <= GAP_S:
        down_for = down_for + (mono - checked_mono)
        if state.get("reason") != down:
            _log(f"a session needs the service and none answers ({down}); ensure: {started}")
    else:
        if numbers:
            _log(f"none answers ({down}) after a gap (a sleep, a reboot): the minutes are counted again")
        else:
            _log(f"a session needs the service and none answers ({down}); ensure: {started}")
        since, down_for = now, 0.0
    state.update(down_since=since, reason=down, checked_at=now, checked_mono=mono, down_for=down_for,
                 ensure=started)
    reported = state.get("reported_at")
    due = down_for >= DOWN_REPORT_S and not (
        isinstance(reported, (int, float)) and 0 <= now - reported < REPORT_EVERY_S
    )
    if due:
        state["reported_at"] = now  # before the child: a keeper run next minute starts no second one
    saved = _save(state)
    if due and not saved:
        _log(f"service_down ({down}) not reported: the keeper's state could not be saved")
    elif due:
        _report(down, down_for, started)


def _report(down: str, seconds: float, started: str | None) -> None:
    """`service_down` (crash-report plan B3), with the machine's consent: every
    live session's (hosted ones by their environment, registered ones by their
    `report_env`), else the login shell's variables and the CLI config's."""
    from .. import watch

    if not watch.reports_enabled():
        return
    try:
        live = watch.sessions_on_disk()
        login = None
        if not live:
            import asyncio

            login = asyncio.run(watch.login_env())
        allowed, why = watch.decide_machine(live, watch.config_base_url(), login)
    except Exception as exc:  # noqa: BLE001 -- unknown consent: no report
        allowed, why = False, f"consent unknown ({exc!r})"
    if not allowed:
        _log(f"service_down ({down}) not reported: {why}")
        return
    params = {
        "auto": True, "family": watch.Family.SERVICE_DOWN, "reason": down, "sid": None, "env": {},
        "facts": watch.bounded_facts({"down_s": round(seconds), "ensure": started, "sessions": len(live)}),
    }
    try:
        code, value = watch.report_blocking(params)
        said = watch.outcome(code, value)
    except OSError as exc:
        said = f"could not start: {exc}"
    _log(f"report service_down ({down}): {said}")


def _uninstalling() -> bool:
    """`probe uninstall` runs (its barrier is LIVE): the keeper does nothing."""
    from ...foundation import service_api as client

    return client.uninstall_barrier() is not None
