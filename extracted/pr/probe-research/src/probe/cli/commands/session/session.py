"""probe session status: which session this is (or the daemon's), its capture and daemon blocks."""

from __future__ import annotations
import os
import sys
from pathlib import Path

import typer

from probe.cli.commands.commands import register_group
from ....sdk import agent_session, session_marker


def _capture_block(session_id: str, *, heal_cwd: str | None) -> dict:
    """The `capture` object every session surface returns.

    `heal_cwd` is None for callers that must NOT heal -- `session initialize`
    is the pi extension's own bridge, called before the extension's own spawn,
    and healing there would take the spawn away from the extension on every
    healthy session.
    """
    from probe.cli.capture import state as capture_state  # noqa: PLC0415 - keeps CLI startup cheap

    healed = None
    if heal_cwd is not None:
        healed = capture_state.ensure_capture(session_id, heal_cwd)
    state = capture_state.session_capture_state(session_id)

    reason = state.reason
    # THE PROBE KNOWS WHETHER A DAEMON RUNS; ONLY THE HEAL KNOWS WHY NOT.
    # `session_capture_state` reads a pid file, so every refusal it cannot see
    # collapses to `not started` -- an ephemeral session reported a crashed
    # daemon that never existed, where the spec promises `no session file`.
    # When the heal declined for a reason in the shared vocabulary, that
    # reason is the more specific true answer, so it wins. `off` and
    # `not applicable` are deliberately NOT in that vocabulary: the first is
    # carried by `effective`, and the second is not this surface's business.
    # Nor is `running`: the heal reads the marker alone (`ask_service=False`),
    # so for a session the Probe service hosts it says running while the
    # service's answer above (`not recording`) is the true one.
    if (
        healed is not None
        and not healed.started
        and not state.running
        and healed.reason != "running"
        and healed.reason in capture_state.REASONS
    ):
        reason = healed.reason
    return {"running": state.running, "pid": state.pid, "reason": reason}


def _effective(tracking: bool, capture: dict) -> str:
    """THREE states where the switch has two.

    `tracking` alone cannot distinguish "recording" from "says it is recording
    and nothing is listening", and that second state is the whole reason this
    field exists. The vocabulary is closed and rendered verbatim.
    """
    if not tracking:
        return "off"
    return "tracked" if capture["running"] else "tracked, not capturing session transcript"


# -- session ----------------------------------------------------------------
# The coding-agent conversation, not a Probe run. `untrack` is the off switch
# the track-work skill's explicit `off` drives: a DECLARATION that this conversation
# is not research, which the status line, the refresh hook and the change notice
# all read. Per session, never machine-wide -- a mute button that silenced the
# next conversation too is exactly the surprise nobody wants from one.
session_app = typer.Typer(
    no_args_is_help=True, help="this coding-agent session: is its work being tracked"
)

#: `probe session --help` order (session, switch, initialize, records and probe_config register them).
SESSION_GROUP = register_group(
    session_app,
    (
        "state", "untrack", "track", "toggle", "initialize", "owed", "export", "send", "delete",
        "undelete", "status", "parent", "default",
    ),
)


def _resolve_agent_session(session: str | None, *, read: bool = False) -> str:
    """This session's id for `probe session ...`, or exit 1 saying so.

    Resolves through the ``AGENTS`` table rather than naming variables here.
    The hardcoded ``CLAUDE_CODE_SESSION_ID or CODEX_THREAD_ID`` this replaces
    is why every `probe session` subcommand exited 1 under pi even though
    ``PI_SESSION_ID`` was in that table: an agent added to the table did not
    become an agent the switch could name.

    `read`: a command that only reads the session (`session status`, the
    `companion` logs) falls back to the session the Probe daemon watches. The
    daemon's `probe` calls run with a stripped environment that names no
    coding agent, only `PROBE_DAEMON_SESSION` (`daemon/worker/worker.py::probe_env`),
    so its `probe session status` answered "no session id" (62 times in 14
    days for one pi user) and it went hunting for the id with `printenv`, each
    hunt a question for the researcher. A fallback, after the agent's own
    variables: no coding agent's shell carries that variable, so the agent
    side resolves exactly as before. Never for a command that moves the
    switch: those stay the researcher's, however they are run.
    """
    resolved = session or agent_session.session_id_from_env() or (_daemon_session() if read else None)
    if not resolved:
        print("no session id: pass --session, or run inside a coding agent", file=sys.stderr)
        raise typer.Exit(1)
    return resolved


def _daemon_session() -> "str | None":
    """The session the Probe daemon watches, when the daemon runs this command:
    its `probe` calls carry no coding agent's variables, only
    `PROBE_DAEMON_SESSION` (`daemon/worker/worker.py::probe_env`), and no coding agent's
    shell carries that one. None anywhere else."""
    if agent_session.session_id_from_env() is not None:
        return None
    value = os.environ.get(agent_session.DAEMON_SESSION_ENV)
    return value if agent_session.valid_session_id(value) else None


#: `probe session status` run by the Probe daemon (`_daemon_session`) says why
#: these three are null.
DAEMON_STATUS_NOTE = ("run by the Probe daemon, not the coding agent: capture, effective and writes_allowed "
                      "describe the agent's own shell, so they are null here")


def _state_word(state: "str | None") -> "str | None":
    """A state as the WORD this version prints, with None preserved as null.

    Every JSON surface goes through here rather than printing the stored value:
    the config file and the session marker keep the longer `full`/`read-only`
    spellings for the older copies of this client that read them (see
    `session_marker.STATE_LABELS`), and a person reading `probe session status`
    should not have to know that. Readers of this output take both spellings --
    ours here, and pi's `parseState`.
    """
    return None if state is None else session_marker.state_label(state)


def _state_display(session_id: str, state: "str | None") -> "str | None":
    """The state as a PERSON reads it: `on (daemon)` / `read only (daemon)` /
    `off` where the Probe daemon records and reads, else the JSON word. Beside
    `state`, never instead of it -- pi and older hooks parse `state`."""
    if state is None:
        return None
    from probe.cli.commands.daemon.daemon import calling_agent

    return session_marker.state_display(
        state,
        session_marker.daemon_session(session_id, calling_agent()),
        session_marker.is_inline(session_id, state),
    )


def _daemon_block(session_id: str, state: str) -> "dict | None":
    """The daemon's status in the `daemon` state, else None.

    `status`/`reason` say whether the daemon is recording; `agent_writes` is the
    gate's own list of what stays the agent's (`session_marker.DAEMON_AGENT_WRITES`),
    so an agent asking "may I?" reads the answer rather than the gate's source.
    """
    status = session_marker.daemon_status(session_id, state)
    if status is None:
        return None
    return {
        "status": status[0],
        "reason": status[1],
        "agent_writes": sorted(session_marker.DAEMON_AGENT_WRITES),
        # Allowed only from inside a run's own job (`PROBE_RUN_ID` set).
        "agent_writes_in_run": sorted(session_marker.DAEMON_RUN_WRITES),
        "directed": "add --directed to any other write the researcher asks for",
    }


@session_app.command("status")
def session_status(
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
) -> None:
    """Whether this conversation is being tracked, and how that was decided."""
    from probe.shared.harness.harnesses.codex.env_warning import _codex_env_warning
    resolved = _resolve_agent_session(session, read=True)
    signal = session_marker.tracking_signal(resolved)
    session_state = session_marker.session_state(resolved)
    state = session_marker.read(resolved)
    default = session_marker.default_tracking()
    cwd_default, cwd_default_source = session_marker.resolve_tracking_default(None)
    cwd_state_default, _cwd_state_source = session_marker.resolve_state_default(None)
    if session_state is None:
        session_state = cwd_state_default
    tracking = session_marker.is_tracking(signal) if signal is not None else cwd_default
    machine_source = str(Path(os.path.abspath(os.fspath(session_marker.config_path()))))
    if signal is not None:
        decided_by = "session"
    elif cwd_default_source == "environment":
        decided_by = "environment"
    elif cwd_default_source in ("shipped", machine_source):
        decided_by = "machine default"
    else:
        decided_by = "folder default"
    # Run by the Probe daemon: its shell is not the coding agent's. Capture is read
    # by the agent's `PROBE_AGENT`, which the daemon's shell drops, so it answered
    # Claude Code's watcher for a pi session ("not installed"), and its heal can
    # start `tap start` for pi; `writes_allowed` is the agent's, and read by the
    # daemon it sounds like the daemon's own. Null, never guessed, and no heal.
    by_daemon = _daemon_session() is not None
    capture = None if by_daemon else _capture_block(resolved, heal_cwd=os.getcwd())
    reads_allowed = session_marker.state_allows_reads(session_state)
    # Only this session's own read: another session's harness is not this shell's.
    codex_env = None if by_daemon or session else _codex_env_warning(resolved)
    _print_json(
        {
            "session_id": resolved,
            "tracking": tracking,
            "state": _state_word(session_state),
            "label": _state_display(resolved, session_state),
            "reads_allowed": reads_allowed,
            # Whether the AGENT may record freely. Under `daemon` with a live
            # lease the daemon records and this is False; degraded, it is True.
            "writes_allowed": None if by_daemon else session_marker.agent_writes_freely(resolved, session_state),
            "daemon": _daemon_block(resolved, session_state),
            # Whether the researcher set the state (`explicit`) or it is a
            # machine default (`default`); `unrecorded`: an older client seeded
            # it (counts as explicit).
            "state_source": session_marker.state_source_label(resolved),
            # WHY, not just what. The status line shows two states on purpose, so
            # "off because I said so" and "off because this machine defaults off"
            # look identical there; this is where they separate.
            "decided_by": decided_by,
            "signal": signal,
            "machine_default": "on" if default else "off",
            "machine_default_state": _state_word(session_marker.default_session_state()),
            # Diagnostic only: this is what a NEW session started here would
            # inherit. It does not relabel an existing session signal, which may
            # have been seeded from another directory or changed explicitly.
            "cwd_default": "on" if cwd_default else "off",
            "cwd_default_source": cwd_default_source,
            "project": (state or {}).get("project"),
            "runs": len((state or {}).get("run_ids") or []),
            "running": tracking and session_marker.is_live(state),
            # WHETHER anything is actually listening, and the closed reason
            # when nothing is. `tracking: true` with no daemon is the lie this
            # pair exists to make unsayable.
            "capture": capture,
            "effective": None if by_daemon else _effective(tracking, capture),
            # `.probe.config` (paths Probe never records): where this session
            # started, and the researcher's answer about the files above it.
            "probe_config": _probe_config_block(resolved),
            **({"note": DAEMON_STATUS_NOTE} if by_daemon else {}),
            **({"warning": codex_env} if codex_env else {}),
        }
    )


def _probe_config_block(session_id: str) -> dict:
    pc = session_marker.probe_config()
    status, parents = session_marker.parent_config_status(session_id)
    launch = pc.launch_dir(session_marker.sessions_dir(), session_id) if session_marker.valid_session_id(session_id) else None
    return {
        "launch_dir": launch,
        "parent": status or None,
        "parent_files": [pc.shown(p.path) for p in parents],
    }
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
