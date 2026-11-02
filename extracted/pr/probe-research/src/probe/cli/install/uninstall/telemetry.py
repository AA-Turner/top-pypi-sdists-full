"""the uninstall's analytics events: started, declined, done, and who the removal is of."""

from __future__ import annotations

import contextlib
import time


# -- telemetry -----------------------------------------------------------------------------------


def _telemetry_start(run: Run) -> None:
    """`wizard.uninstall_started`, BEFORE the confirmation and before anything
    is torn down: what is being removed is unreadable after it."""
    try:
        from probe import analytics as telemetry_mod
        from probe.cli.install.uninstall import plan as uninstall_plan
        from probe.cli.wizard.state.state import TAP_PLUGIN_NAME
        from probe.sdk.settings.settings import resolve

        run.telemetry = telemetry_mod.TelemetryContext.start(
            via=telemetry_mod.Via.WIZARD, interactive=run.options.interactive, base_url=resolve().base_url)
        traces = list(_all_traces().values())
        plugins = [p for found in traces for p in found.get("plugins", [])]
        run.telemetry.emit(
            telemetry_mod.EVENT_WIZARD_UNINSTALL_STARTED,
            agent_count=len(run.agents),
            tracking_installed=any(TAP_PLUGIN_NAME not in p for p in plugins),
            capture_installed=any(TAP_PLUGIN_NAME in p for p in plugins) or any("capture" in f for f in traces),
            agent_rules_installed=any("rules" in found for found in traces),
            was_signed_in=any(ctx.get("token") for ctx in uninstall_plan.contexts().values()),
            confirmed_via="prompt" if run.options.interactive else "flag",
        )
    except Exception:  # noqa: BLE001 - observability never stops the uninstall
        run.telemetry = None


def _all_traces() -> dict:
    from probe.cli.install.uninstall import agent_traces as uninstall_agents

    return uninstall_agents.all_traces()


def _telemetry_pin(run: Run) -> None:
    """The person this removal is of, resolved while the credential that
    names them still exists (the server phase revokes it)."""
    with contextlib.suppress(Exception):
        if run.telemetry is not None:
            run.telemetry.pin_identity()


def _telemetry_declined(run: Run) -> None:
    with contextlib.suppress(Exception):
        if run.telemetry is not None:
            from probe import analytics as telemetry_mod

            run.telemetry.emit(telemetry_mod.EVENT_WIZARD_UNINSTALL_COMPLETED,
                               outcome=telemetry_mod.UninstallOutcome.DECLINED, agent_count=len(run.agents),
                               duration_seconds=round(time.monotonic() - run.started_at, 3))


def _telemetry_done(run: Run) -> None:
    if run.telemetry is None:
        return
    try:
        from probe import analytics as shared
        from probe import analytics as telemetry_mod

        run.telemetry.emit(telemetry_mod.EVENT_WIZARD_UNINSTALL_COMPLETED,
                           outcome=telemetry_mod.UninstallOutcome.REMOVED, agent_count=len(run.agents),
                           warnings=run.warnings, duration_seconds=round(time.monotonic() - run.started_at, 3))
        shared._ensure_sender().request_flush(2.0)  # noqa: SLF001 - before its files go
    except Exception:  # noqa: BLE001
        pass
from probe.cli.install.uninstall.state import Run  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.uninstall import run  # noqa: E402 -- pieces need each other; the front door loads this one first
