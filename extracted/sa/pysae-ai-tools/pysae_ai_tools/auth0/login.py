"""``pysae-ai-tools auth0 login`` — configure the Auth0 CLI (machine login).

Resolves the ``pysae-tooling-auth0-ro`` credentials from AWS Secrets Manager
and runs a non-interactive ``auth0 login`` (client_credentials / machine
login) against the prod tenant, so subsequent ``auth0 api`` calls are
authenticated read-only. Mirrors the ``tools install argocd`` pattern: a
secret resolved in-process configures an external CLI. The client secret is
never printed — it is passed straight to the ``auth0`` subprocess.
"""

import shutil
import subprocess

import typer

from ..env import secret_store
from .mgmt import DOMAIN, SECRET_ID


def main() -> None:
    """Log the ``auth0`` CLI into the prod tenant with the read-only M2M client."""
    if shutil.which("auth0") is None:
        typer.echo(
            "FAILED: auth0 CLI not found — install it first (https://github.com/auth0/auth0-cli).",
            err=True,
        )
        raise typer.Exit(1)

    try:
        client_id = secret_store.get_key(SECRET_ID, "client-id")
        client_secret = secret_store.get_key(SECRET_ID, "client-secret")
    except secret_store.SecretError as exc:
        typer.echo(f"FAILED: {exc}", err=True)
        raise typer.Exit(1) from None

    try:
        result = subprocess.run(
            [
                "auth0",
                "login",
                "--domain",
                DOMAIN,
                "--client-id",
                client_id,
                "--client-secret",
                client_secret,
            ],
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        typer.echo(f"FAILED: could not run auth0 CLI: {exc}", err=True)
        raise typer.Exit(1) from None

    if result.returncode != 0:
        typer.echo(f"FAILED: auth0 login exited with code {result.returncode}", err=True)
        raise typer.Exit(1)

    typer.echo(f"OK: auth0 CLI logged in to {DOMAIN} (read-only Management client).")
