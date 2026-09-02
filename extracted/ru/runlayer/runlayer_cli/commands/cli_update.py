"""Managed Runlayer CLI update scheduler entrypoint."""

import os
import platform

import typer

from runlayer_cli.commands.update import _installed_package_or_exit, _run_or_exit
from runlayer_cli.commands.update_scheduler import is_privileged_system_scheduler
from runlayer_cli.mdm_config import read_managed_config, resolve_auto_update
from runlayer_cli.product import package_display_name


# First release containing the package-owned scheduler and safe native handoff.
# This intentionally exceeds the explicit-update eligibility floor: a managed
# rollback must not replace itself with an installer that removes the scheduler.
MINIMUM_SCHEDULED_UPDATE_TARGET = "0.29.2"
# Linux cron is package content, so rolling below its first shipping release
# would delete the only automatic path back to a managed target.
LINUX_MINIMUM_SCHEDULED_UPDATE_TARGET = "0.30.8"


def _is_privileged_scheduler() -> bool:
    return is_privileged_system_scheduler()


def scheduled_update() -> None:
    """Apply the managed CLI target from the package-owned system scheduler."""
    linux_org_api_key = os.environ.pop("RUNLAYER_API_KEY", None)
    if not _is_privileged_scheduler():
        typer.secho(
            "Runlayer CLI auto-update runs only from the privileged system scheduler.",
            err=True,
        )
        raise typer.Exit(1)

    managed = read_managed_config()
    if not resolve_auto_update(managed):
        return

    system = platform.system()
    host = managed.get("host")
    org_api_key = managed.get("org_api_key")
    if system == "Linux":
        host = host or os.environ.get("RUNLAYER_HOST")
        org_api_key = org_api_key or linux_org_api_key
    if not host or not org_api_key:
        return

    minimum_target_version = (
        LINUX_MINIMUM_SCHEDULED_UPDATE_TARGET
        if system == "Linux"
        else MINIMUM_SCHEDULED_UPDATE_TARGET
    )
    package = _installed_package_or_exit()
    _run_or_exit(
        package=package,
        product=package_display_name(package),
        host=host,
        org_api_key=org_api_key,
        quiet=True,
        allow_privileged_reexec=False,
        minimum_target_version=minimum_target_version,
    )
