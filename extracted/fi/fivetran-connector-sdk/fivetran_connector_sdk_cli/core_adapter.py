"""Connects the Connector SDK to the core that runs a connector on this machine.

The core (`fivetran_connector_sdk_core`) is a separate package that imports nothing from this one. It is given a `Source` to run
and gives it a `Sink` to emit into, and what crosses between them (records, declared tables) is defined by the
core and used by this package as it is. What is left here is what only this package can do: `ConnectorSource` is the `Source`
of a `Connector`, and the core's log goes through the SDK's logger.
"""
import fivetran_connector_sdk_core as core
from fivetran_connector_sdk_common.helpers import print_library_log
from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_cli import runtime, schema_processing


def _log(message: str, level: core.Level, icon: core.Icon, indent: bool):
    """The core's logger: the same levels and icons, printed the way the SDK prints everything else."""
    print_library_log(message, Logging.Level(int(level)), log_icon=Logging.LogIcon(int(icon)), indent=indent)


core.set_logger(_log)


class ConnectorSource:
    """A `Connector` as the core's `Source`."""

    def __init__(self, connector):
        self.connector = connector

    def schema(self, configuration) -> core.SchemaResult:
        schema_processing.reset()
        return self.connector.get_schema(configuration)

    def update(self, configuration, state, sink: core.Sink) -> None:
        runtime.install(sink)
        self.connector.run_update(configuration, state)


def run(connector, project_path: str, configuration, state, apply_renaming: bool = True, destination=None, state_path=None):
    """Runs `connector` in this process against `<project_path>/files/warehouse.db`, or against the Iceberg catalog `destination` (the
    content of destination.json) describes, with the SDK's logging."""
    try:
        return core.run(ConnectorSource(connector), project_path, configuration, state, apply_renaming, destination, state_path)
    finally:
        # Not when update() returns: the core still flushes and writes the state after that, and a connector thread that is
        # still emitting then is accepted, as it always was.
        runtime.install(None)
