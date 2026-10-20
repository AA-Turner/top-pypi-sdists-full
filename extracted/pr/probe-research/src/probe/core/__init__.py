"""`probe.core`: what this Probe install can be asked to do, with no UI.

One library under every front end (Probe service plan, "Revised
architecture"): the `probe` CLI is a terminal over it, the Probe service a
socket over it, and the desktop app talks to the service. Each behaviour lives
here once.

    actions   configure, recorder, logout, uninstall, update, session_default
              (`probe.core.actions`): a request in, events out, an exit status back
    reads     status (`probe.core.reads`): `probe status --json`'s object
    events    the one event type, `probe wizard --json` schema v1 (`probe.core.events`)
    requests  each action's parameters, and their JSON (`probe.core.requests`)
    run       `python -m probe.core.run <action>`: one action as a child process

Today these are a facade over the CLI's own functions (the strangler step:
the code moves behind them later; the signatures stay).

Importing this package is light (stdlib and `probe`'s own small modules): no
typer, no prompt toolkit, no HTTP client, no `probe.cli`. Each operation
imports what it needs when it runs. `tests/test_core_run.py` pins it.
"""

from __future__ import annotations

from probe.core.actions import configure, logout, recorder, session_default, uninstall, update
from probe.core.events import EventSink
from probe.core.reads import status
from probe.core.requests import (
    ActionName,
    Agent,
    ConfigureRequest,
    Recorder,
    RecorderRequest,
    RequestError,
    SessionDefaultRequest,
    SessionState,
    StatusRequest,
)

__all__ = [
    "ActionName",
    "Agent",
    "ConfigureRequest",
    "EventSink",
    "Recorder",
    "RecorderRequest",
    "RequestError",
    "SessionDefaultRequest",
    "SessionState",
    "StatusRequest",
    "configure",
    "logout",
    "recorder",
    "session_default",
    "status",
    "uninstall",
    "update",
]
