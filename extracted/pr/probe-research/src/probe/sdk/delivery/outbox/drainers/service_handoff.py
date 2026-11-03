"""Hand a training process's outbox drainer and box watcher to a Probe service running here (plan Q5),
else do what the SDK did before; never a credential (DESIGN.md). Request core: foundation handoff.py."""

from __future__ import annotations

import os
import sys

from probe.foundation.service_api.handoff import _ask, _cwd, _platform_ok, _version, env_credential, runtime_env


def _background_env() -> dict | None:
    """The env for a child, when this process may hand one off at all."""
    if not _platform_ok() or env_credential():
        return None
    return runtime_env()


def drain(directory: str) -> str | None:
    """Ask the service to drain the outbox folder `directory`. Its answer's state
    (`protocol.BackgroundState`: STARTED, a child starts; RUNNING, a drainer holds the
    outbox's lease or is starting), or None: not taken, fork as before (an unanswered request
    too: two drainers meet at the lease and one steps aside). Never raises."""
    try:
        env = _background_env()
        if env is None:
            return None
        from probe.sdk.agent_session import EVENT_AT_ENV, RUN_PROCESS_ENV
        from probe.foundation.service_api.wire import Method

        # A drainer sends every writer's ops, each with its own date and origin
        # (`journal._delivery_scope`), so it inherits neither from this process
        # (`outbox_worker._worker_env`).
        env.pop(EVENT_AT_ENV, None)
        env.pop(RUN_PROCESS_ENV, None)
        path, cwd = os.path.abspath(str(directory)), _cwd()
        _, answer = _ask(Method.OUTBOX_DRAIN, lambda c, deadline, sent: c.drain_outbox(
            path, sys.executable, env, cwd=cwd, deadline=deadline, on_sent=sent, client_version=_version()))
        return answer.get("state") if answer else None
    except Exception:  # noqa: BLE001 -- a hand-off may never break an enqueue
        return None


def box_watch(directory: str | None = None) -> str | None:
    """Ask the service to watch the box registry `directory` (default: this process's), on a
    thread of its own since X9. Its answer's state, or None: not taken, spawn as before. Never
    raises. `PROBE_BOX_DIR` is the wire name every service release reads."""
    try:
        env = _background_env()
        if env is None:
            return None
        from probe.sdk.run.watcher import registry

        env["PROBE_BOX_DIR"] = os.path.abspath(str(directory if directory is not None else registry.default_dir()))
        from probe.foundation.service_api.wire import Method

        cwd = _cwd()
        _, answer = _ask(Method.BOX_WATCH, lambda c, deadline, sent: c.watch_box(
            sys.executable, env, cwd=cwd, deadline=deadline, on_sent=sent, client_version=_version()))
        return answer.get("state") if answer else None
    except Exception:  # noqa: BLE001 -- the watcher is never the run's problem
        return None
