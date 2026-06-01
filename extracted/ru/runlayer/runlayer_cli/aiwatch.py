"""Scan-only entrypoint for MDM-deployed AI Watch binaries.

Imports only the scan/auth/logs commands — avoids pulling in fastmcp, docker,
mcp, anyio, questionary, etc. that the full CLI needs.
"""

from runlayer_cli.truststore_init import inject as _inject_truststore

_inject_truststore()

# ruff: noqa: E402 - imports below intentionally come after _inject_truststore()
import os

import typer

from runlayer_cli import __version__
from runlayer_cli.commands.auth import login, logout
from runlayer_cli.commands.logs import logs
from runlayer_cli.commands.org_api_key import app as org_api_key_app
from runlayer_cli.commands.scan import app as scan_app
from runlayer_cli.mdm_config import read_managed_config
from runlayer_cli.tls import set_ca_bundle_path

app = typer.Typer(help="Runlayer AI Watch — scan MCP client configurations")

app.add_typer(scan_app, name="scan")
app.add_typer(org_api_key_app, name="org-api-key")
app.command()(login)
app.command()(logout)
app.command()(logs)


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
    """Populate host/secret env vars from the OS-native managed store.

    The MDM pushes the actual org API key value (e.g. ``rl_org_...``) — not a
    name to look up — so we feed it straight into ``RUNLAYER_API_KEY`` which
    the scan command consumes via its ``--secret`` option. Only fills values
    the operator did not already provide, so CLI flags and explicit env vars
    still win. One binary/installer ships to every tenant; the MDM pushes the
    tenant-specific config via Configuration Profile (macOS) or Registry
    (Windows, written by the MSI at install time).
    """
    managed = read_managed_config()
    host = managed.get("host")
    org_api_key = managed.get("org_api_key")
    if host and not os.environ.get("RUNLAYER_HOST"):
        os.environ["RUNLAYER_HOST"] = host
    if org_api_key and not os.environ.get("RUNLAYER_API_KEY"):
        os.environ["RUNLAYER_API_KEY"] = org_api_key


def main() -> None:
    _apply_managed_config()
    app()


if __name__ == "__main__":
    main()
