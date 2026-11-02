"""the updater's timings and limits, each overridable by its environment variable (the one place tests patch)."""

from __future__ import annotations
import contextlib
import os
import sys
import time

from probe.shared.updates import step as update_step
from ...foundation.service_api.vocabularies import DeferReason

CHECK_EVERY_S = 6 * 3600
#: After a cycle that ended not ok (a failed step, or an update child that said
#: `complete: false`: the CLI install left nothing, the plugins moved), the next
#: check comes this soon, doubling with each failure in a row up to
#: CHECK_EVERY_S: a failure retried six hours later left a machine on the old
#: CLI for most of a day (live test C, 2026-10-24).
FAILED_RETRY_S = 3600
#: How long a running cycle may keep an otherwise idle service alive (plan R3),
#: outside its update child's run (which holds it for as long as the child may
#: run: `update_timeout_s` + `update_stop_grace_s`, `_hold_for_child`).
HOLD_S = 10 * 60
#: `update.check_now` within this of a finished cycle answers `recent`: the
#: manifest cache's own TTL, and the bound on a sweep of runs each ending
#: with a check.
CHECK_NOW_COOLDOWN_S = 15 * 60
#: Between raising the barrier and checking again: a `probe` that passed the
#: barrier's stat a moment before it existed has taken its lock by then.
BARRIER_SETTLE_S = 1.0
#: A deferred update is retried this soon after a session ends (its worker lets
#: go of its lock as it exits), within the service's own idle grace ...
SESSION_END_RETRY_S = 2.0
#: ... and again, twice as long after each busy look, up to this: a worker
#: drains its queue for a while after its session ended, holding its lock.
SESSION_END_RETRY_MAX_S = 15 * 60
#: While an update is deferred, the schedule looks again this often (not every
#: minute, which a last check older than CHECK_EVERY_S would otherwise give).
DEFERRED_RETRY_S = 15 * 60
VERSION_TIMEOUT_S = 30.0
STATE_VERSION = 1
#: The update child's stderr; cut back at a cycle's start past this.
MAX_LOG_BYTES = 1024 * 1024
#: How long the running daemon workers get to hand over before an update (D7):
#: each finishes the model round it is in. Past it, the update is deferred.
WORKER_STOP_S = 10 * 60
#: While waiting, a stopping worker's `.handover` marker is touched this often
#: (the worker trusts only one younger than 10 s: `worker.HANDOVER_FRESH_S`).
HANDOVER_TOUCH_S = 2.0
WORKER_POLL_S = 0.25
#: Deferred this long without a break by workers, a run or an action, or a
#: setup holding wizard.lock this long: the next cycle updates anyway (D7, D33, C1).
DEFER_LIMIT_S = 24 * 3600
#: Told to the update child when DEFER_LIMIT_S ran out: the reasons it updates
#: past that the child would otherwise defer on again by itself, comma
#: separated (`CHILD_FORCED`): a live run (D33), a setup holding wizard.lock
#: (C1). The child then goes on as this cycle decided
#: (`probe.cli.install.upgrade.turn.forced_past`).
FORCED_ENV = update_step.FORCED_ENV
#: Told to the update child when the CLI is current and daemon workers run
#: from its env: plugins only (`probe.cli.install.upgrade.turn.SKIP_CLI_ENV`, D7).
SKIP_CLI_ENV = update_step.SKIP_CLI_ENV
#: Told to the update child when it must update the CLI beside the running
#: version or not at all (`probe.cli.install.updater.cli_install.REQUIRE_SIDE_BY_SIDE_ENV`): the
#: service did not wait for runs and workers, because nothing they run from is
#: replaced (D6, D33).
SIDE_BY_SIDE_ENV = update_step.SIDE_BY_SIDE_ENV
#: The update child's wall time, at most. Past it the child is stopped (SIGTERM
#: to its process group, SIGKILL after UPDATE_STOP_GRACE_S) and the step is
#: failed, so the next cycle can run: a child that never returned used to keep
#: the cycle in progress for good, every `update.check_now` answering
#: `running`, and the next service deferring on its `wizard.lock` (then never
#: overridden) for good. What a normal update takes: 11-28 s for each of the 19
#: cycles in one devbox's service.log (2026-10-22/23); 24 s from start to report
#: for the last update of a machine that then ran none for 29 h. The longest
#: step the child bounds itself is the CLI env's install, 300 s
#: (`probe.cli.install.updater.cli_install._UPGRADE_TIMEOUT_S`, `bootstrap._INSTALL_TIMEOUT_S`), and
#: this code already reads an update older than 15 min as a crashed one (the
#: barrier's MAX_AGE_S; the hold of R3 is 10 min). Twice that, six times the
#: longest step and sixty times the slowest update seen: a child still running
#: then is stuck outside its own bounds, not slow.
UPDATE_TIMEOUT_S = 30 * 60
#: SIGTERM to SIGKILL. The child's SIGTERM handler (`probe.core.events`) ends
#: the run through its `finally` blocks: its locks let go, its records and its
#: update report written (the send is bounded at 3 s,
#: `probe.shared.updates.update_report.SEND_TIMEOUT_S`), the command it was running killed.
UPDATE_STOP_GRACE_S = 30.0
#: Test-only overrides of the two (API v1, "Lifecycle"). Nothing in production sets them.
WORKER_STOP_ENV = "PROBE_SERVICE_WORKER_STOP_S"
DEFER_LIMIT_ENV = "PROBE_SERVICE_DEFER_LIMIT_S"
#: And of APP_RESULT_TIMEOUT_S (a delegated app check that never reports).
APP_RESULT_TIMEOUT_ENV = "PROBE_SERVICE_APP_RESULT_TIMEOUT_S"
#: And of UPDATE_TIMEOUT_S and UPDATE_STOP_GRACE_S.
UPDATE_TIMEOUT_ENV = "PROBE_SERVICE_UPDATE_TIMEOUT_S"
UPDATE_STOP_GRACE_ENV = "PROBE_SERVICE_UPDATE_STOP_GRACE_S"
UPDATE_LOG_NAME = "update.log"
#: A follow-up a service left for the next one (`Updater.mark_followup`) is
#: done when that one starts within this long; older, the next session's own
#: start does it.
FOLLOWUP_MAX_AGE_S = 24 * 3600
#: A cycle's CLI-and-plugins step whose child exited 0 but did not finish
#: every step (`complete: false`; its update.log says which).
INCOMPLETE_DETAIL = "the update did not finish every step (see update.log)"
#: `probe.shared.updates.update_report.TRIGGER_ENV`: what asked, for the server's report.
TRIGGER_ENV = update_step.TRIGGER_ENV
#: `probe.cli.wizard.session.lock.LOCK_FILENAME`, under the default state dir.
WIZARD_LOCK_NAME = update_step.WIZARD_LOCK_NAME
#: `probe.cli.wizard.session.lock.BUSY_EXIT_CODE`: the update child found a setup running.
WIZARD_BUSY_EXIT = update_step.WIZARD_BUSY_EXIT

#: The deferrals DEFER_LIMIT_S ends. A setup is one since C1 (owner,
#: 2026-10-26: nothing a person leaves open blocks updates for more than a day):
#: wizard.lock held, or a `probe wizard` menu waiting on a person
#: (`setup_marks.MENU_PREFIX`), which counts only for an update that moves the
#: files that menu runs from (in place, or the first switch): a side-by-side
#: switch goes on beside it. Its time is how long the lock has been held, or
#: the menu has waited, from its record (`setup_marks.holder`), else (a holder
#: from before the record) how long this service has deferred on it. Past it
#: the update goes on and never stops the setup: the child is told
#: (FORCED_ENV) and runs without the lock. (An update child a service before
#: this one started, still running past UPDATE_TIMEOUT_S, is stopped first:
#: `overrun_update`. That is the one holder of the lock ever ended, and only
#: once it is proven to be that child.)
LIMITED = frozenset({
    DeferReason.DAEMON_RECORDING, DeferReason.RUN_IN_FLIGHT, DeferReason.ACTION_RUNNING,
    DeferReason.SETUP_RUNNING,
})
#: The LIMITED reasons the update child checks again by itself, so is told it
#: was forced past (FORCED_ENV): its run check, and its own wizard.lock.
CHILD_FORCED = (DeferReason.RUN_IN_FLIGHT, DeferReason.SETUP_RUNNING)

#: The app step's record when the service installed a closed app's update
#: itself (`Updater._install_closed`), not the app's own updater.
VIA_SERVICE_INSTALL = "service_install"


def _installs_closed_app() -> bool:
    """Does the service install a closed desktop app's update here (plan E1)?
    macOS only: Linux and Windows have no desktop app."""
    return sys.platform == "darwin"


#: Deferrals as `autoupdate` skip reasons (what `probe doctor` and the server read).
_SKIPS = {
    DeferReason.RUN_IN_FLIGHT: "SKIP_RUN_IN_FLIGHT",
    DeferReason.SETUP_RUNNING: "SKIP_SETUP_RUNNING",
    DeferReason.ACTION_RUNNING: "SKIP_SETUP_RUNNING",
    DeferReason.DAEMON_RECORDING: "SKIP_DAEMON_RECORDING",
}


def log(message: str) -> None:
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with contextlib.suppress(OSError, ValueError):
        sys.stderr.write(f"[{stamp}] probe-service[{os.getpid()}]: update: {message}\n")
        sys.stderr.flush()


def _env_seconds(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError:
        return default
    return value if value >= 0 else default
