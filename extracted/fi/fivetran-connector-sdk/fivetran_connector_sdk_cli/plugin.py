"""Adapter exposing fivetran_connector_sdk to the fivetran_cli plugin registry."""

from fivetran_connector_sdk_cli.cli import main as _cli_main
from fivetran_connector_sdk_cli.cli_parser import COMMAND_DESCRIPTIONS
from fivetran_connector_sdk_common.constants import TELEMETRY_SOURCE_NAME

class ConnectorSdkPlugin:

    @staticmethod
    def get_commands() -> dict[str, str]:
        return dict(COMMAND_DESCRIPTIONS)

    @staticmethod
    def dispatch(argv: list[str]) -> int:
        # fivetran_connector_sdk_cli.cli.main() signals failure via sys.exit(), which
        # propagates past this call; a normal return (e.g. a successful deploy)
        # falls off the end of main() with no value. `or 0` treats that as success.
        # If main() is ever changed to signal failure via a falsy return instead
        # of sys.exit(), this would silently misreport it as success.
        return _cli_main(argv) or 0

    @staticmethod
    def get_cli_tool_name_for_telemetry() -> str:
        return TELEMETRY_SOURCE_NAME


PLUGIN = ConnectorSdkPlugin()
