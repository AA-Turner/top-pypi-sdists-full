import sys

from flytekit.clis.sdk_in_container.pyflyte import main as pyflyte_main

from union._config import _UNION_CONFIG
from union._usage import _configure_tracking_cli

# This module should only be imported by the union entrypoint, so we set
# _UNION_CONFIG.is_direct_union_cli_call = True to configure the CLI to use union
# defaults. To be safe, we also check for sys.argv to make sure we are only setting
# `is_direct_union_cli_call=True` in a CLI context.
if sys.argv:
    _UNION_CONFIG.is_direct_union_cli_call = True

main = _configure_tracking_cli(pyflyte_main)
main.name = "union"
