"""The name customers import: `from fivetran_connector_sdk import Connector, Operations as op, Logging as log`.

The open-source package's code lives in `fivetran_connector_sdk_cli` (so the repository's tests can load it next to
production's gRPC package, which has the same public names). The open-source wheel installs this module under the public
name, so a connector written against the SDK runs unchanged under `fivetran debug`.
"""
import sys
import fivetran_connector_sdk_common as _common
from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_cli import cli_commands as _cli_commands
from fivetran_connector_sdk_cli import configuration_form, connector as _connector, file_upload, form_field, operations, test
from fivetran_connector_sdk_cli.configuration_form import ConfigurationForm
from fivetran_connector_sdk_cli.file_upload import ByteStream, FileUpload
from fivetran_connector_sdk_cli.operations import Operations
from fivetran_connector_sdk_cli.test import Test

__version__ = _common.__version__
Connector = _connector.Connector  # a connector's `from fivetran_connector_sdk import Connector`, though not in `__all__`
main = _cli_commands.main  # what the `fivetran` command runs

# `import fivetran_connector_sdk.form_field` and the like work as they do with the production package.
for _module in (configuration_form, file_upload, form_field, operations, test):
    sys.modules[f"{__name__}.{_module.__name__.rsplit('.', 1)[1]}"] = _module
__all__ = [cls.__name__ for cls in [ByteStream, FileUpload, Logging, Operations, ConfigurationForm, Test]] + ["form_field"]
