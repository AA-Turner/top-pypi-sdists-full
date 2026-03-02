from typing import Optional, Type

from dlt.common.configuration import plugins
from dlt.common.runtime.run_context import active as run_context_active


def is_workspace_active() -> bool:
    # verify run context type without importing

    ctx = run_context_active()
    return ctx.__class__.__name__ == "WorkspaceRunContext"


@plugins.hookimpl(specname="plug_cli")
def plug_cli_runtime() -> Optional[Type[plugins.SupportsCliCommand]]:
    if is_workspace_active():
        from dlt_runtime.commands import RuntimeCommand

        return RuntimeCommand
    else:
        return None
