"""Tray: submit one pending approval decision."""

from __future__ import annotations

from uuid import UUID

import httpx
import typer

from runlayer_cli.api import API_KEY_HEADER_NAME, USER_AGENT
from runlayer_cli.config import load_config
from runlayer_cli.tls import http_client


_DECISION_TIMEOUT_SECONDS = 15.0


def decide_approval(
    approval_request_id: UUID = typer.Option(
        ..., "--approval-request-id", help="Approval request UUID"
    ),
    approve: bool = typer.Option(False, "--approve", help="Approve the request"),
    prevent: bool = typer.Option(False, "--prevent", help="Prevent the request"),
) -> None:
    """POST a decision for one exact approval request."""
    if approve == prevent:
        typer.echo("Choose exactly one of --approve or --prevent.", err=True)
        raise typer.Exit(1)

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

    url = f"{host}/api/v1/approvals/{approval_request_id}/decision"
    try:
        with http_client(
            headers={
                "User-Agent": USER_AGENT,
                API_KEY_HEADER_NAME: secret,
            },
            timeout=_DECISION_TIMEOUT_SECONDS,
        ) as client:
            response = client.post(url, json={"approve": approve})
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        # The tray shows this stderr verbatim, so lead with the server's reason
        # ("already decided", "decide this one in the dashboard") over the
        # generic httpx phrasing.
        typer.echo(
            f"Failed to submit approval decision: {_reason(exc.response)}", err=True
        )
        raise typer.Exit(1) from exc
    except httpx.HTTPError as exc:
        typer.echo(f"Failed to submit approval decision: {exc}", err=True)
        raise typer.Exit(1) from exc

    typer.echo("Approved." if approve else "Prevented.")


def _reason(response: httpx.Response) -> str:
    """Pull FastAPI's `detail` out of an error body, else fall back to status."""
    fallback = f"HTTP {response.status_code}"
    try:
        payload = response.json()
    except ValueError:
        return fallback
    if not isinstance(payload, dict):
        return fallback
    detail = payload.get("detail")
    if isinstance(detail, str) and detail.strip():
        return detail.strip()
    # Conflicts send {"message": ..., "status": ...} under detail.
    if isinstance(detail, dict):
        message = detail.get("message")
        if isinstance(message, str) and message.strip():
            status = detail.get("status")
            return f"{message.strip()} ({status})" if status else message.strip()
    return fallback
