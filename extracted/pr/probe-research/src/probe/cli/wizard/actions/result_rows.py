"""the --json result row each action reports (configure, install, recorder, update, removal, device sign-in) and the run summary they feed."""

from __future__ import annotations

import contextlib
from ....sdk.settings.settings import load_context
from ....sdk import session_marker


def _record_install(
    source: str, *, ok: bool, summary: str = "", notes=(), restart: bool = False, must=()
) -> bool:
    """This agent's install, in the run's summary if there is one (`_run_summary`)."""
    from probe.cli import wizard as wizard

    run_summary = wizard.current_run_summary()
    if run_summary is None:
        return False
    run_summary.record(source, ok=ok, summary=summary, notes=notes, restart=restart, must=must)
    return True


def _run_summary(action, sources):
    """The final screen's `setup.RunSummary` for an install or an Update the
    wizard draws (a terminal); for anything else, and for a run whose output
    is read by a program, nothing: those keep the full per-agent report."""
    from probe.cli.wizard.actions import onboarding as actions_mod
    from probe.cli import wizard as wizard

    kind = {
        actions_mod.Action.CONFIGURE: wizard.SummaryAction.INSTALL,
        actions_mod.Action.UPDATE: wizard.SummaryAction.UPDATE,
        actions_mod.Action.UNINSTALL: wizard.SummaryAction.UNINSTALL,
    }.get(action)
    if not wizard.interactive() or kind is None:
        return contextlib.nullcontext()
    return wizard.run_summary(kind, sources)


def _capability_fields(values) -> dict[str, bool]:
    """A selection (`setup.Selection`) or a `Capabilities.enabled()` map as
    `--json` names it: {tracking, capture, auto_update, agent_rules}."""
    from probe.cli.wizard.state.state import Capability

    if isinstance(values, dict):
        return {str(capability): bool(values.get(capability)) for capability in Capability}
    return {str(capability): bool(getattr(values, capability.value)) for capability in Capability}


def _record_configure(source: str, selection, after, *, ok: bool, message: str = "") -> None:
    """`--json`'s result row for one agent's configure: what the run asked for,
    what the agent reads as on now, and whether the run verified it. Automatic
    updates and the instruction rules are plain files on this machine, so a
    mismatch there fails the row whatever the step said. So does tracking or
    capture still on after the run was asked to turn it off: the run's verdict
    checks only what it installed."""
    from probe.core import events as json_events
    from probe.cli.wizard.state.state import Capability

    if not json_events.enabled():
        return
    requested = _capability_fields(selection)
    for capability in requested:
        if selection.keeps(capability):
            requested[capability] = None  # kept as found, not asked for (`preserve`)
    actual = _capability_fields(after.enabled())
    unmet = [c for c in (Capability.AUTO_UPDATE, Capability.AGENT_RULES) if actual[c] != requested[c]]
    unmet += [c for c in (Capability.TRACKING, Capability.CAPTURE) if requested[c] is False and actual[c] is True]
    if unmet and not message:
        message = f"not as asked: {', '.join(unmet)}"
    json_events.agent_result(source, requested=requested, actual=actual, ok=ok and not unmet, message=message)


def _record_recorder(chosen: str | None, caps_by_source: dict, lines: list[str] | None) -> None:
    """`--json`'s result rows for a Who records switch: what each agent's own
    config says now, never which steps ran. A refusal or a missing key or
    libraries leaves an agent on the other recorder, so its row is not ok, with
    the switch's own words as the reason. An agent with no daemon profile is not
    part of the switch (the lines say it keeps recording itself), so it has no
    row: its row could never be ok, and the run would never read complete."""
    from probe.core import events as json_events
    from probe.cli import wizard as wizard

    if chosen is None or not json_events.enabled():
        return
    detail = "\n".join(lines or [])
    agents = [source for source in caps_by_source if source in wizard.RECORDER_SOURCES]
    if not agents:
        actual = wizard.machine_recorder()
        json_events.agent_result(
            None, requested={"recorder": chosen}, actual={"recorder": actual},
            ok=actual == chosen, message="" if actual == chosen else detail,
        )
    for source in agents:
        actual = session_marker.recorder(source)
        json_events.agent_result(
            source, requested={"recorder": chosen}, actual={"recorder": actual},
            ok=actual == chosen, message="" if actual == chosen else detail,
        )


def _record_update(source: str, outcome) -> None:
    """`--json`'s result row for one agent's update (`upgrading.UpdateOutcome`)."""
    from probe.core import events as json_events

    if not json_events.enabled():
        return
    json_events.agent_result(
        source,
        requested={"updated": True},
        actual={"updated": bool(outcome.ok), "restart_needed": bool(outcome.restart_needed)},
        ok=bool(outcome.ok),
        message="" if outcome.ok else "\n".join(outcome.lines) or "the update did not finish",
    )


def _record_removal(source: str, after, lines: list[str]) -> None:
    """`--json`'s result row for one agent's uninstall: what is still there."""
    from probe.core import events as json_events

    if not json_events.enabled():
        return
    actual = {
        "tracking": bool(after.tracking_plugin_installed),
        "capture": bool(after.capture_plugin_installed or after.capture_on),
        "agent_rules": bool(after.agent_rules_installed),
    }
    json_events.agent_result(
        source,
        requested={key: False for key in actual},
        actual=actual,
        ok=not any(actual.values()),
        message="\n".join(line for line in lines if line.startswith("!")),
    )


def _record_device_sign_in(*, wanted: bool, ok: bool | None = None, message: str = "") -> None:
    """`--json`'s result row for the device's own credentials (agent null):
    whether a token is saved here now."""
    from probe.core import events as json_events

    if not json_events.enabled():
        return
    try:
        signed_in = bool((load_context() or {}).get("token"))
    except Exception:  # noqa: BLE001 - an unreadable config holds no credential
        signed_in = False
    json_events.agent_result(
        None,
        requested={"signed_in": wanted},
        actual={"signed_in": signed_in},
        ok=(signed_in == wanted) if ok is None else ok,
        message=message,
    )
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
