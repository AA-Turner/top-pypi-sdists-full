"""``pysae-ai-tools auth0 token`` — mint a read-only Auth0 Management API token.

Resolves the ``pysae-tooling-auth0-ro`` credentials from AWS Secrets Manager
in-process, runs a ``client_credentials`` grant, and prints the token.

- ``--raw`` prints the bare access token, for capture in ``$(...)`` (this is
  what the ``AUTH0_MGMT_RO_TOKEN`` env resolver consumes).
- Default prints the token metadata as JSON with the access token **masked** —
  never the full secret.
"""

import json
from typing import Annotated

import typer

from ..env import secret_store
from .mgmt import SECRET_ID, Auth0MgmtError, fetch_mgmt_token


def _mask(value: str) -> str:
    return value[:4] + "****" + value[-4:] if len(value) > 12 else "****"


def main(
    raw: Annotated[
        bool,
        typer.Option("--raw", help="Print only the access token (for capture in $(...))."),
    ] = False,
) -> None:
    """Mint a read-only Auth0 Management API token via client_credentials."""
    try:
        client_id = secret_store.get_key(SECRET_ID, "client-id")
        client_secret = secret_store.get_key(SECRET_ID, "client-secret")
    except secret_store.SecretError as exc:
        typer.echo(f"FAILED: {exc}", err=True)
        raise typer.Exit(1) from None

    try:
        payload = fetch_mgmt_token(client_id, client_secret)
    except Auth0MgmtError as exc:
        typer.echo(f"FAILED: {exc}", err=True)
        raise typer.Exit(1) from None

    token = str(payload.get("access_token", ""))
    if not token:
        typer.echo("FAILED: Auth0 returned no access token", err=True)
        raise typer.Exit(1)

    if raw:
        typer.echo(token)
        return

    typer.echo(
        json.dumps(
            {
                "access_token": _mask(token),
                "token_type": payload.get("token_type", "Bearer"),
                "expires_in": payload.get("expires_in"),
                "scope": payload.get("scope", ""),
            },
            indent=2,
        )
    )
