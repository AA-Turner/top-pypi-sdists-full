"""stopping: ask the service to finish what it records."""

from __future__ import annotations

import contextlib


# -- stopping (U-T3 first step, U-T4) --------------------------------------------------------


def _phase_stopping(run: Run) -> list[str]:
    from probe.cli.install.uninstall import processes as uninstall_procs
    from probe.core import events
    from probe.service import keeper
    from probe.service.updater import lifeboat

    lines = run.out
    # FIRST: a deployed (v2) lifeboat or the keeper's timer must not fire in
    # the middle of this (they do not know the barrier). No `keeper-off` left.
    keeper.remove(mark_off=False)
    lifeboat.remove()
    lines.append("Removed the keeper and the lifeboat.")
    # Nothing that lasts before the point of no return: the barrier alone keeps
    # taps and starters quiet until then (the killswitches are the
    # integrations phase's, the import jobs the state phase's).
    _finish_recorders(lines)
    survivors = uninstall_procs.stop_everything(run.plan, force=run.options.force, lines=lines,
                                                stopped=run.stopped)
    _step(events.Step.UNINSTALL_STOP, events.Status.FAILED if survivors else events.Status.DONE,
          f"{len(survivors)} Probe process(es) still running" if survivors else "every Probe process stopped")
    return lines


def _finish_recorders(lines: list[str]) -> None:
    """Ask the service to finish what it records (its last pass ships the
    transcripts it holds) before it is stopped."""
    from probe.foundation.harness_registry import get_registry
    from probe.foundation import service_api as client

    if client.connect(0.5) is None:
        return
    from probe.cli.lifecycle import service_calls

    for harness in get_registry().captured():
        with contextlib.suppress(Exception):
            service_calls.finish_recorders(harness.id)
from probe.cli.install.uninstall.state import Run, _step  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.uninstall import run  # noqa: E402 -- pieces need each other; the front door loads this one first
