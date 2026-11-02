"""the package harness's step inside an Update (pi today): bounded by its own deadline, and retried alone when owed."""

from __future__ import annotations
import contextlib
import time

from probe import __version__
# `update_report` is imported HERE, at the top, for the same reason updater.py
# imports its whole call graph eagerly (H8): it runs after `uv tool upgrade` has
# replaced the installed tree, when a first import would read the new files.
from probe.shared.updates import autoupdate
from probe.shared.updates import update_report
from probe.foundation.harness_registry import get_registry


def package_harness() -> str | None:
    """The coding agent whose Probe plugin is a package (pi), not a
    marketplace plugin: its update is `_update_pi_package`'s."""
    return _package_harness()


def _package_harness() -> str | None:
    """The extension-family harness whose package `_update_pi_package` moves
    (pi's), from the registry rather than by name."""
    from probe.foundation.harness_registry import FAMILY_EXTENSION, get_registry

    return next(
        (h.id for h in get_registry().installable() if h.family == FAMILY_EXTENSION), None
    )


def _bounded_pi_update() -> _PiUpdate:
    """`_update_pi_package` in an exception boundary and a deadline of its own
    (`component_deadline`, plan A3): one that raises or hangs is pi's failed
    step (owed, so pi's next start tries again), never the run's."""
    label = _agent_label(_package_harness())
    what = f"{label}'s package update" if label else "the package update"
    started: list[_Component] = []
    with _stopped_with_the_update(started):
        started.append(_start(UpdatePart.PI_PACKAGE, _update_pi_package))
        found = _outcome_by(started[0], time.monotonic() + component_deadline(), what)
    if isinstance(found, _PiUpdate):
        return found
    detail = _stopped_detail(what, found)
    with contextlib.suppress(Exception):
        autoupdate.mark_pi_update_pending(True)
    return _PiUpdate(
        ["pi package:", f"  ! not updated ({detail})"],
        ok=False,
        detail=f"pi package not updated: {detail}",
        ran=True,
        code=update_report.PiStep.FAILED,
    )


def update_owed_pi_package() -> None:
    """Run ONLY the pi step, for a pi package update that failed
    (`autoupdate.PI_UPDATE_PENDING_FILENAME`) while the CLI itself is current.
    The caller holds the update lock. Records the attempt only when `pi update`
    ran: a skip is not news, and overwriting `last_attempt` with it would hide
    the real one."""
    step = _bounded_pi_update()
    if not step.ran:
        return
    attempted_at = int(time.time())
    autoupdate.record_attempt(
        autoupdate.Attempt(
            at=attempted_at,
            ok=True,
            from_version=__version__,
            plugin_ok=step.ok,
            plugin_detail=step.detail or f"pi package {step.lines[-1].strip()}",
        )
    )
    # Only pi's step ran: no CLI or tap half to report. pi's session start or a
    # run's end asked for it; the spawner's TRIGGER_ENV says which.
    _report_attempt(
        lambda: update_report.attempt_report(
            trigger=update_report.trigger_from_env(update_report.Trigger.SESSION_START),
            ok=step.ok,
            at=attempted_at,
            source=_package_harness(),
            cli=None,
            plugin=update_report.pi_component(step, target=None),
            tap=None,
        )
    )
from probe.cli.install.upgrade.components import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _Component,
    _outcome_by,
    _start,
    _stopped_detail,
    _stopped_with_the_update,
    component_deadline,
)
from probe.cli.install.upgrade.finish import _agent_label, _report_attempt  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.upgrade import UpdatePart  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.pi.package_upgrade import _PiUpdate, _update_pi_package  # noqa: E402 -- pieces need each other; the front door loads this one first
