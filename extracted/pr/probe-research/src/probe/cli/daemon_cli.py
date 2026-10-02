"""`probe daemon ...`, `probe approvals`, `probe deny` (daemon v2).

    probe daemon worker ...     the AI process (capture spawns it; not for people)
    probe daemon status         is the AI process installable here, what it is doing
    probe daemon install        install the daemon's AI libraries (the `daemon` extra)
    probe daemon override ...   the daemon's own request to override a blocked check
    probe approvals             questions the daemon holds for you; answer y/n here
    probe deny <id>             say no to one
"""

from __future__ import annotations

import json
import sys
from typing import Optional

import typer

daemon_app = typer.Typer(no_args_is_help=True, help="the Probe daemon that records a session for its agent")


#: `ai_libraries`'s imports, run by the installed copy's own Python.
_IMPORT_AI_LIBRARIES = (
    "import pydantic_ai, pydantic_ai_harness; "
    "print(getattr(pydantic_ai, '__version__', 'installed'))"
)
#: The installed copy's answer once it was yes: libraries do not vanish
#: mid-run, and each ask costs a fresh interpreter importing Pydantic AI.
_installed_copy_ready: dict[str, str] = {}


def _installed_copy() -> str | None:
    """The installed `probe`, when THIS process is a launcher's temporary copy
    (`updater.Method.EPHEMERAL`); else None.

    The tap starts the daemon's worker from the installed `probe` (its
    `probe_cli()`), never from a launcher's cache, so that copy's environment
    is the one whose AI libraries count. `npx probe-research` runs the newest
    CLI from uv's cache whenever the installed one is behind -- after every
    release -- and checking, or refusing to install into, the cache's
    environment failed every switch to the daemon until Probe was reinstalled."""
    from probe.cli import bootstrap, updater

    if updater.detect_install().method != updater.Method.EPHEMERAL:
        return None
    return bootstrap._installed_binary()


def _ai_libraries_of(binary: str) -> str | None:
    """`ai_libraries` asked of the environment `binary` runs in (`<env>/bin/probe`,
    the layout `bootstrap._is_this_install` reads too)."""
    import os
    import subprocess
    from pathlib import Path

    if binary in _installed_copy_ready:
        return _installed_copy_ready[binary]
    python = Path(os.path.realpath(binary)).parent / "python"
    try:
        done = subprocess.run(  # noqa: S603 - that install's own interpreter, no shell
            [str(python), "-c", _IMPORT_AI_LIBRARIES],
            capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=60, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    version = (done.stdout or "").strip()
    if done.returncode != 0 or not version:
        return None
    _installed_copy_ready[binary] = version
    return version


def ai_libraries() -> str | None:
    """The installed Pydantic AI version where the daemon runs, or None when the
    `daemon` extra is missing there: this CLI's environment, or the installed
    `probe`'s when this is a launcher's temporary copy (`_installed_copy`).

    IMPORTS them, on purpose: this is the READINESS check that gates choosing
    the daemon, provisioning it and `probe daemon install`, and a package that
    is present but broken (a missing transitive dependency) must read missing
    here. For a version on a status screen, see `located_ai_libraries`."""
    installed = _installed_copy()
    if installed is not None:
        return _ai_libraries_of(installed)
    try:
        import pydantic_ai  # noqa: F401
        import pydantic_ai_harness  # noqa: F401

        return getattr(pydantic_ai, "__version__", "installed")
    except ImportError:
        return None


def located_ai_libraries() -> str | None:
    """The same answer for DISPLAY, without importing: located and read from
    package metadata. Importing pydantic_ai costs ~1.5s, and the setup wizard's
    status snapshot reads this on every launch only to print a version. Never
    use it to decide whether the daemon can run -- `ai_libraries` does that."""
    import importlib.metadata
    import importlib.util

    if any(
        importlib.util.find_spec(module) is None
        for module in ("pydantic_ai", "pydantic_ai_harness")
    ):
        return None
    try:
        return importlib.metadata.version("pydantic-ai-slim")
    except importlib.metadata.PackageNotFoundError:
        return "installed"


@daemon_app.command("worker", hidden=True, context_settings={"allow_extra_args": True,
                                                             "ignore_unknown_options": True})
def daemon_worker(ctx: typer.Context) -> None:
    """The AI process. Capture starts it beside a session in `daemon` state."""
    from probe.daemon import worker

    raise typer.Exit(worker.main(list(ctx.args)))


@daemon_app.command("status")
def daemon_status(as_json: bool = typer.Option(False, "--json")) -> None:
    """Can the daemon run here, and what is it doing."""
    from pathlib import Path

    from probe.daemon import approvals as appr
    from probe.daemon import store as store_mod
    from probe.daemon import trace as trace_mod
    from probe.daemon import usage as usage_mod

    info: dict = {"ai_libraries": ai_libraries() or "missing: Who records in the wizard (switch it to the daemon, or Enter on it) installs them"}
    base = store_mod.state_dir()
    sessions = []
    for path in sorted(base.glob("*.sqlite"), key=lambda p: p.stat().st_mtime, reverse=True)[:5]:
        try:
            st = store_mod.Store(path)
        except Exception:  # noqa: BLE001 -- a status line never fails on one bad file
            continue
        pending = st.db.execute("SELECT count(*) AS n, min(noticed) AS oldest FROM events WHERE bite IS NULL").fetchone()
        last = st.recent_bites(1)
        live = st.live_conversation()
        sessions.append({
            "session": path.stem,
            "queued_events": pending["n"],
            "writes": st.writes_count(),
            "last_bite": dict(last[0]) if last else None,
            "tokens_today": st.tokens_today(),
            # Every model round of the session (T10): tokens, the cached share, dollars.
            "usage": st.usage_summary(),
            "conversation": ({"runs": live["runs"], "compactions": live["compactions"]}
                             if live is not None else None),
            # The worker's log and each agent's full trace (`probe/daemon/trace.py`).
            "folder": str(trace_mod.session_dir(path.stem)),
        })
        st.close()
    info["sessions"] = sessions
    info["questions_waiting"] = [{"id": r.id, "policy": r.policy, "question": r.question.question}
                                 for r in appr.Board().waiting()]
    errors = Path(base.parent / "daemon-errors.log")
    if errors.exists():
        info["recent_errors"] = errors.read_text(encoding="utf-8").splitlines()[-5:]
    if as_json:
        typer.echo(json.dumps(info, indent=1, default=str))
        return
    typer.echo(f"AI libraries: {info['ai_libraries']}")
    for s in sessions:
        conv = s["conversation"]
        extra = (f"; one conversation: {conv['runs']} runs, {conv['compactions']} compactions"
                 if conv is not None else "")
        # `usage` counts every model round of the session, not today's.
        typer.echo(f"session {s['session']}: {s['queued_events']} events queued, {s['writes']} writes; "
                   f"since the session started: {usage_mod.fmt_usage(s['usage'])}{extra}")
        if Path(s["folder"]).is_dir():
            typer.echo(f"  log and traces: {s['folder']}")
    for q in info["questions_waiting"]:
        typer.echo(f"waiting for you: {q['id']} ({q['policy']}) {q['question']}")
    for line in info.get("recent_errors", []):
        typer.echo(f"error: {line}")


@daemon_app.command("install")
def daemon_install() -> None:
    """Install the daemon's AI libraries into this CLI's environment (the `daemon` extra)."""
    import subprocess

    from probe import __version__
    from probe.cli import updater

    installed = _installed_copy()
    if installed is not None:
        # This copy is thrown away on exit and the daemon never runs from it:
        # the installed `probe` installs into its own environment, by its own
        # install method, at its own version.
        cmd = [installed, "daemon", "install"]
        typer.echo("$ " + " ".join(cmd))
        try:
            done = subprocess.run(cmd, timeout=600)  # noqa: S603 - our own CLI, no shell
        except (OSError, subprocess.TimeoutExpired) as exc:
            typer.echo(f"install failed: {exc}. Capture keeps running; daemon mode stays unavailable.", err=True)
            raise typer.Exit(1) from None
        if done.returncode != 0:
            raise typer.Exit(done.returncode)
        return
    if ai_libraries():
        typer.echo(f"already installed (Pydantic AI {ai_libraries()})")
        return
    install = updater.detect_install()
    # `all` stays (plan 2.11: the CLI's own dependencies leave core in the next
    # release), and so does whatever the install records beside it (#2043 review).
    kept = updater.kept_from_uv_receipt() or updater.KeptInstall()
    extras = ",".join(sorted({"all", "daemon", *kept.extras}))
    spec = f"probe-research[{extras}]=={__version__}"
    if install.method in (updater.Method.UV_TOOL, updater.Method.UV_TOOL_LEGACY):
        cmd = ["uv", "tool", "install", "--force", spec]
        for requirement in kept.with_packages:
            cmd += ["--with", requirement]
        if kept.python:
            cmd += ["--python", kept.python]
    elif install.method == updater.Method.PIPX:
        cmd = ["pipx", "install", "--force", spec]
    elif install.method == updater.Method.PIP:
        cmd = [sys.executable, "-m", "pip", "install", spec]
    else:
        typer.echo(f"install the extra with your package manager: {spec} ({install.detail or install.method})", err=True)
        raise typer.Exit(2)
    typer.echo("$ " + " ".join(cmd))
    try:
        done = subprocess.run(cmd, timeout=600)
    except (OSError, subprocess.TimeoutExpired) as exc:
        typer.echo(f"install failed: {exc}. Capture keeps running; daemon mode stays unavailable.", err=True)
        raise typer.Exit(1) from None
    if done.returncode != 0:
        typer.echo("install failed. Capture keeps running; daemon mode stays unavailable.", err=True)
        raise typer.Exit(done.returncode)
    typer.echo("installed: daemon mode can run on this machine")


@daemon_app.command("override", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def daemon_override(ctx: typer.Context) -> None:
    """The daemon's request to override a check that blocked one of its commands.

    Only meaningful inside the daemon, which handles it before it reaches here."""
    typer.echo("`probe daemon override` is the Probe daemon's own request; it does nothing when you run it. "
               "Answer the daemon's questions with `probe approvals`.", err=True)
    raise typer.Exit(2)


def approvals_cmd(
    list_only: bool = typer.Option(False, "--list", help="only list them; ask nothing"),
) -> None:
    """Questions the Probe daemon is holding for you. In a terminal, answer each y/n.

    The coding agent normally puts these to you word for word with its question
    tool; this is the fallback for harnesses without one, and for anything left
    unanswered. Only a real terminal can answer (the agent's shell cannot)."""
    from probe.daemon import approvals as appr

    board = appr.Board()
    waiting = board.waiting()
    if not waiting:
        typer.echo("nothing is waiting for you")
        return
    # A CONVENIENCE, NOT A SECURITY BOUNDARY. The agent's shell has no terminal,
    # so this keeps it from answering here by accident; it cannot stop a process
    # of the same user that allocates a pseudo-terminal, nor one that writes the
    # answer file directly. What protects a yes is on the daemon's side: the
    # request's held action must still match (`approvals.verify_held`), and the
    # guard hook refuses the agent's plain writes into the approvals folder.
    interactive = sys.stdin.isatty() and sys.stdout.isatty() and not list_only
    for req in waiting:
        q = req.question
        typer.echo(f"\n[{q.header}] {q.question}\n  y = {q.yes_label}   n = {q.no_label}")
        # A long diff is asked here only (never cut in a chat question); print it whole.
        for key in ("command", "diff"):
            full = req.facts.get(key)
            if isinstance(full, str) and full and full not in q.question:
                typer.echo(f"  the whole {key}:\n{full}")
        if not interactive:
            continue
        choice = typer.prompt("y/n", default="n").strip().lower()
        board.answer(req.id, q.yes_label if choice in ("y", "yes") else q.no_label, channel="terminal")
    if not interactive:
        typer.echo("\n(answer in your own terminal: `probe approvals`; say no with `probe deny <id>`)")


def deny_cmd(request_id: str = typer.Argument(..., help="the question's id, e.g. 7f3a09c1"),
             note: Optional[str] = typer.Option(None, "--why")) -> None:
    """Say no to a question the Probe daemon holds. Anyone may say no."""
    from probe.daemon import approvals as appr

    board = appr.Board()
    req = board.get(request_id.removeprefix("Probe ").strip())
    if req is None or req.state != appr.WAITING:
        typer.echo(f"no waiting question {request_id}", err=True)
        raise typer.Exit(1)
    board.answer(req.id, req.question.no_label, channel="deny")
    typer.echo(f"said no to {req.id}: {req.question.question[:120]}")


#: `probe ask`'s text (the researcher's review folder:
#: `~/daemon-prompts/reads/agent-facing/probe-ask.NEW.md`).
ASK_HELP = ("Ask the Probe daemon about the team's prior work. Returns at once; the answer arrives later as a "
            "[Probe] message.")
ASK_ARG_HELP = "What you want to know - short is fine; the daemon sees the session."
ASK_WAIT_HELP = "Wait for the answer and print it - for when you cannot go on without it. Give the shell command a long timeout."
ASK_NOTHING = "nothing in the team's records for this."
ASK_STILL_LOOKING = "still looking ({id}) - the answer will reach you as a [Probe] message."
ASK_FAILED = "ask {id} failed: {reason}"
ASK_ASKED = "asked ({id}) - the answer will reach you as a [Probe] message."
ASK_NO_WORKER = "asked ({id}) - the Probe daemon is not running; it restarts at the next prompt and answers then."
ASK_FINISHING = "asked ({id}) - the Probe daemon is finishing the previous session; it answers once that is done."
ASK_NO_DAEMON = "not asked: the Probe daemon does not run on this machine - use the Probe MCP."
ASK_SESSION_OFF = "not asked: Probe is off for this session."
ASK_NO_SESSION = "not asked: no coding agent session found in this shell's environment."
ASK_EMPTY = "give a question"
#: How often a waiting `probe ask --wait` looks for its answer.
ASK_POLL_S = 0.5


def calling_agent() -> str | None:
    """The coding agent this shell belongs to (`CLAUDE_CODE_SESSION_ID` ->
    claude_code, `CODEX_THREAD_ID` -> codex, `PI_SESSION_ID` -> pi), or None."""
    from probe.sdk import agent_session

    resolved = agent_session.session_agent_from_env()
    return resolved[0] if resolved else None


def ask_cmd(
    question: str = typer.Argument("", help=ASK_ARG_HELP, show_default=False),
    wait: bool = typer.Option(False, "--wait", help=ASK_WAIT_HELP),
) -> None:
    import time

    from probe.daemon import mailbox
    from probe.sdk import agent_session, session_marker

    question = " ".join(question.split())
    if not question:
        typer.echo(ASK_EMPTY, err=True)
        raise typer.Exit(1)
    sid = agent_session.session_id_from_env()
    if not sid:
        typer.echo(ASK_NO_SESSION, err=True)
        raise typer.Exit(1)
    state = session_marker.session_state(sid)
    if state == session_marker.STATE_OFF:
        typer.echo(ASK_SESSION_OFF, err=True)
        raise typer.Exit(1)
    # `on (daemon)` and `read only (daemon)`: the daemon's reader answers in both.
    reads_only = state == session_marker.STATE_READ_ONLY and session_marker.daemon_session(sid, calling_agent())
    if (state != session_marker.STATE_DAEMON and not reads_only) or not mailbox.enabled(source=calling_agent()):
        typer.echo(ASK_NO_DAEMON, err=True)
        raise typer.Exit(1)
    alive = mailbox.worker_alive(sid)
    ask = mailbox.write_ask(sid, question, wait=wait and alive)
    if not alive:
        # Nothing would answer while the agent blocks: the worker restarts only at
        # the next prompt, so a wait here would never end early.
        typer.echo(ASK_NO_WORKER.format(id=ask.id))
        return
    finishing = mailbox.finishing(sid)
    if not wait or finishing or not mailbox.status_path(sid).exists():
        # A wait only while a reader serves this session (its status file) and no
        # handover is pending: otherwise nothing may take the ask for a while, and
        # the answer arrives as a [Probe] message instead.
        typer.echo((ASK_FINISHING if finishing else ASK_ASKED).format(id=ask.id))
        return
    deadline = time.monotonic() + mailbox.WAIT_MAX_S
    beat = 0.0
    try:
        while time.monotonic() < deadline:
            if time.monotonic() - beat >= mailbox.HEARTBEAT_S:
                mailbox.touch_heartbeat(sid, ask.id)
                beat = time.monotonic()
            msg = mailbox.claim_answer(sid, ask.id)
            if msg is not None:
                if msg.kind == mailbox.Kind.FAILED:
                    typer.echo(ASK_FAILED.format(id=ask.id, reason=msg.reason or "unknown"))
                    raise typer.Exit(1)
                typer.echo(ASK_NOTHING if msg.kind == mailbox.Kind.NOTHING else msg.text)
                return
            time.sleep(ASK_POLL_S)
        typer.echo(ASK_STILL_LOOKING.format(id=ask.id))
    finally:
        # Not waiting any more, however this ends: the answer is the hooks' now.
        mailbox.heartbeat_path(sid, ask.id).unlink(missing_ok=True)


ask_cmd.__doc__ = ASK_HELP
