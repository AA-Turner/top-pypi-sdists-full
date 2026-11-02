"""One update step's contract, shared by `probe update` (cli upgrading) and the service's update cycle.
The update child's switches and exit live here once: the service may not import the CLI, so it restated them."""

from __future__ import annotations

from typing import Protocol

#: Told to the update child when the service's DEFER_LIMIT_S ran out: the deferrals it updates past,
#: comma separated (`probe.cli.install.upgrade.turn.forced_past`). Past a live run the run-lock check is
#: skipped (D33); past a setup holding wizard.lock for a day, the update runs without that lock (C1).
FORCED_ENV = "PROBE_UPDATE_FORCED"
#: Told to the update child when the CLI is current and daemon workers run from its env: plugins only (D7).
SKIP_CLI_ENV = "PROBE_UPDATE_SKIP_CLI"
#: Told to the update child when the service did not wait for runs and workers: update the CLI beside
#: the running version or not at all, since nothing they run from is replaced (D6, D33).
SIDE_BY_SIDE_ENV = "PROBE_UPDATE_SIDE_BY_SIDE"
#: What asked for the update (manual, session start, ...), for the server's update report.
TRIGGER_ENV = "PROBE_AUTOUPDATE_TRIGGER"
#: The setup lock, under the state dir: a `probe` setup holds it, and the update child waits on it.
WIZARD_LOCK_NAME = "wizard.lock"
#: EX_TEMPFAIL: the update child (or a setup) found a setup holding WIZARD_LOCK_NAME; try again later.
WIZARD_BUSY_EXIT = 75


class UpdateStep(Protocol):
    """One part of an update: the CLI env, one coding agent's plugins, pi's package or the desktop app.
    `probe update` and the service's cycle each walk their steps in order and record what each did.
    Not the wire vocabulary `probe.foundation.service_api.vocabularies.UpdateStep` (the cycle's step names); `name` is
    one of those, an `UpdatePart` or an agent's source. Implementations land with the cli and service
    splits (agent steps 14 and 16)."""

    #: How progress hooks and update reports name this step.
    name: str

    def run(self) -> object:
        """Bring this part up to date; returns what happened, for the driver to record."""
        ...
