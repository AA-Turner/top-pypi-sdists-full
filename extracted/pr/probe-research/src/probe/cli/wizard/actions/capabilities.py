"""change only the wanted capabilities per agent through CONFIGURE, and Update's one question when a sign-in left capture pending."""

from __future__ import annotations
import os

import typer


#: Set once Update's capture question has been shown. The hand-off execs the
#: newest release with this process's environment (`handoff._child_env`), and
#: that release must not ask again: a "Not now" stands for the whole Update.
CAPTURE_QUESTION_ASKED_ENV = "PROBE_CAPTURE_QUESTION_ASKED"


def _confirm_pending_capture(caps_by_source: dict, *, base_now: str, telemetry=None):
    """Update's one question when a sign-in left capture behind its pending lock.

    The lock (`capture.AWAITING_CONFIRMATION`) waits for the person to confirm
    capture, and only Install lifted it. On a machine whose plugins were
    already installed people pick Update, so capture stayed off behind a live
    credential while the menu called it "killswitch set" (Anthrogen,
    2026-10-26). Asked only for agents that hold their own credential and have
    the capture plugin: one with no credential needs Install's browser
    approval, which this cannot give, and neither does a credential the
    server refused. "Not now" changes nothing, and the menu keeps saying
    "finish Install". Returns the result lines, or the question's own None
    (Ctrl-C) / `tui.BACK` (Esc) for the caller to act on.
    """
    from probe.cli import wizard as wizard
    from probe.cli.wizard import terminal as tui
    from probe.cli.wizard.state.state import Capability
    from probe.cli.wizard.state.capture_credentials import tap_plugin_dir

    pending = {
        source: snapshot
        for source, snapshot in caps_by_source.items()
        if snapshot.capture_awaiting_confirmation
        and snapshot.capture_token_sources
        and snapshot.capture_credential_valid is not False
        and snapshot.capture_plugin_installed
    }
    if not pending:
        return []
    tui.clear()
    answer = wizard.confirm_pending_capture(tuple(pending))
    if answer is None or answer is tui.BACK:
        return answer  # not answered: the next Update asks again
    os.environ[CAPTURE_QUESTION_ASKED_ENV] = "1"
    if answer is not True:
        return []
    lines = _apply_capability_targets(
        {Capability.CAPTURE: True},
        caps_by_source=pending,
        base_now=base_now,
        telemetry=telemetry,
        retry_hint="pick “Install Probe” to turn capture on",
    )
    # Verified by the lock itself, not by the configure's word for it.
    on = [source for source in pending if not (tap_plugin_dir(source) / ".disabled").exists()]
    still_off = [source for source in pending if source not in on]
    if on:
        lines.append(f"Session capture is on for {wizard.agent_label(on)}.")
    if still_off:
        lines.append(f"! Session capture is still off for {wizard.agent_label(still_off)}.")
    return lines


def _capture_answer(lines: list[str]) -> tuple[list[str], list[str]]:
    """`_confirm_pending_capture`'s result for a page: what is now true
    ("Session capture is on for Codex."), then the errors named for their agent.
    Each agent's configure report behind it stays off, as on Settings' page."""
    said = [line.removeprefix("! ") for line in lines]
    verdict = [line for line in said if line.startswith("Session capture is ")]
    return verdict, _labelled_problems([line for line, plain in zip(lines, said) if plain not in verdict])


def _apply_capability_targets(
    wanted: dict,
    *,
    caps_by_source: dict,
    base_now: str,
    telemetry=None,
    retry_hint: str,
) -> list[str]:
    """Change only the capabilities in `wanted`, per agent, through CONFIGURE.

    Every other capability rides in each agent's target marked `preserve`: its
    boolean is only that agent's read (`capability_state_for`), and a read
    cannot say "leave it". `capture_on` is False for a deliberate off and for a
    sign-in's pending lock alike, and applying that False ran the full
    turn-off -- it revoked a capture credential minted 90 seconds earlier on a
    machine where nobody had turned capture off (Anthrogen, 2026-10-26: the
    Settings commit was automatic updates).
    """
    from probe.cli.wizard.actions import onboarding as actions_mod
    from probe.cli.wizard.apply import client_installation
    from probe.cli.wizard import doctor as doctor_impl
    from probe.cli import wizard as wizard
    from probe.cli.wizard.state.state import Capability
    from probe.cli.wizard.state.agent_identity import agent_target

    untouched = frozenset(Capability) - frozenset(wanted)
    targets: dict[str, object] = {}
    for source, snapshot in caps_by_source.items():
        state = wizard.capability_state_for(snapshot)
        state.update(wanted)
        targets[source] = wizard.Selection(
            tracking=state[Capability.TRACKING],
            capture=state[Capability.CAPTURE],
            auto_update=state[Capability.AUTO_UPDATE],
            agent_rules=state[Capability.AGENT_RULES],
            preserve=untouched,
        )

    lines: list[str] = []
    # One registration for the machine, not one per agent: see
    # `client_installation.merged_registration`.
    with client_installation.merged_registration() as registration_warnings:
        for source in caps_by_source:
            label = wizard.agent_label(source)
            try:
                with agent_target(source):
                    current = doctor_impl.collect()
                    result = _run_wizard_action(
                        actions_mod.Action.CONFIGURE,
                        caps=current,
                        base_now=base_now,
                        yes=True,
                        tracking=None,
                        capture=None,
                        auto_update=None,
                        agent_rules=None,
                        uninstall=False,
                        configured=True,
                        selection_override=targets[source],
                        authorization_needs=[],
                        capture_sources=[],
                        telemetry=telemetry,
                    )
            except typer.Exit:
                # The configure path already streamed WHAT failed on its progress
                # screen; what must not happen is the whole wizard dying with the
                # other agent unapplied.
                lines.extend([f"{label}:", f"! not finished — {retry_hint}.", ""])
                continue
            if result:
                lines.extend([f"{label}:", *result, ""])
    return lines + registration_warnings
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.snapshots.snapshots import snapshot  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.actions import _run_wizard_action  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.settings import _labelled_problems  # noqa: E402 -- pieces need each other; the front door loads this one first
