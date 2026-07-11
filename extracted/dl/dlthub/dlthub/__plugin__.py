from typing import Optional, Type

from dlt.common.configuration import plugins as _plugins
from dlt.common.configuration.plugins import only_host
from dlt.common.configuration.specs.pluggable_run_context import ProfilesRunContext
from dlt.common.runtime.run_context import active as run_context_active

from dlt._workspace.cli import SupportsCliCommand


def supports_profiles() -> bool:
    return isinstance(run_context_active(), ProfilesRunContext)


@_plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def _plug_cli_dbt(host: str) -> Optional[Type[SupportsCliCommand]]:
    if not supports_profiles():
        return None

    from dlthub.dbt_generator.cli import DbtCommand

    return DbtCommand
