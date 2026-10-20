"""The actions the desktop app and the Probe service ask for, with no UI.

A strangler facade (Probe service plan, T1): every action here CALLS today's
implementation, the `probe wizard` function behind `probe wizard --action <a>
--yes --json`, with exactly the flags the desktop app passes for it today
(`src-tauri/src/wizard.rs`), and `session_default` the `probe session default`
command. Nothing is re-implemented, so an action here and that command cannot
do different things; `tests/test_core_run.py` holds the two side by side.
Later steps move the code behind these functions; their signatures stay.

One refusal is the facade's own: a wizard action from inside a coding agent's
session the Probe daemon records (`_refuse_from_daemon_session`), which the
daemon profile's guard refuses as `probe wizard` but cannot see by this name.

Each action takes its request and an event sink and returns the run's exit
status, the one `probe wizard` exits with (0 done, 1 failed, 2 usage, 75 busy,
130 interrupted during a browser approval, 128+N stopped by signal N). Its
events are `probe.core.events` schema v1, `done` last however it ends: to
`sink` when one is given, else to the process's real stdout, as `--json` writes
them. Either way the run's own text, and its child processes', go to stderr.

The CLI is imported inside each action, never at module level: `import
probe.core` stays light.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

from probe import errors
from probe.core import events
from probe.core.requests import (
    ActionName,
    ConfigureRequest,
    Recorder,
    RecorderRequest,
    SessionDefaultRequest,
    SessionState,
)

#: Every parameter of `probe.cli.main.wizard`, as typer hands it over for a
#: command line that does not use it. Called as a function, an omitted one would
#: be its truthy `typer.Option` default instead, so every one is named (the test
#: suite fails when `wizard` grows a parameter this does not name).
WIZARD_DEFAULTS: dict[str, Any] = {
    "agent": None,
    "tracking": None,
    "capture": None,
    "auto_update": None,
    "agent_rules": None,
    "capy_project": None,
    "channel": None,
    "uninstall": False,
    "action": None,
    "folder": None,
    "yes": False,
    "experimental": False,
    "token": None,
    "base_url": None,
    "context": None,
    "ingest_token": None,
    "hmac_secret": None,
    "endpoint_only": False,
    "no_browser": False,
    "who_records": None,
    "json_output": False,
    "auth_code": None,
    "reinstall": False,
}


def wizard_flags(action: ActionName, request: object = None) -> dict[str, Any]:
    """The `probe wizard` flags an action runs as, beyond `WIZARD_DEFAULTS`:
    always `--action <a> --yes --json`, plus what the request says."""
    flags: dict[str, Any] = {"action": str(action), "yes": True, "json_output": True}
    if isinstance(request, ConfigureRequest):
        flags.update(
            agent=[agent.value for agent in request.agents],
            tracking=request.tracking,
            capture=request.capture,
            auto_update=request.auto_update,
            agent_rules=request.agent_rules,
            reinstall=request.reinstall,
        )
    elif isinstance(request, RecorderRequest):
        flags["who_records"] = request.who_records.value
    return flags


def configure(request: ConfigureRequest, sink: events.EventSink | None = None) -> int:
    """Install and configure Probe for `request.agents`: `probe wizard --action
    configure --yes --json --agent A ...`, with `--[no-]tracking`, `--[no-]capture`,
    `--[no-]auto-update` and `--[no-]agent-rules` for each capability the request
    names. One it leaves out is a flag left out: kept as the device has it."""
    return _wizard(sink, wizard_flags(ActionName.CONFIGURE, request))


def recorder(request: RecorderRequest | Recorder | str, sink: events.EventSink | None = None) -> int:
    """Switch who records: `probe wizard --action recorder --who-records W --yes --json`."""
    if not isinstance(request, RecorderRequest):
        request = RecorderRequest(request)  # an unknown word: RequestError, before anything runs
    return _wizard(sink, wizard_flags(ActionName.RECORDER, request))


def logout(sink: events.EventSink | None = None) -> int:
    """`probe wizard --action logout --yes --json`."""
    return _wizard(sink, wizard_flags(ActionName.LOGOUT))


def uninstall(sink: events.EventSink | None = None) -> int:
    """`probe wizard --action uninstall --yes --json`."""
    return _wizard(sink, wizard_flags(ActionName.UNINSTALL))


def update(sink: events.EventSink | None = None) -> int:
    """`probe wizard --action update --yes --json`. What asked for it is read
    from the environment, as the wizard reads it (`update_report.TRIGGER_ENV`:
    the app sets `manual`)."""
    return _wizard(sink, wizard_flags(ActionName.UPDATE))


def session_default(
    state: SessionDefaultRequest | SessionState | str, sink: events.EventSink | None = None
) -> int:
    """Set the machine's default for new sessions: `probe session default
    <state>` itself, so the same refusal from inside a session the Probe daemon
    records (exit 2), the same write, the same object printed (to stderr here).

    Not a wizard action, so its events are its own: a `result` row for the
    device (`agent` null, `{"session_default": <state>}` asked for and read
    back), then `done`. `ok` is the default a new session now gets, read back.
    """
    request = state if isinstance(state, SessionDefaultRequest) else SessionDefaultRequest(state)
    return _run(sink, lambda: _apply_session_default(request.state))


def _cli() -> Any:
    """The `probe.cli.main` MODULE. (`from probe.cli import main` is the
    package's `main()` function, which shadows it.)"""
    import importlib

    return importlib.import_module("probe.cli.main")


def _wizard(sink: events.EventSink | None, flags: dict[str, Any]) -> int:
    def run_wizard() -> None:
        _refuse_from_daemon_session(flags["action"])
        main = _cli()
        main.begin_command()
        main.wizard(**{**WIZARD_DEFAULTS, **flags})

    return _run(sink, run_wizard)


def _refuse_from_daemon_session(action: str) -> None:
    """A wizard action run from inside a coding agent's session the Probe daemon
    records (`<sid>.profile`, the lean plugin's mark): exit 2, nothing changed.

    The daemon profile's guard refuses `probe wizard` there, typed or as `python
    -m probe.cli`, and this facade is one more way to run the same actions --
    switch who records, turn capture off, sign out, uninstall -- which no guard
    copy knows by name. So it refuses them itself, however the call is wrapped,
    as `_refuse_switch_from_agent` does for the researcher's switch. The
    researcher's own terminal, the desktop app and the Probe service (a clean
    environment) carry no agent session, so they are never refused.
    """
    import typer

    from probe.sdk import agent_session, session_marker

    session_id = agent_session.session_id_from_env()
    if not session_id or session_marker.session_profile(session_id) != session_marker.RECORDER_DAEMON:
        return
    message = session_marker.DAEMON_PROFILE_DENY.format(matched=f"probe wizard --action {action}")
    print(message, file=sys.stderr)
    events.error(events.ErrorCode.USAGE, message)
    raise typer.Exit(2)


def _run(sink: events.EventSink | None, body: Callable[[], None]) -> int:
    """`body` in an event session, as the exit status `probe` would give it.

    The session writes the events, `done` included, however the body ends; this
    only turns the ending into the status `probe.cli.main.main` returns for it.
    Anything else (a bug) propagates, after its `error` and `done` events.
    """
    import typer

    main = _cli()
    try:
        with events.session(True, sink=sink):
            body()
    except typer.Exit as exc:
        return int(exc.exit_code or 0)
    except typer.Abort:
        print("aborted", file=sys.stderr)
        return 1
    except main.ClickException as exc:  # usage errors (`typer.BadParameter`)
        exc.show()
        return exc.exit_code or 2
    except SystemExit as exc:  # SIGTERM / SIGHUP (`events._stop`), or a stray one
        if isinstance(exc.code, int):
            return exc.code
        if exc.code is not None:
            print(str(exc.code), file=sys.stderr)
            return 1
        return 0
    except (errors.RosError, OSError) as exc:  # a server refusal or a local path: no traceback
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


def _apply_session_default(state: SessionState) -> None:
    """`probe session default <state>`, called as a function inside this run's
    session: its refusal from an agent the Probe daemon records (exit 2), its
    write (exit 1 when it fails) and the object it prints, all its own. The
    device's row is its outcome, with the default a new session now gets."""
    import typer

    from probe.sdk import session_marker

    main = _cli()
    events.begin_result(ActionName.SESSION_DEFAULT.value, [None])
    requested = {"session_default": state.value}
    try:
        main.session_default(value=state.value, folder=None)
    except typer.Exit as exc:
        # The command said why on stderr; the row names what did not happen.
        refused = exc.exit_code == 2
        events.agent_result(
            None, requested=requested, actual=None, ok=False,
            message=(
                session_marker.RESEARCHER_SWITCH_DENY.format(matched="probe session default")
                if refused else f"could not update {session_marker.config_path()}"
            ),
        )
        raise
    now = session_marker.state_label(session_marker.default_session_state())
    events.agent_result(
        None, requested=requested, actual={"session_default": now}, ok=now == state.value,
        message="" if now == state.value else f"saved, but this environment sets new sessions to {now}",
    )
