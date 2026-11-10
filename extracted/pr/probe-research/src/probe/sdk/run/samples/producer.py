"""A producer process (a Ray actor, a trainer rank, a Harbor job) joining the run a launcher exported
(`PROBE_RUN_ID`) as a data-writing `rank` writer with its own outbox, and taking part in the
hardware node-leader election (RL plan §4, review C4)."""

from __future__ import annotations

import atexit
import os
import re
import uuid
import weakref
from typing import TYPE_CHECKING, Any

from ... import errors

if TYPE_CHECKING:
    from ..run import Run

#: A producer's name in seals and plans (`validate_producer`): `rollout-0`, `trainer-0`.
PRODUCER_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:\-]{0,127}$")
#: How long a producer's release at exit may wait for its outbox; the rest stays queued for the
#: detached outbox worker, which outlives the process.
RELEASE_FLUSH_SECONDS = 10.0


def attach_producer(
    producer: str,
    *,
    run_id: str | None = None,
    client: Any = None,
    should_sample_hardware: bool | None = None,
    should_capture_logs: bool = True,
) -> Run:
    """This process's handle on the run, writing samples as ``producer``. A `rank` lease with no
    world size (closure never waits on a slot for it), a terminal status never sent, the lease
    released at exit with how the process ended. What the process prints is kept as its own log
    (``probe/run.rank<N>.log``, ``run.<pid>`` with no rank), unless a launcher on this host tees
    it or ``should_capture_logs`` is off (a helper process whose output its launcher already has).
    ``PROBE_MODE=disabled`` gives a handle that records nothing. Raises when there is no run
    to join; adapters catch it (fail open)."""
    from ..disabled import DisabledRun
    from ...settings.settings import Mode, resolve_mode

    if resolve_mode(None) is Mode.DISABLED:
        return DisabledRun(name=producer)  # type: ignore[return-value]
    if not PRODUCER_NAME.match(producer or ""):
        raise errors.ValidationError(f"producer {producer!r} must match {PRODUCER_NAME.pattern}")
    run_ref = run_id or os.environ.get("PROBE_RUN_ID", "").strip()
    if not run_ref:
        raise errors.ValidationError(
            "attach_producer() needs the run to join: PROBE_RUN_ID is not set. The process that "
            "opened the run exports it to its workers (a Ray runtime env, a launcher)."
        )
    if client is None:
        from ...client.client import Client

        client = Client()
    handle = _attach_as_rank(client, run_ref)
    from .samples import RunSamples

    handle.__dict__["_samples_view"] = RunSamples(handle, producer)
    from ...hardware import wiring as hw_wiring

    handle._hw_monitor = hw_wiring.maybe_start(client, handle, should_sample_hardware)
    if should_capture_logs:
        handle._start_capture(should_keep_files=False, log_name=_get_log_name())
    else:
        from ...capture.logs import early

        early.end_held_window()  # the tee `import probe` started has no run to own it here
    atexit.register(_release_at_exit, weakref.ref(handle))
    return handle


def _get_log_name() -> str:
    """A producer's own log: never the owner's ``probe/run.log``."""
    from probe.foundation.process_rank import read_process_rank

    launched = read_process_rank(os.environ)
    return f"probe/run.rank{launched.rank}.log" if launched is not None else f"probe/run.{os.getpid()}.log"


def _attach_as_rank(client: Any, run_ref: str) -> Run:
    raw_epoch = os.environ.get("PROBE_RUN_EPOCH", "").strip()
    write_epoch = int(raw_epoch) if raw_epoch.isdigit() else None
    handle = client.attach_run(
        run_ref,
        heartbeat=True,
        attached=True,
        write_epoch=write_epoch,
        session_id=str(uuid.uuid4()),
        is_producer=True,
    )
    # One producer's ending is not the run's: its close is the lease release, never a status.
    handle._sends_terminal_status = False
    return handle


def _get_ending_status() -> str:
    """How this process is ending, as `probe.init()`'s exit hooks recorded it, else completed."""
    from ... import fluent

    if fluent._in_hooks_process() and fluent._exit_recorded:
        return fluent._exit_status
    return "completed"


def _release_at_exit(handle_ref: weakref.ref) -> None:
    handle = handle_ref()
    if handle is None or getattr(handle, "_closed_status", None) is not None:
        return
    try:
        handle.finish(_get_ending_status(), flush_timeout=RELEASE_FLUSH_SECONDS)
    except Exception:  # noqa: BLE001 -- a release at exit never raises
        pass
