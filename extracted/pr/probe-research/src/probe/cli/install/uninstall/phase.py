"""UninstallPhase protocol and the ordered phase registry `_run` walks (stopping ... finishing)."""

from __future__ import annotations
from probe.cli.install.uninstall.phases.draining import _phase_draining
from probe.cli.install.uninstall.phases.integrations import _phase_integrations
from probe.cli.install.uninstall.phases.server import _phase_server
from probe.cli.install.uninstall.phases.state import _phase_state
from probe.cli.install.uninstall.phases.stopping import _phase_stopping
from probe.cli.install.uninstall.state import Phase


# -- the run ---------------------------------------------------------------------------------


_PHASE_STEPS = {
    Phase.STOPPING: _phase_stopping,
    Phase.DRAINING: _phase_draining,
    Phase.SERVER: _phase_server,
    Phase.INTEGRATIONS: _phase_integrations,
    Phase.STATE: _phase_state,
}
