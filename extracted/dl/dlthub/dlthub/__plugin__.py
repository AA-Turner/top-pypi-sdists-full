import os
from typing import Any, Dict, Optional

from dlt.common.configuration import plugins as _plugins
from dlt.common.configuration.specs.pluggable_run_context import RunContextBase

from dlthub.project.cli._plugins import *  # noqa


@_plugins.hookimpl(specname="plug_run_context", tryfirst=True)
def _plug_run_context_impl(
    run_dir: Optional[str], runtime_kwargs: Optional[Dict[str, Any]]
) -> Optional[RunContextBase]:
    """Called when run new context is created"""

    from dlthub.project.exceptions import ProjectRunContextNotAvailable
    from dlthub.project.project_context import (
        create_project_context,
        find_project_dir,
        is_project_dir,
    )

    # use explicit dir or find one starting from cwd
    project_dir = (
        run_dir
        if run_dir and is_project_dir(run_dir)
        else find_project_dir()
        if not run_dir
        else None
    )
    runtime_kwargs = runtime_kwargs or {}
    profile = runtime_kwargs.get("profile")
    if project_dir:
        # TODO: get local_dir, data_dir, and verify settings_dir. allow them to override
        #   settings in project config
        return create_project_context(
            project_dir, profile=profile, validate=runtime_kwargs.get("_validate", False)
        )
    else:
        if runtime_kwargs.get("_required") == "ProjectRunContext":
            raise ProjectRunContextNotAvailable(project_dir or run_dir or os.getcwd())

    # no run dir pass through to next plugin
    return None
