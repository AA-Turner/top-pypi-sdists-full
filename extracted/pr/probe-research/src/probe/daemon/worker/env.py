"""what the worker's model runs and probe commands run with: model, environment, token counts."""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from probe.daemon.host import runctx
from probe.daemon.store.device import (
    LANE_WRITE,
    add_device_tokens)


@dataclass
class Session:
    session_id: str
    transcript: Path
    cwd: Path
    source: str
    home: Path = field(default_factory=Path.home)


# ---------------------------------------------------------------------------
# The agent.
# ---------------------------------------------------------------------------


def build_agent(instructions: str, *, model, state=None):
    from probe.daemon.agent.agent import build_agent as _build

    return _build(instructions, model=model, state=state)


def _default_model():
    from probe.daemon.agent.model import model as model_mod

    return model_mod.build(model_mod.endpoint())


def _new_usage():
    from pydantic_ai.usage import RunUsage

    return RunUsage()


def _tokens(usage) -> tuple[int, int, int]:
    """`(input, output, cached)` tokens of a run's usage (zeros for none), its
    tasks' included (`usage.TASK_DETAILS`, kept beside the run's own so they never
    count against its token limit)."""
    from probe.daemon.agent.model.usage import TASK_DETAILS

    details = getattr(usage, "details", None) or {}
    tasks = [int(details.get(key, 0) or 0) for key in TASK_DETAILS]
    return (int(getattr(usage, "input_tokens", 0) or 0) + tasks[0],
            int(getattr(usage, "output_tokens", 0) or 0) + tasks[1],
            int(getattr(usage, "cache_read_tokens", 0) or 0) + tasks[2])


def probe_env(session_id: str) -> dict[str, str]:
    """What the daemon's `probe` commands run with: its key, the session, no gate."""
    from probe.daemon.agent.model import model as model_mod

    try:
        ep = model_mod.endpoint()
    except model_mod.NoKey:
        return {"PROBE_DAEMON_SESSION": session_id}
    return {"PROBE_TOKEN": ep.key, "PROBE_BASE_URL": ep.base_url, "PROBE_DAEMON_SESSION": session_id}


def event_at_env(work_began: float | None) -> dict[str, str]:
    """What dates the daemon's `probe` writes at the work they file
    (`X-Probe-Event-At`, swarm friction R1): the time that work began, so the
    session's effort counts from there and not from when the daemon caught up.
    Nothing without one; the server clamps a time it cannot believe."""
    if work_began is None:
        return {}
    from datetime import datetime, timezone

    from probe.sdk.agent_session import EVENT_AT_ENV

    return {EVENT_AT_ENV: datetime.fromtimestamp(work_began, timezone.utc).isoformat()}


def run_side_env(agent: str, session_id: str, run_side: bool) -> dict[str, str]:
    """What marks a bite's `probe` writes as a run process's (`RUN_PROCESS_ENV`,
    in `forwarded_session`'s spelling, so `X-Probe-Write-Origin: run` goes with
    them) when every event the bite files is the daemon's own observation of a
    run (`Store.run_side_only`): a background job's start, end or files, none of
    the agent's own work. They are still filed as the watched session's, and add
    no agent-hours (swarm friction R41)."""
    if not run_side or not session_id:
        return {}
    from probe.sdk.agent_session import RUN_PROCESS_ENV

    return {RUN_PROCESS_ENV: f"{agent}:{session_id}"}


def forwarded_session(agent: str, session_id: str) -> dict[str, str]:
    """What the daemon's `probe` commands carry so what they create is filed as
    the WATCHED session's own work (`X-Probe-Agent-Session`, the server's origin
    record): the forwarded session, for a shell with no agent of its own."""
    from probe.sdk.agent_session import FORWARDED_SESSION_ENV

    return {FORWARDED_SESSION_ENV: f"{agent}:{session_id}"} if session_id else {}


def uncached_tokens(usage) -> int:
    """What a model response burned that a runaway would: fresh input plus output.
    Cache reads are INSIDE `input_tokens` (pydantic_ai `usage.py`), and a
    conversation re-sent every round is mostly cache reads, so counting them
    would trip the daily fuse on normal work."""
    fresh = int(getattr(usage, "input_tokens", 0) or 0) - int(getattr(usage, "cache_read_tokens", 0) or 0)
    return max(0, fresh) + int(getattr(usage, "output_tokens", 0) or 0)


#: Tokens a locked counter could not take yet, per lane: added to the next count
#: (each run's own in the daemon host, `runctx.Shared`).
_UNCOUNTED: dict[str, int] = {}
_uncounted = runctx.Shared(globals(), "_UNCOUNTED", dict)


def _count_device_tokens(n: int, lane: str = LANE_WRITE) -> None:
    """Best-effort: a counter that cannot be updated is logged, never fails (or
    replays) the bite it counts; what it could not take is counted next time."""
    uncounted = _uncounted.get()
    n += uncounted.pop(lane, 0)
    try:
        add_device_tokens(n, lane)
    except Exception as exc:  # noqa: BLE001
        uncounted[lane] = n
        log.warning("device token counter not updated (%s tokens): %s: %s", n, type(exc).__name__, exc)
from probe.daemon.worker.loop.reading import log  # noqa: E402 -- pieces need each other; the front door loads this one first
