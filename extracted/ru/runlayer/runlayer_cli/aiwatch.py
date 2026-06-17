"""Single entrypoint for the AI Watch frozen executable (see cli/AGENTS.md).

One ``aiwatch`` binary serves both the typer CLI (scan / enroll / setup hooks /
bootstrap) and the MCP guardrail hook. ``aiwatch hook ...`` is dispatched to
``runlayer_cli.hook.dispatch.run_hook`` before the typer app loads.
"""

from runlayer_cli.truststore_init import inject as _inject_truststore

_inject_truststore()

# ruff: noqa: E402 - imports below intentionally come after _inject_truststore()
import os
import sys

import typer

from runlayer_cli import __version__
from runlayer_cli.commands.aiwatch_setup import app as aiwatch_setup_app
from runlayer_cli.commands.auth import login, logout
from runlayer_cli.commands.bootstrap import bootstrap
from runlayer_cli.commands.enroll import enroll
from runlayer_cli.commands.logs import logs
from runlayer_cli.commands.org_api_key import app as org_api_key_app
from runlayer_cli.commands.scan import app as scan_app
from runlayer_cli.mdm_config import read_managed_config
from runlayer_cli.tls import set_ca_bundle_path

HOOK_SUBCOMMAND = "hook"

app = typer.Typer(help="Runlayer AI Watch — scan MCP client configurations")

app.add_typer(scan_app, name="scan")
app.add_typer(org_api_key_app, name="org-api-key")
app.add_typer(aiwatch_setup_app, name="setup")
app.command()(login)
app.command()(logout)
app.command()(logs)
app.command()(enroll)
app.command()(bootstrap)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"aiwatch version {__version__}")
        raise typer.Exit()


@app.callback()
def _root(
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
    ca_bundle: str | None = typer.Option(
        None,
        "--ca-bundle",
        help="Path to a PEM CA bundle for TLS inspection proxies.",
    ),
) -> None:
    set_ca_bundle_path(ca_bundle)


def _apply_managed_config() -> None:
    """Populate host/secret env vars from MDM-managed config (CLI flags / env still win)."""
    managed = read_managed_config()
    host = managed.get("host")
    org_api_key = managed.get("org_api_key")
    if host and not os.environ.get("RUNLAYER_HOST"):
        os.environ["RUNLAYER_HOST"] = host
    if org_api_key and not os.environ.get("RUNLAYER_API_KEY"):
        os.environ["RUNLAYER_API_KEY"] = org_api_key


def main() -> None:
    from runlayer_cli.runtime import mark_aiwatch_runtime  # noqa: PLC0415

    mark_aiwatch_runtime()

    from runlayer_cli.hook.relay import (  # noqa: PLC0415
        TRANSCRIPT_STREAM_WORKER_SENTINEL,
    )

    if len(sys.argv) >= 2 and sys.argv[1] == TRANSCRIPT_STREAM_WORKER_SENTINEL:
        from runlayer_cli.hook import _transcript_stream_worker  # noqa: PLC0415

        sys.argv = [sys.argv[0], *sys.argv[2:]]
        _transcript_stream_worker.main()
        return

    # Single converged binary: ``aiwatch hook ...`` is dispatched here (before
    # the typer app) so the hot hook path stays fast and never imports the
    # heavier command/scan modules. Strip the ``hook`` token so ``run_hook``
    # sees the same argv the legacy ``aiwatch-hook`` exe did.
    if len(sys.argv) >= 2 and sys.argv[1] == HOOK_SUBCOMMAND:
        from runlayer_cli.hook.dispatch import run_hook  # noqa: PLC0415

        sys.argv = [sys.argv[0], *sys.argv[2:]]
        run_hook()
        return

    _apply_managed_config()
    app()


if __name__ == "__main__":
    main()
