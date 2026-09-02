"""Tray: reject one pending access request."""

from __future__ import annotations

import httpx
import typer

from runlayer_cli.api import API_KEY_HEADER_NAME, USER_AGENT
from runlayer_cli.config import load_config
from runlayer_cli.tls import http_client


_REJECT_TIMEOUT_SECONDS = 15.0


def reject_access_request(
    access_request_id: str = typer.Option(
        ..., "--access-request-id", help="Access request UUID"
    ),
) -> None:
    """POST /access-requests/{id}/reject with an empty rejection reason."""
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

    url = f"{host}/api/v1/access-requests/{access_request_id}/reject"
    try:
        with http_client(
            headers={
                "User-Agent": USER_AGENT,
                API_KEY_HEADER_NAME: secret,
                "Content-Type": "application/json",
            },
            timeout=_REJECT_TIMEOUT_SECONDS,
        ) as client:
            response = client.post(url, json={"rejection_reason": None})
            response.raise_for_status()
    except httpx.HTTPError as exc:
        typer.echo(f"Failed to reject access request: {exc}", err=True)
        raise typer.Exit(1) from exc

    typer.echo("Access request rejected.")
