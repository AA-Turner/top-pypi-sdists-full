"""`probe daemon ...`, `probe approvals`, `probe deny` (daemon v2).

    probe daemon worker ...     the AI process (capture spawns it; not for people)
    probe daemon status         is the AI process installable here, what it is doing
    probe daemon install        install the daemon's AI libraries (the `daemon` extra)
    probe daemon override ...   the daemon's own request to override a blocked check
    probe daemon session ...    the daemon's own look at the session it records
    probe daemon task ...       the daemon's own child agent for one long read
    probe approvals             questions the daemon holds for you; answer y/n here
    probe deny <id>             say no to one
"""

from __future__ import annotations

import json
import os
import sys
import time
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
    from probe.cli import install_pipeline

    # An install entry: an uninstall that stopped halfway is finished first;
    # one running refuses.
    gate = install_pipeline.gate(finish=True)
    if gate.refused:
        typer.echo(f"not installed: {gate.refused}", err=True)
        raise typer.Exit(2)
    # Identity first (plan clean-uninstall-reinstall R-T4), on every path, the
    # "already installed" one too: an earlier sign-in's daemon key of another
    # team is revoked and dropped (approved afresh where someone can) before
    # the daemon's libraries are provisioned or the key reused. The daemon
    # wrote to the old team.
    problems = _hold_identity()
    _provision(fresh=gate.finished)
    if problems:
        typer.echo("daemon mode is INCOMPLETE on this machine: " + "; ".join(problems), err=True)
        raise typer.Exit(1)


def _hold_identity() -> list[str]:
    """`identity_check.reconcile`, said: its lines, its problems with `!`.
    The problems (they make the install incomplete)."""
    from probe.cli import identity_check

    report = identity_check.reconcile(only_when_needed=True)
    for line in report.lines:
        typer.echo(line)
    for line in report.problems:
        typer.echo(f"! {line}", err=True)
    return list(report.problems)


def _provision(*, fresh: bool = False) -> None:
    """The daemon's libraries, by this install's method (`daemon_install`).
    `fresh`: an uninstall was just finished here, which took the CLI's link
    and `probe` command with it: the CLI is installed again side by side (the
    daemon extra included) and the service started, never "already installed"."""
    import dataclasses
    import subprocess

    from probe import __version__
    from probe.cli import updater

    if fresh:
        managed = _install_side_by_side(__version__)
        if managed is not None:
            if managed != 2:
                _start_service()
            if managed:
                raise typer.Exit(managed)
            return
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
        _start_service()
        return
    install = updater.detect_install()
    if install.method == updater.Method.UV_TOOL:
        managed = _install_side_by_side(__version__)
        if managed is not None and managed != 2:
            _start_service()
        if managed:
            raise typer.Exit(managed)
        if managed == 0:
            return  # never `Exit(0)`: the wizard's provisioning reads any Exit as a failed install
    # `all` stays (plan 2.11: the CLI's own dependencies leave core in the next
    # release), and so does whatever the install records beside it (#2043 review).
    # `daemon` is asked for here, not inferred: on a first switch to the daemon
    # neither the libraries nor the setting exist yet.
    kept = updater.faithful_kept_from_uv_receipt()
    if kept is None and install.method in (updater.Method.UV_TOOL, updater.Method.UV_TOOL_LEGACY):
        # Unreadable, or an editable or local `--with`, constraints: a reinstall
        # would drop what it cannot restate, which `probe update` refuses too.
        typer.echo(
            "this install's uv receipt cannot be restated (unreadable, or an editable or local `--with` "
            "package, constraints). Add the extra yourself: uv tool install "
            f"'probe-research[all,daemon]=={__version__}' with your own `--with` packages.",
            err=True,
        )
        raise typer.Exit(2)
    kept = kept or updater.KeptInstall()
    wanted = dataclasses.replace(kept, extras=tuple(sorted({"daemon", *kept.extras})))
    extras = ",".join(sorted({"all", "daemon", *kept.extras}))
    spec = f"probe-research[{extras}]=={__version__}"
    if install.method == updater.Method.UV_TOOL:
        # No `--force`: a plain install adds the missing packages to the
        # environment it has. `--force` deletes and rebuilds the environment --
        # on the newest Python uv has, unless told -- under every running `probe`
        # (2026-10-12: a daemon worker crashed reading its own files).
        cmd = updater.uv_tool_install_command(wanted, version=f"=={__version__}")
    elif install.method == updater.Method.UV_TOOL_LEGACY:
        # The old probe-agent tool owns `probe`: only `--force` takes it over.
        cmd = updater.uv_tool_install_command(wanted, force=True, version=f"=={__version__}")
    elif install.method == updater.Method.PIPX:
        cmd = ["pipx", "install", "--force", spec]
    elif install.method == updater.Method.PIP:
        cmd = [sys.executable, "-m", "pip", "install", spec]
    else:
        typer.echo(f"install the extra with your package manager: {spec} ({install.detail or install.method})", err=True)
        raise typer.Exit(2)
    _run_install(cmd)
    # The old probe-agent tool's interpreter is not the one the install filled:
    # ask the `probe` it left behind.
    python = _installed_python() if install.method == updater.Method.UV_TOOL_LEGACY else sys.executable
    ready = _fresh_ai_libraries(python)
    if ready is None and install.method == updater.Method.UV_TOOL:
        # A receipt that already asks for `daemon` makes the plain install a
        # no-op ("already installed") even when the packages themselves are
        # broken or gone: reinstall just those, in place.
        repair = [*cmd]
        for package in _DAEMON_PACKAGES:
            repair += ["--reinstall-package", package]
        _run_install(repair)
        ready = _fresh_ai_libraries(python)
    if ready is None:
        typer.echo(
            "the install finished but the daemon's AI libraries still do not import. Capture keeps running; "
            "daemon mode stays unavailable.",
            err=True,
        )
        raise typer.Exit(1)
    typer.echo("installed: daemon mode can run on this machine")
    _start_service()


def _start_service() -> None:
    """An install ends with the Probe service started, as the hooks start it
    (its start installs the OS keeper and the lifeboat): one line when it
    cannot run here, never a failure (`install_pipeline.start_service`)."""
    from probe.cli import install_pipeline

    note = install_pipeline.start_service()
    if note:
        typer.echo(note)


def _install_side_by_side(version: str) -> int | None:
    """The `daemon` extra the way every install goes (plan clean-uninstall-
    reinstall R-T1): the same version again, with the extra, in a folder of
    its own beside the running one (`<version>+g<N>`), checked, then switched
    to under the install lock -- never a `uv tool install` into the env every
    running `probe` reads its files from. The exit status (2: refused, or
    another update holds the install lock; 0 too when the switch waits for a
    quiet machine), or None where the side-by-side layout is not used (the
    caller installs as before)."""
    from probe._shared import installs

    from probe.cli import install_pipeline

    out = install_pipeline.install_cli(version, mode=install_pipeline.Mode.DAEMON, person=True)
    if out.unmanaged:
        return None
    if out.refused:
        typer.echo(f"not installed: {out.refused}", err=True)
        return 2
    if out.busy:
        typer.echo(f"not installed: {out.busy} (run `probe daemon install` again when it ends)", err=True)
        return 2
    for line in out.lines:
        typer.echo(line)
    if out.waiting and not out.ok:
        # Built and checked beside uv's own folder; the first switch waits for
        # a quiet machine (as `probe repair` says it): no failure.
        typer.echo(f"daemon mode {install_pipeline.QUIET_SWITCH} ({out.waiting}); "
                   "capture keeps running until then")
        return 0
    if out.waiting:
        typer.echo(out.waiting)
    if not out.ok or out.env is None:
        for line in out.problems or ["the install did not end up working"]:
            typer.echo(line, err=True)
        typer.echo("Capture keeps running; daemon mode stays unavailable.", err=True)
        return 1
    if _fresh_ai_libraries(str(installs.env_python(out.env))) is None:
        typer.echo(
            "the install finished but the daemon's AI libraries still do not import. Capture keeps running; "
            "daemon mode stays unavailable.",
            err=True,
        )
        return 1
    typer.echo("installed: daemon mode can run on this machine")
    return 0


#: The `daemon` extra's own packages: what a repair reinstalls.
_DAEMON_PACKAGES = ("pydantic-ai-slim", "pydantic-ai-harness", "pydantic-ai-skills")


def _run_install(cmd: list[str]) -> None:
    import subprocess

    typer.echo("$ " + " ".join(cmd))
    try:
        done = subprocess.run(cmd, timeout=600)  # noqa: S603 - fixed argv, no shell
    except (OSError, subprocess.TimeoutExpired) as exc:
        typer.echo(f"install failed: {exc}. Capture keeps running; daemon mode stays unavailable.", err=True)
        raise typer.Exit(1) from None
    if done.returncode != 0:
        typer.echo("install failed. Capture keeps running; daemon mode stays unavailable.", err=True)
        raise typer.Exit(done.returncode)


def _installed_python() -> str:
    """The interpreter of the `probe-research` uv tool environment, found through
    uv itself (`uv tool dir`, custom locations included), not a `probe` on PATH,
    which can still be the old probe-agent tool or another copy."""
    from pathlib import Path

    from probe.cli import bootstrap, updater

    env = bootstrap._persistent_tool_env(["uv", "tool", "dir"], updater.DIST)
    return str(Path(env) / "bin" / "python") if env else sys.executable


def _fresh_ai_libraries(python: str) -> str | None:
    """`ai_libraries` asked of a NEW interpreter: this process imported (or
    failed to import) before the install changed the environment."""
    import subprocess

    try:
        done = subprocess.run(  # noqa: S603 - that environment's own interpreter, no shell
            [python, "-c", _IMPORT_AI_LIBRARIES],
            capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=60, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    version = (done.stdout or "").strip()
    return version if done.returncode == 0 and version else None


@daemon_app.command("override", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def daemon_override(ctx: typer.Context) -> None:
    """The daemon's request to override a check that blocked one of its commands.

    Only meaningful inside the daemon, which handles it before it reaches here."""
    typer.echo("`probe daemon override` is the Probe daemon's own request; it does nothing when you run it. "
               "Answer the daemon's questions with `probe approvals`.", err=True)
    raise typer.Exit(2)


@daemon_app.command("session", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def daemon_session(ctx: typer.Context) -> None:
    """The daemon's own look at the session it records (open, outline, search,
    logbook, status). Only meaningful inside the daemon, which answers it before
    it reaches here."""
    typer.echo("`probe daemon session` is the Probe daemon's own look at the session it records; it does nothing "
               "when you run it.", err=True)
    raise typer.Exit(2)


@daemon_app.command("task", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def daemon_task(ctx: typer.Context) -> None:
    """The daemon's own child agent for one long read, in a context of its own.
    Only meaningful inside the daemon, which answers it before it reaches here."""
    typer.echo("`probe daemon task` is the Probe daemon's own helper for a long read; it does nothing when you run "
               "it.", err=True)
    raise typer.Exit(2)


def approvals_cmd(
    list_only: bool = typer.Option(False, "--list", help="only list them; ask nothing"),
) -> None:
    """Questions Probe is holding for you (the daemon's, and feedback for the Probe team). In a terminal,
    answer each y/n. Then the shell commands the daemon ran on Jev's yes in the last day, which nobody was asked.

    The coding agent normally puts these to you word for word with its question
    tool; this is the fallback for harnesses without one, and for anything left
    unanswered. Only a real terminal can answer (the agent's shell cannot)."""
    from probe.daemon import approvals as appr
    from probe.sdk import agent_session

    board = appr.Board()
    waiting = board.waiting()
    agent_sid = agent_session.session_id_from_env()
    in_agent = agent_sid is not None or agent_session.detect_agent() is not None
    # Whose Jev runs this shell sees (`_echo_jev_approved`): a coding agent its own
    # session's, and so does the daemon (its `probe` carries only PROBE_DAEMON_SESSION).
    daemon_sid = None if agent_sid else os.environ.get(agent_session.DAEMON_SESSION_ENV)
    own_sid = agent_sid or (daemon_sid if agent_session.valid_session_id(daemon_sid) else None)
    scoped = in_agent or bool(daemon_sid)
    if not waiting:
        typer.echo("nothing is waiting for you")
        _echo_jev_approved(own_sid, scoped=scoped)
        return
    # A CONVENIENCE, NOT A SECURITY BOUNDARY. The agent's shell has no terminal,
    # so this keeps it from answering here by accident; it cannot stop a process
    # of the same user that allocates a pseudo-terminal, nor one that writes the
    # answer file directly. What protects a yes is on the daemon's side: the
    # request's held action must still match (`approvals.verify_held`), and the
    # guard hook refuses the agent's plain writes into the approvals folder.
    # And a shell that carries a coding agent's session (`script -qc` included,
    # which keeps the environment) lists only: the researcher answers in a
    # terminal of their own, which carries no agent session.
    interactive = sys.stdin.isatty() and sys.stdout.isatty() and not list_only and not in_agent
    answered_feedback = False
    for req in waiting:
        q = req.question
        typer.echo(f"\n[{q.header}] {_indented(_shown(q.question), '    ', first=False)}\n"
                   f"  y = {q.yes_label}   n = {q.no_label}")
        # A long diff is asked here only (never cut in a chat question); print it whole.
        for key in ("command", "diff"):
            full = req.facts.get(key)
            if isinstance(full, str) and full and full not in q.question:
                typer.echo(f"  the whole {key}:\n{_indented(_shown(full), '    ')}")
        if not interactive:
            continue
        choice = typer.prompt("y/n", default="n").strip().lower()
        board.answer(req.id, q.yes_label if choice in ("y", "yes") else q.no_label, channel="terminal")
        answered_feedback = answered_feedback or req.policy == appr.FEEDBACK
    if answered_feedback:
        # Feedback has no daemon to act on its answer: send what was said yes to now.
        from .feedback_cli import flush_quietly

        flush_quietly()
    if in_agent:
        # `--list` too: the agent lists these in the daemon profile, whose guard
        # refuses its `probe deny`. Both answers are the researcher's, in their terminal.
        typer.echo("\n(this shell belongs to a coding agent, so it answers nothing: the researcher answers in a "
                   "terminal of their own, with `probe approvals` there, or says no with `probe deny <id>` there)")
    elif not interactive:
        typer.echo("\n(answer in your own terminal: `probe approvals`; say no with `probe deny <id>`)")
    _echo_jev_approved(own_sid, scoped=scoped)


#: Characters a terminal acts on or that hide text, by Unicode category: controls
#: (an escape sequence, a carriage return), formats (a bidi override, a zero-width
#: joiner), line and paragraph separators, surrogates, private-use and unassigned
#: code points (some terminals draw these with no width).
_HIDDEN = frozenset({"Cc", "Cf", "Zl", "Zp", "Cs", "Co", "Cn"})
#: And what a terminal draws with no width whatever its category: Unicode's
#: Default_Ignorable_Code_Point set (variation selectors, the combining grapheme
#: joiner, the Hangul and Khmer fillers, tags), which `unicodedata` cannot look
#: up. A string of variation selectors can carry a whole payload unseen.
_INVISIBLE = ((0x00AD, 0x00AD), (0x034F, 0x034F), (0x061C, 0x061C), (0x115F, 0x1160), (0x17B4, 0x17B5),
              (0x180B, 0x180F), (0x200B, 0x200F), (0x202A, 0x202E), (0x2060, 0x206F), (0x3164, 0x3164),
              (0xFE00, 0xFE0F), (0xFEFF, 0xFEFF), (0xFFA0, 0xFFA0), (0xFFF0, 0xFFF8), (0x1BCA0, 0x1BCA3),
              (0x1D173, 0x1D17A), (0xE0000, 0xE0FFF))


def _hidden(ch: str) -> bool:
    import unicodedata

    if ch in "\n\t":
        return False
    code = ord(ch)
    return unicodedata.category(ch) in _HIDDEN or any(lo <= code <= hi for lo, hi in _INVISIBLE)


def _shown(text: str) -> str:
    """`text` with each `_hidden` character printed as its escape (`\\x1b`,
    `\\ufe00`), so text the daemon's model wrote cannot redraw, hide or carry
    unseen part of a line. Line breaks and tabs stay; so do other spaces (NBSP,
    U+3000) and every printable script."""
    return "".join(ch.encode("unicode_escape").decode("ascii") if _hidden(ch) else ch for ch in text)


def _indented(text: str, pad: str, *, first: bool = True) -> str:
    """Each line of `text` after `pad` (the first too, unless `first` is False).
    `probe approvals`' own lines start at column 0 or 2, so with a 4-space pad a
    line the model wrote never starts where one of them does (a line the terminal
    wraps can still reach column 0)."""
    lines = text.split("\n")
    return "\n".join(pad + line if i or first else line for i, line in enumerate(lines))


#: How far back `probe approvals` lists the commands Jev ran without asking, and how many.
JEV_SHOWN_S = 24 * 3600
JEV_SHOWN = 20


def _echo_jev_approved(own_sid: str | None, *, scoped: bool) -> None:
    """The shell commands the daemon ran on Jev's yes in the last day
    (`store.jev_approved`), by session, newest first, each whole (Jev is never
    asked about one longer than `approvals.COMMAND_CHARS`). Nobody was asked
    about them, so this is where the researcher sees them (R2). It says when
    it shows fewer than ran, or could not read a session's logbook.

    A coding agent's shell (`scoped`) sees its own session's only: this output
    lands in its transcript, which is uploaded with that session, and another
    session's commands are another project's."""
    from probe.daemon import store

    if scoped and own_sid is None:
        # An agent whose session is unknown: none of them is its own. Said, not dropped.
        typer.echo("\n(what Jev ran without asking is listed by `probe approvals` in the researcher's own terminal)")
        return
    found = store.jev_approved(time.time() - JEV_SHOWN_S, JEV_SHOWN, session_id=own_sid if scoped else None)
    if not found.rows and not found.unreadable and not found.damaged:
        return
    which = "in this session, " if scoped else ""
    typer.echo(f"\nRun without asking you, on Jev's yes ({which}the last {JEV_SHOWN_S // 3600} hours, newest first):")
    by_session: dict[str, list[dict]] = {}
    for row in found.rows:
        by_session.setdefault(row["session_id"], []).append(row)
    for session_id, rows in by_session.items():
        typer.echo(f"  session {_shown(session_id)}")
        for row in rows:
            when = time.strftime("%Y-%m-%d %H:%M", time.localtime(row["at"]))
            if row["ended"] != "ran":
                ended = store.JEV_ENDINGS[row["ended"]]
            else:
                ended = "no exit code (timed out or stopped)" if row["exit_code"] is None else f"exit {row['exit_code']}"
            typer.echo(f"    {when}  p={row['lowest']}  {ended}")
            for line in _shown(row["command"]).split("\n"):
                typer.echo(f"      {line}")
    left_out = found.total - len(found.rows)
    if left_out:
        hidden = {sid: n - len(by_session.get(sid, [])) for sid, n in found.by_session.items()}
        where = ", ".join(f"session {_shown(sid)}: {n}" for sid, n in hidden.items() if n > 0)
        typer.echo(f"  and {left_out} more not shown ({where}): every one is in `probe companion log <session>`")
    elif found.rows:
        typer.echo("  (every decision the daemon made in a session: `probe companion log <session>`)")
    if found.unreadable:
        typer.echo(f"  ({found.unreadable} session logbook(s) could not be read just now (written by a newer Probe "
                   "CLI, damaged, or busy), so this list may be missing some)")
    if found.damaged:
        typer.echo(f"  ({found.damaged} logbook line(s) that name Jev are in a shape the daemon never writes, so "
                   "they are left out; this list may be missing some)")


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
#: `--writer` (Richard's approved text, 2026-10-13: ~/plans/writer-channel).
ASK_WRITER_HELP = ("Ask the daemon's writer to change the record (file runs, make or regroup an experiment). "
                   "Its reply says what it did.")
#: `--writer` refused: the writer records nothing in `read only (daemon)`.
ASK_WRITER_READ_ONLY = "not asked: Probe is read only for this session, so the daemon's writer records nothing."
#: `--writer` refused: the worker running now is from before requests (a reinstall
#: under a live session): nothing would take one.
ASK_WRITER_OLD_DAEMON = ("not asked: the Probe daemon running now is older than this CLI and takes no requests; "
                         "the next session's daemon does.")
ASK_WRITER_TOO_LONG = "not asked: a request is at most {n:,} characters."
ASK_NOTHING = "nothing in the team's records for this."
ASK_STILL_LOOKING = "still looking ({id}) - the answer will reach you as a [Probe] message."
ASK_FAILED = "ask {id} failed: {reason}"
ASK_ASKED = "asked ({id}) - the answer will reach you as a [Probe] message."
ASK_NO_WORKER = "asked ({id}) - the Probe daemon is not running; it restarts at the next prompt and answers then."
ASK_FINISHING = "asked ({id}) - the Probe daemon is finishing the previous session; it answers once that is done."
ASK_NO_DAEMON = "not asked: the Probe daemon does not run on this machine - use the Probe MCP."
ASK_SESSION_OFF = "not asked: Probe is off for this session."
#: `/probe inline` (the researcher's): the daemon is off, and the agent has the whole CLI.
ASK_SESSION_INLINE = (
    "not asked: Probe is inline for this session, so the daemon is off - search the team's "
    "work yourself with the `probe` CLI."
)
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
    writer: bool = typer.Option(False, "--writer", help=ASK_WRITER_HELP),
) -> None:
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
    if session_marker.is_inline(sid, state):
        typer.echo(ASK_SESSION_INLINE, err=True)
        raise typer.Exit(1)
    # `on (daemon)` and `read only (daemon)`: the daemon's reader answers in both.
    reads_only = state == session_marker.STATE_READ_ONLY and session_marker.daemon_session(sid, calling_agent())
    if (state != session_marker.STATE_DAEMON and not reads_only) or not mailbox.enabled(
        source=calling_agent()
    ):
        typer.echo(ASK_NO_DAEMON, err=True)
        raise typer.Exit(1)
    alive = mailbox.worker_alive(sid)
    if writer:
        _ask_writer(sid, question, wait=wait, alive=alive, reads_only=reads_only)
        return
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
    _wait_for(sid, ask.id)


def _ask_writer(sid: str, text: str, *, wait: bool, alive: bool, reads_only: bool) -> None:
    """`probe ask --writer`: a request for the daemon's WRITER (`requests.py`),
    filed in the mailbox's `requests/` folder -- never `asks/`, where a worker
    from before requests would hand it to the reader."""
    from probe.daemon import mailbox

    if reads_only:
        typer.echo(ASK_WRITER_READ_ONLY, err=True)
        raise typer.Exit(1)
    if len(text) > mailbox.REQUEST_MAX_CHARS:
        typer.echo(ASK_WRITER_TOO_LONG.format(n=mailbox.REQUEST_MAX_CHARS), err=True)
        raise typer.Exit(1)
    takes = alive and mailbox.accepts_requests(sid)
    if alive and not takes:
        typer.echo(ASK_WRITER_OLD_DAEMON, err=True)
        raise typer.Exit(1)
    req = mailbox.write_request(sid, text, wait=wait and takes)
    if not alive:
        # The next worker (this install's) takes it when it starts, at the next prompt.
        typer.echo(ASK_NO_WORKER.format(id=req.id))
        return
    finishing = mailbox.finishing(sid)
    if not wait or finishing:
        typer.echo((ASK_FINISHING if finishing else ASK_ASKED).format(id=req.id))
        return
    _wait_for(sid, req.id)


def _wait_for(sid: str, ask_id: str) -> None:
    """Hold the answer to `ask_id` (its heartbeat) and print it, up to WAIT_MAX_S."""
    import time

    from probe.daemon import mailbox

    deadline = time.monotonic() + mailbox.WAIT_MAX_S
    beat = 0.0
    try:
        while time.monotonic() < deadline:
            if time.monotonic() - beat >= mailbox.HEARTBEAT_S:
                mailbox.touch_heartbeat(sid, ask_id)
                beat = time.monotonic()
            msg = mailbox.claim_answer(sid, ask_id)
            if msg is not None:
                if msg.kind == mailbox.Kind.FAILED:
                    typer.echo(ASK_FAILED.format(id=ask_id, reason=msg.reason or "unknown"))
                    raise typer.Exit(1)
                typer.echo(ASK_NOTHING if msg.kind == mailbox.Kind.NOTHING else msg.text)
                return
            time.sleep(ASK_POLL_S)
        typer.echo(ASK_STILL_LOOKING.format(id=ask_id))
    finally:
        # Not waiting any more, however this ends: the answer is the hooks' now.
        mailbox.heartbeat_path(sid, ask_id).unlink(missing_ok=True)


ask_cmd.__doc__ = ASK_HELP
