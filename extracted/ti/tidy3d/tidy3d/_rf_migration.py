"""Notices for RF APIs that move from Tidy3D to Flexcompute RF in Tidy3D 2.13."""

from __future__ import annotations

from tidy3d.log import log

RF_PLUGIN_MIGRATION_MESSAGE = (
    "'tidy3d.plugins.microwave' and the terminal component modeler "
    "('TerminalComponentModeler' with its lumped, coaxial and wave ports) are moving "
    "to Flexcompute RF and will be removed from Tidy3D in 2.13. Install "
    "'flexcompute-rf' and import them from 'flexcompute.rf.tidy3d' instead. "
    "'ModalComponentModeler' stays in Tidy3D."
)

RF_SIMULATION_DEPRECATION_MESSAGE = (
    "The RF classes in Tidy3D are deprecated and will be removed in Tidy3D 3.0. "
    "They remain available until then, from the top level where they have a name "
    "there and otherwise from 'tidy3d.rf'. New RF development continues in "
    "Flexcompute RF; install 'flexcompute-rf' and import 'flexcompute.rf.tidy3d'."
)


def warn_rf_plugin_migration() -> None:
    """Log that the RF plugins leave Tidy3D in 2.13."""
    # one fixed message, so log_once collapses the import and construction notices
    log.warning(RF_PLUGIN_MIGRATION_MESSAGE, log_once=True)
