"""Tray: initiate OAuth reconnect for one account and open the browser."""

from __future__ import annotations

import webbrowser

import httpx
import typer

from runlayer_cli.api import API_KEY_HEADER_NAME, USER_AGENT
from runlayer_cli.config import load_config
from runlayer_cli.tls import http_client


_INITIATE_TIMEOUT_SECONDS = 15.0


def reconnect_account(
    server_id: str = typer.Option(..., "--server-id", help="Server UUID"),
    account_id: str = typer.Option(..., "--account-id", help="Account UUID"),
) -> None:
    """POST oauth/initiate for account_id, then open authorization_url."""
    config = load_config()
    host = config.default_host
    if not host:
        typer.echo("No default host configured. Run `runlayer login` first.", err=True)
        raise typer.Exit(1)
    secret = config.get_secret_for_host(host)
    if secret is None:
        typer.echo(
            f"Not authenticated to {host}. Run `runlayer login` first.", err=True
        )
        raise typer.Exit(1)

    url = f"{host}/api/v1/servers/{server_id}/oauth/initiate"
    try:
        with http_client(
            headers={
                "User-Agent": USER_AGENT,
                API_KEY_HEADER_NAME: secret,
            },
            timeout=_INITIATE_TIMEOUT_SECONDS,
        ) as client:
            response = client.post(url, params={"account_id": account_id})
            response.raise_for_status()
            payload = response.json()
    except httpx.HTTPError as exc:
        typer.echo(f"Failed to start reconnect: {exc}", err=True)
        raise typer.Exit(1) from exc

    authorization_url = (
        payload.get("authorization_url") if isinstance(payload, dict) else None
    )
    if not isinstance(authorization_url, str) or not authorization_url.strip():
        typer.echo("OAuth initiate response missing authorization_url", err=True)
        raise typer.Exit(1)

    if not webbrowser.open(authorization_url.strip()):
        typer.echo(authorization_url.strip())
        typer.echo("Could not open a browser; open the URL above.", err=True)
        raise typer.Exit(1)

    typer.echo("Opened browser to reconnect.")
