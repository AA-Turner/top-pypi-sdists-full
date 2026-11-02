"""probe session initialize: seed a host session from its start cwd and the agent calling it."""

from __future__ import annotations
import os
import sys

import typer
from ....sdk import session_marker
from probe.cli.commands.session.session import (
    _capture_block,
    _effective,
    _resolve_agent_session,
    _state_word,
    session_app,
)


@session_app.command("initialize", hidden=True)
def session_initialize(
    session: str = typer.Option(None, "--session", help="session id"),
    cwd: str = typer.Option(..., "--cwd", help="the host session's initial working directory"),
) -> None:
    """Seed a host session from its initial cwd and return its durable state.

    This is a host-facing bridge for agents whose extension cannot import the
    Python resolver directly. It is deliberately hidden from CLI help: people
    set defaults with `session default` and move a live switch with
    `track|untrack|toggle`.
    """
    resolved = _resolve_agent_session(session)
    # Where the session started, once (a resume keeps the first): what decides
    # which `.probe.config` files are ABOVE it (`probe session parent`).
    session_marker.record_launch_dir(resolved, cwd)
    agent = _initializing_agent()
    # WHICH PROFILE THIS SESSION RUNS: what the machine's "Who records" says for
    # this agent NOW, written on EVERY start, resume and reload. pi reads its
    # package's skill filter (the profile's install) when it starts, so the
    # session's profile must follow the same moment, not the session's first
    # start. Claude Code and Codex never call this command; their lean plugin
    # writes the mark itself.
    if agent is not None:
        session_marker.mark_session_profile(resolved, session_marker.recorder(agent))
    state = session_marker.session_state(resolved)
    signal = session_marker.tracking_signal(resolved)
    is_seeded = False
    source = "session"
    if (
        state in (session_marker.STATE_FULL, session_marker.STATE_DAEMON)
        and agent is not None
        and not session_marker.is_inline(resolved, state)
    ):
        # An `on` session follows its profile: a session resumed after the
        # researcher switched Who records records the way pi now loads it.
        # `read-only` and `off` are the researcher's own switch and stay, and so
        # does a session they set inline (`/probe inline`): a reload must not
        # hand Probe back to the daemon behind their back.
        target = session_marker.on_state(resolved, agent)
        if target != state and session_marker.set_session_state(resolved, target, explicit=False):
            state = session_marker.session_state(resolved)
            signal = session_marker.tracking_signal(resolved)
    if state is None:
        default, source = session_marker.resolve_state_default(cwd)
        # The same rule as the session-start hook: `on` (or a `daemon` default
        # from before) is stored by who records.
        default = session_marker.seed_state(resolved, default, agent)
        is_seeded = session_marker.set_session_state_if_absent(
            resolved, default, source=session_marker.seed_source(source)
        )
        state = session_marker.session_state(resolved)
        signal = session_marker.tracking_signal(resolved)
        if signal is None:
            print(
                f"could not initialize tracking for session {resolved}",
                file=sys.stderr,
            )
            raise typer.Exit(1)
        if not is_seeded:
            # Another writer won the atomic publish. Its signal is the answer;
            # the folder value this process resolved is no longer provenance.
            source = "session"

    # heal_cwd=None: this command REPORTS capture and never starts it. The pi
    # extension calls it immediately before its own spawn, so healing here
    # would take that spawn from the extension on every healthy session.
    capture = _capture_block(resolved, heal_cwd=None)
    _print_json(
        {
            "session_id": resolved,
            # `tracking` AND `signal` KEEP THEIR TWO-VALUED MEANING FOREVER.
            # pi's trackingState.ts declares `signal: "on" | "off"` and ships on
            # its own release train, so a machine routinely runs a new CLI
            # against an old extension. Both non-recording states project to
            # `off`, which is TRUE of both and is the strongest thing a
            # two-valued reader can be told. The third value arrives as a NEW
            # field that an old reader simply ignores.
            "tracking": session_marker.is_tracking(signal),
            "signal": signal,
            "state": _state_word(state),
            "seeded": is_seeded,
            "source": source,
            "capture": capture,
            "effective": _effective(session_marker.is_tracking(signal), capture),
            # NEW, additive (an old extension ignores it): "daemon" when the
            # Probe daemon records and reads for this session, else "agent".
            "profile": session_marker.session_profile(resolved) or session_marker.RECORDER_AGENT,
            # `.probe.config` (additive): `context`, the paths Probe records
            # nothing about, for the prompt on every turn; `ask`, the question
            # about files above the launch folder, ONCE (marked asked here, so
            # the extension delivers it with the next turn).
            "probe_config": _probe_config_start(resolved, cwd, state),
        }
    )


def _probe_config_start(session_id: str, cwd: str, state: "str | None") -> dict:
    if not session_marker.state_allows_writes(state):
        return {"context": None, "ask": None}
    return {
        "context": session_marker.excluded_context(session_id, cwd),
        "ask": session_marker.take_parent_ask(session_id),
    }


def _initializing_agent() -> "str | None":
    """The coding agent calling `session initialize`: its session markers when
    this shell has them, else `PROBE_AGENT` when it names a harness. The pi
    extension runs this command with an allowlisted environment that carries
    `PROBE_AGENT=pi` and no PI_* variable (pi sets those only on its bash
    tool's children), so without the second rung every pi session seeded as
    if no agent had called."""
    from probe.cli.commands.daemon.daemon import calling_agent
    from probe.foundation.harness_registry import get_registry

    detected = calling_agent()
    if detected is not None:
        return detected
    harness = get_registry().find(os.environ.get("PROBE_AGENT"))
    return harness.id if harness is not None and harness.installable else None
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
