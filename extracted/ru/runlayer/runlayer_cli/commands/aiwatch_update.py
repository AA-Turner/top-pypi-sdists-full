"""Managed AI Watch self-update scheduler entrypoint."""

import os

import typer

from runlayer_cli.commands.update import _run_or_exit
from runlayer_cli.commands.update_scheduler import is_privileged_system_scheduler
from runlayer_cli.mdm_config import read_managed_config, resolve_auto_update


def _is_privileged_scheduler() -> bool:
    return is_privileged_system_scheduler()


def self_update() -> None:
    """Apply the managed AI Watch target from a privileged scheduler."""
    # ``aiwatch.main`` applies managed config before Typer dispatch. Scrub the
    # secret on every exit path so command-metrics cannot inherit it.
    org_api_key = os.environ.pop("RUNLAYER_API_KEY", None)
    if not _is_privileged_scheduler():
        typer.secho(
            "AI Watch self-update runs only from the privileged system scheduler.",
            err=True,
        )
        raise typer.Exit(1)

    managed = read_managed_config()
    if not resolve_auto_update(managed):
        return

    org_api_key = org_api_key or managed.get("org_api_key")
    host = os.environ.get("RUNLAYER_HOST") or managed.get("host")
    if not org_api_key or not host:
        return

    # Scheduler path stays quiet on success so cron/launchd do not emit periodic
    # noise. Structured attempt/success fields are logged by updater.
    _run_or_exit(
        package="ai-watch",
        product="AI Watch",
        host=host,
        org_api_key=org_api_key,
        quiet=True,
        allow_privileged_reexec=False,
    )
