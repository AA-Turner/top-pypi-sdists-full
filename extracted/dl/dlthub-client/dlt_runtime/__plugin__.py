# Python internals
from typing import TYPE_CHECKING, Optional, Set, Type

# Other libraries
from dlt.common.configuration import plugins
from dlt.common.configuration.plugins import only_host
from dlt.common.runtime.run_context import active as run_context_active

if TYPE_CHECKING:
    # Other libraries
    from dlt._workspace._plugins import McpFeatures


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


# Ungated on purpose, unlike the cli hooks: the tools address a platform
# workspace by id, so a local dlt workspace is not needed to reach one.
@plugins.hookimpl(specname="plug_mcp")
def plug_mcp_jobs(features: Set[str]) -> Optional["McpFeatures"]:
    """Contribute the read-only job and run tools, on `--features=+dlthub.jobs`."""
    # Current package
    from dlthub_mcp import jobs_features

    return jobs_features(features)


@plugins.hookimpl(specname="plug_mcp")
def plug_mcp_logs(features: Set[str]) -> Optional["McpFeatures"]:
    """Contribute the read-only run log tools, on `--features=+dlthub.logs`."""
    # Current package
    from dlthub_mcp import logs_features

    return logs_features(features)


@plugins.hookimpl(specname="plug_mcp")
def plug_mcp_config(features: Set[str]) -> Optional["McpFeatures"]:
    """Contribute the read-only configuration tools, on `--features=+dlthub.config`."""
    # Current package
    from dlthub_mcp import config_features

    return config_features(features)


@plugins.hookimpl(specname="plug_mcp")
def plug_mcp_telemetry(features: Set[str]) -> Optional["McpFeatures"]:
    """Contribute the read-only telemetry tools, on `--features=+dlthub.telemetry`."""
    # Current package
    from dlthub_mcp import telemetry_features

    return telemetry_features(features)
