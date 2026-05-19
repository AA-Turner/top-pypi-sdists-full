import os
from typing import Optional, Type

from dlt.common.configuration import plugins as _plugins
from dlt.common.configuration.plugins import only_host
from dlt.common.configuration.specs.pluggable_run_context import ProfilesRunContext
from dlt.common.runtime.run_context import active as run_context_active

from dlt._workspace.cli import SupportsCliCommand
from dlthub.common.license.decorators import is_scope_active


_LEGACY_COMMANDS_ENABLED_ENV = "DLTHUB_LEGACY_COMMANDS_ENABLED"


def _legacy_commands_enabled() -> bool:
    return os.environ.get(_LEGACY_COMMANDS_ENABLED_ENV, "").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )


__all__ = [
    "_plug_cli_transformation",
    "_plug_cli_cache",
    "_plug_cli_project",
    "_plug_cli_pipeline",
    "_plug_cli_dataset",
    "_plug_cli_source",
    "_plug_cli_destination",
    "_plug_cli_profile",
    "_plug_cli_license",
    "_plug_cli_dbt",
]


def is_project_active() -> bool:
    # verify run context type without importing

    ctx = run_context_active()
    return ctx.__class__.__name__ == "ProjectRunContext"


def supports_profiles() -> bool:
    return isinstance(run_context_active(), ProfilesRunContext)


#
# legacy transformation commands
#


@_plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def _plug_cli_transformation(host: str) -> Optional[Type[SupportsCliCommand]]:
    if not _legacy_commands_enabled():
        return None
    if not is_scope_active("dlthub.project"):
        return None

    from dlt.common.exceptions import MissingDependencyException

    try:
        from dlthub.legacy.transformations.cli import TransformationCommand

        return TransformationCommand
    except (MissingDependencyException, ImportError):
        # TODO: we need a better mechanism to plug in placeholder commands for non installed
        # packages
        from dlt._workspace.cli import SupportsCliCommand

        class _PondCommand(SupportsCliCommand):
            command = "transformation"
            help_string = "Please install dlthub[cache] to enable transformations"

        return _PondCommand


@_plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def _plug_cli_cache(host: str) -> Optional[Type[SupportsCliCommand]]:
    if not _legacy_commands_enabled():
        return None
    if not is_scope_active("dlthub.project"):
        return None

    from dlt.common.exceptions import MissingDependencyException

    try:
        from dlthub.cache.cli import CacheCommand

        return CacheCommand
    except (MissingDependencyException, ImportError):
        from dlt._workspace.cli import SupportsCliCommand

        class _CacheCommand(SupportsCliCommand):
            command = "cache"
            help_string = "Please install dlthub[cache] to use local transformation cache"

        return _CacheCommand


@_plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def _plug_cli_project(host: str) -> Optional[Type[SupportsCliCommand]]:
    if not _legacy_commands_enabled():
        return None
    if not is_scope_active("dlthub.project"):
        return None

    from dlthub.project.cli.project_command import ProjectCommand

    return ProjectCommand


@_plugins.hookimpl(specname="plug_cli", tryfirst=True)
@only_host("dlthub")
def _plug_cli_pipeline(host: str) -> Optional[Type[SupportsCliCommand]]:
    if not is_scope_active("dlthub.project"):
        return None

    if is_project_active():
        # should be executed before dlt command got plugged in (tryfirst) to override it
        from dlthub.project.cli.pipeline_command import ProjectPipelineCommand

        return ProjectPipelineCommand
    return None


@_plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def _plug_cli_dataset(host: str) -> Optional[Type[SupportsCliCommand]]:
    if not is_scope_active("dlthub.project"):
        return None

    if is_project_active():
        from dlthub.project.cli.dataset_command import DatasetCommand

        return DatasetCommand
    return None


@_plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def _plug_cli_source(host: str) -> Optional[Type[SupportsCliCommand]]:
    if not is_scope_active("dlthub.project"):
        return None

    if is_project_active():
        from dlthub.project.cli.source_command import SourceCommand

        return SourceCommand
    return None


@_plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def _plug_cli_destination(host: str) -> Optional[Type[SupportsCliCommand]]:
    if not is_scope_active("dlthub.project"):
        return None

    if is_project_active():
        from dlthub.project.cli.destination_command import DestinationCommand

        return DestinationCommand
    return None


@_plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def _plug_cli_profile(host: str) -> Optional[Type[SupportsCliCommand]]:
    if not is_scope_active("dlthub.project"):
        return None

    if is_project_active():
        from dlthub.project.cli.profile_command import ProfileCommand

        return ProfileCommand
    return None


@_plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def _plug_cli_license(host: str) -> Optional[Type[SupportsCliCommand]]:
    from dlthub.common.license.decorators import _license_enabled

    if not _license_enabled():
        return None

    from dlthub.common.license.cli import LicenseCommand

    return LicenseCommand


@_plugins.hookimpl(specname="plug_cli")
@only_host("dlthub")
def _plug_cli_dbt(host: str) -> Optional[Type[SupportsCliCommand]]:
    if not is_scope_active("dlthub.dbt_generator"):
        return None

    if not supports_profiles():
        return None

    from dlthub.dbt_generator.cli import DbtCommand

    return DbtCommand
