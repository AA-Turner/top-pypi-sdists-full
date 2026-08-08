# Python internals
from typing import Optional, Type

# Other libraries
from dlt.common.configuration import plugins
from dlt.common.configuration.plugins import only_host
from dlt.common.runtime.run_context import active as run_context_active


def is_workspace_active() -> bool:
    # verify run context type without importing the workspace package
    ctx = run_context_active()
    return ctx.__class__.__name__ == "WorkspaceRunContext"


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_login(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import LoginCommand

    return LoginCommand


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_logout(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import LogoutCommand

    return LogoutCommand


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_run(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import RunCommand

    return RunCommand


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_serve(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import ServeCommand

    return ServeCommand


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_workspace(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import WorkspaceCommand

    return WorkspaceCommand


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_deploy(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import DeployCommand

    return DeployCommand


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_show(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import ShowCommand

    return ShowCommand


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_dashboard(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import DashboardCommand

    return DashboardCommand


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_variable(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import VariableCommand

    return VariableCommand


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_job(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import JobCommand

    return JobCommand


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_job_run(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import JobRunCommand

    return JobRunCommand


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_job_serve(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import JobServeCommand

    return JobServeCommand


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_pipeline_run(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import PipelineRunCommand

    return PipelineRunCommand


@plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def plug_cli_pipeline_show(host: str) -> Optional[Type[plugins.SupportsCliCommand]]:
    if not is_workspace_active():
        return None
    # Current package
    from dlt_runtime.commands import PipelineShowCommand

    return PipelineShowCommand
