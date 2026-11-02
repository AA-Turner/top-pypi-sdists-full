"""turn Probe on/read/off for this conversation or by default: probe session state/track/untrack/toggle/default."""

from __future__ import annotations
import os
import sys
from pathlib import Path

import typer
from ....sdk import agent_session, session_marker
from probe.cli.commands.session.session import (
    _capture_block,
    _daemon_block,
    _resolve_agent_session,
    _state_display,
    _state_word,
    session_app,
)


def _require_tracking_state(session_id: str, on: bool) -> None:
    """Fail unless the signal on disk matches the requested state.

    The setter deliberately returns False instead of raising for both invalid
    ids and filesystem failures. A host switch only has an exit code, so
    success must mean the authoritative read-back agrees -- otherwise Pi can
    announce that an opt-out landed while the old value is still active.
    """
    expected = "on" if on else "off"
    if session_marker.tracking_signal(session_id) == expected:
        return
    print(
        f"could not set tracking {expected} for session {session_id}",
        file=sys.stderr,
    )
    raise typer.Exit(1)


def _require_state(session_id: str, state: str) -> None:
    """Fail unless the canonical file on disk now reads `state`.

    Same contract as `_require_tracking_state`: the setter returns False rather
    than raising, a host switch only has an exit code, so success must mean the
    authoritative read-back agrees. Announcing that an opt-out landed while the
    old value is still active is the one failure this must never produce.
    """
    if session_marker.session_state(session_id) == state:
        return
    print(
        f"could not set probe state {state} for session {session_id}",
        file=sys.stderr,
    )
    raise typer.Exit(1)


def _switch_word(session_id: str, value: str) -> str:
    """A typed switch word to the state it STORES, or exit.

    `on` is stored by who records (`session_marker.on_state`). `daemon` is not a
    position of the switch (Richard 2026-09-29): refused with where it is set,
    exit 2, nothing written."""
    from probe.cli.commands.daemon.daemon import calling_agent

    wanted = session_marker.normalize_state(value)
    if wanted is None:
        print(_expected_state(value, extra=(session_marker.INLINE_WORD,)), file=sys.stderr)
        raise typer.Exit(1)
    target = session_marker.switch_target(session_id, wanted, calling_agent())
    if target is None:
        print(session_marker.DAEMON_SWITCH_REFUSAL, file=sys.stderr)
        raise typer.Exit(2)
    return target


def _expected_state(value: object, *, extra: tuple[str, ...] = ()) -> str:
    """The "you typed something else" line, built from the REAL vocabulary.

    One function, so the words a command offers and the words it accepts cannot
    drift apart -- and so a state added to the switch shows up in every error
    message without anyone remembering to go and find them.
    """
    words = [*session_marker.STATE_WORDS, *extra]
    listed = ", ".join(f"'{word}'" for word in words[:-1])
    return f"expected {listed} or '{words[-1]}', got {value!r}"


def _state_block(session_id: str, state: str, *, heal: bool) -> dict:
    """The JSON every state-moving command prints, plus the daemon it owes.

    ONLY a recording state (`full`, `daemon`) is owed a capture daemon --
    `daemon` needs it twice over, since the companion worker is its child.
    `read-only` and `off` both record nothing, so starting one would leave a
    transcript uploader running for a conversation that asked not to be recorded.
    """
    block = {
        "session_id": session_id,
        "state": _state_word(state),
        "label": _state_display(session_id, state),
    }
    if heal and state in session_marker.RECORDING_STATES:
        block["capture"] = _capture_block(session_id, heal_cwd=os.getcwd())
    if state == session_marker.STATE_DAEMON:
        from probe.cli import wizard as wizard

        block["daemon"] = _daemon_block(session_id, state)
        if not wizard.companion_token_held():
            block["note"] = (
                "the Probe daemon has no key yet, so the agent keeps recording; Enter on "
                f"Who records in the wizard approves one ({session_marker.WIZARD_HINT})"
            )
    return block


def _refuse_switch_from_agent(session_id: "str | None", verb: str) -> None:
    """The researcher's switch, run from inside a coding agent's session the
    Probe daemon records (`<sid>.profile`): the agent moving it, however the call
    was wrapped (`probe exec`, `bash -lc`, a script) -- the guard refuses the bare
    command; this refuses the rest (exit 2, nothing written). The researcher
    moves it with `/probe`, pi's command (spawned without the agent's session
    variable) or a terminal outside the agent."""
    own = agent_session.session_id_from_env()
    if not own:
        return
    for sid in {own, session_id or own}:
        if session_marker.session_profile(sid) == session_marker.RECORDER_DAEMON:
            print(session_marker.RESEARCHER_SWITCH_DENY.format(matched=f"probe session {verb}"), file=sys.stderr)
            raise typer.Exit(2)


#: `probe session state inline` from inside a coding agent's shell.
INLINE_FROM_AGENT = (
    "`probe session state inline` was refused: it runs inside a coding agent's session, and only "
    "the researcher hands Probe to the agent (typing `/probe inline`, or this command from a "
    "terminal outside the agent). Nothing changed."
)


@session_app.command("state")
def session_state_cmd(
    value: str = typer.Argument(
        None, help="on | read | off | inline \u2014 omit to show the current state"
    ),
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
) -> None:
    """Show or set Probe's state for THIS conversation.

    \b
    on      reads and writes. Records the work as it happens.
    read    reads allowed, files nothing new in Probe (the transcript is
            still captured). Cleanup still works.
    off     no Probe calls, no session-start injections, and the
            transcript is not captured (a capture process still
            running an older tap uploads it until it ends).

    Where the Probe daemon records (`probe wizard` › Defaults › Who
    records), the same three read `on (daemon)` -- stored as `daemon` --,
    `read only (daemon)` and `off`. The daemon is not a position of this
    switch: `daemon` is refused.

    inline  (the researcher's, where the daemon records) the daemon stops and
            the agent reads and writes Probe itself, as `on (inline)`, until
            the switch moves again. Elsewhere `inline` is `on`.

    Nothing already recorded is deleted by any of them, and moving back to `on`
    does not backfill the interval that was skipped -- it happened unrecorded,
    and inventing it afterwards would be a worse lie than the gap.

    The words are `on`/`read`/`off`; what lands in the config and the session
    marker is the longer `full`/`read-only`/`off`, because those files are read
    by every other copy of the client on the machine and an older one does not
    know a word this version invented (`session_marker.STATE_LABELS`). Both
    spellings are accepted wherever a state is typed.
    """
    resolved = _resolve_agent_session(session)
    if value is None:
        current = session_marker.session_state(resolved)
        if current is None:
            current, _source = session_marker.resolve_state_default(None)
        _print_json(
            {
                "session_id": resolved,
                "state": _state_word(current),
                "label": _state_display(resolved, current),
            }
        )
        return
    if value.strip().lower() == session_marker.INLINE_WORD:
        # The researcher's `/probe inline`, from a terminal or pi's command (which
        # spawns this without the agent's session variable). Inside a coding
        # agent's shell it is the agent asking for itself, however the call was
        # wrapped (`probe exec`, `bash -lc`, a script): refused before anything moves.
        if agent_session.session_id_from_env():
            print(INLINE_FROM_AGENT, file=sys.stderr)
            raise typer.Exit(2)
        wanted = session_marker.STATE_FULL
        if not session_marker.switch_to_inline(resolved) or (
            session_marker.session_profile(resolved) == session_marker.RECORDER_DAEMON
            and not session_marker.is_inline(resolved)
        ):
            print("the switch could not be written: Probe is not inline", file=sys.stderr)
            raise typer.Exit(1)
    else:
        _refuse_switch_from_agent(resolved, "state")
        wanted = _switch_word(resolved, value)
        session_marker.set_session_state(resolved, wanted)
    _require_state(resolved, wanted)
    _capture_switched(resolved, wanted)
    _print_json(_state_block(resolved, wanted, heal=True))


def _capture_switched(session_id: str, state: str) -> None:
    """The switch moved: Probe off means the session is NOT captured, so the
    Probe service that records it looks at the switch now, before the agent
    writes its next line (`service_calls.capture_switched`)."""
    from probe.cli.lifecycle import service_calls

    service_calls.capture_switched(session_id, off=state == session_marker.STATE_OFF)


@session_app.command("untrack")
def session_untrack(
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
) -> None:
    """Turn recording off for THIS conversation. An alias for `state read`.

    THIS IS NOT THE HARD `off`, and the difference is deliberate. What this
    command has always done -- and always documented -- is "records nothing
    further"; it never gated reads. That is `read-only` exactly, so it keeps
    meaning what it meant for everybody with the phrase in muscle memory or in a
    resumed transcript. The state that also stops reads is reached by naming it:
    `probe session state off`.

    Nothing already recorded is deleted -- the work that landed before this stays
    where it is, because it happened.
    """
    resolved = _resolve_agent_session(session)
    _refuse_switch_from_agent(resolved, "untrack")
    ok = session_marker.set_tracking(resolved, False)
    _capture_switched(resolved, session_marker.session_state(resolved) or session_marker.STATE_READ_ONLY)
    # No `_capture_block` here, unlike `track` and `toggle`: the guard those
    # two carry ("heal only if the signal now reads on") is unreachable by
    # construction once `_require_tracking_state(resolved, False)` has proven
    # the signal is off, and a branch that can never run is not a safeguard.
    _require_tracking_state(resolved, False)
    _print_json(
        {
            "session_id": resolved,
            "tracking": "off" if ok else "unchanged",
            "state": _state_word(session_marker.session_state(resolved)),
            "note": (
                "already-recorded work is untouched; `probe session track` turns it "
                "back on. Reads still work -- `probe session state off` stops those too"
            ),
        }
    )


@session_app.command("track")
def session_track(
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
) -> None:
    """Turn tracking ON for this conversation.

    Explicit, so the status line says `tracking` immediately rather than waiting
    for the first project to land -- which is the point when an agent decides a
    session IS research before it has created anything.
    """
    resolved = _resolve_agent_session(session)
    _refuse_switch_from_agent(resolved, "track")
    # `on` is stored by who records: `daemon` where the daemon records (the lean
    # plugin gives the agent nothing to record with, so `full` would record nothing).
    from probe.cli.commands.daemon.daemon import calling_agent

    if session_marker.on_state(resolved, calling_agent()) == session_marker.STATE_DAEMON:
        ok = session_marker.set_session_state(resolved, session_marker.STATE_DAEMON)
    else:
        ok = session_marker.set_tracking(resolved, True)
    _require_tracking_state(resolved, True)
    _capture_switched(resolved, session_marker.session_state(resolved) or session_marker.STATE_FULL)
    # Tracking just went on, so a daemon is owed. Read back rather than
    # trusting `ok`: `_require_tracking_state` has already proven the signal
    # on disk, and that is the value every other surface will render.
    if session_marker.is_tracking(session_marker.tracking_signal(resolved)):
        _capture_block(resolved, heal_cwd=os.getcwd())
    _print_json(
        {
            "session_id": resolved,
            "tracking": "on" if ok else "unchanged",
            "state": _state_word(session_marker.session_state(resolved)),
        }
    )


@session_app.command("toggle")
def session_toggle(
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
) -> None:
    """Toggle this conversation between `on` and `read`.

    \b
        on <---> read        off ---> read

    `off` IS NOT ON THE CYCLE. The bare switch is pressed without reading
    anything, and `off` stops Probe calls entirely -- an agent under it cannot
    find prior work AND cannot know what it missed, so every later answer is
    quietly poorer with nothing to show it. Arriving there by one press too many
    is a cost nobody consented to and nobody can see. `probe session state off`,
    or `/probe off`, is the only way in.

    A press while `off` leaves for `read`: pressing a switch you turned off is
    asking for something to change, and `read` is the smallest change that gives
    back what `off` took away. Getting back to `off` means typing it again.

    "Current" resolves exactly as `status` reports it -- the explicit per-session
    decision when one exists, else this cwd's effective default posture -- so
    advancing never disagrees with what the status line was showing. This is the
    same write the switch's activation hook makes on a bare invocation the
    researcher TYPED, exposed for shells and for reconciling a machine where that
    hook is absent.
    """
    resolved = _resolve_agent_session(session)
    _refuse_switch_from_agent(resolved, "toggle")
    current = session_marker.session_state(resolved)
    if current is None:
        current, _source = session_marker.resolve_state_default(None)
    from probe.cli.commands.daemon.daemon import calling_agent

    target = session_marker.next_state(current)
    target = session_marker.switch_target(resolved, target, calling_agent()) or target
    session_marker.set_session_state(resolved, target)
    _require_state(resolved, target)
    _capture_switched(resolved, target)
    block = _state_block(resolved, target, heal=True)
    block["was"] = _state_word(current)
    _print_json(block)


@session_app.command("default")
def session_default(
    value: str = typer.Argument(
        None,
        help="on | read | off | inherit — omit to show; inherit requires --folder",
    ),
    folder: Path | None = typer.Option(
        None,
        "--folder",
        help="existing directory whose exact tracking override to show or set",
    ),
) -> None:
    """Show or set a new session's tracking default (the machine's).

    `--folder` is retired: folder defaults (`<folder>/.probe/config.json`) gave
    way to `.probe.config`, a gitignore-style list of paths Probe never records
    (`probe ignore check PATH`). It now exits 1 saying so.

    Stored TOP-LEVEL in the probe config, never inside a context: `probe logout`
    replaces a context wholesale, so a preference kept there would be wiped and
    tracking would silently come back on. Top level also keeps the default from
    following whichever tenant is selected, which is not what "all my sessions"
    means.

    A per-session `probe session track|untrack` always wins over this.

    `daemon` is refused: whether the Probe daemon records is `probe wizard
    ` › Defaults › Who records, and a new session's `on` follows it.
    """
    if folder is not None:
        print(session_marker.probe_config().FOLDER_DEFAULT_RETIRED, file=sys.stderr)
        raise typer.Exit(1)
    if value is not None:
        _refuse_switch_from_agent(None, "default")
    if folder is None and value is None:
        shown = {
            "machine_default": _state_word(session_marker.default_session_state()),
            "config": str(session_marker.config_path()),
            "note": "per-session `probe session state` overrides this",
        }
        set_by = session_marker.set_by_note()
        if set_by:
            shown["set_by"] = set_by
        _print_json(shown)
        return

    if folder is None:
        wanted = session_marker.normalize_state(value)
        if wanted is None:
            print(_expected_state(value), file=sys.stderr)
            raise typer.Exit(1)
        if wanted == session_marker.STATE_DAEMON:
            print(session_marker.DAEMON_SWITCH_REFUSAL, file=sys.stderr)
            raise typer.Exit(2)

        from ....sdk.settings.settings import ConfigUnreadable

        try:
            # Shared with the wizard's Settings screen. It raises rather than
            # writing through a failed read, so a broken config file is reported
            # here, never replaced by just this preference.
            path = session_marker.write_default_state(wanted)
        except (OSError, ValueError, ConfigUnreadable) as exc:
            print(f"could not update {session_marker.config_path()}: {exc}", file=sys.stderr)
            raise typer.Exit(1) from exc
        _print_json({"machine_default": _state_word(wanted), "config": str(path)})
        return

    print(session_marker.probe_config().FOLDER_DEFAULT_RETIRED, file=sys.stderr)
    raise typer.Exit(1)
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
