import click
from rich.table import Table

from .. import terminal
from ..channel import ServiceClient, pass_service_client
from ..clients.capsule import (
    CreateSecretRequest,
    DeleteSecretRequest,
    ListSecretsRequest,
)


@click.group()
def secret():
    """Manage workspace secrets."""
    pass


@secret.command("create")
@click.argument("pairs", nargs=-1, required=True)
@pass_service_client
def create(client: ServiceClient, pairs: tuple[str, ...]):
    """Create secrets. Pass NAME=VALUE pairs.

    Example: capsule secret create OPENAI_API_KEY=sk-... TELEGRAM_BOT_TOKEN=123:ABC
    """
    for pair in pairs:
        if "=" not in pair:
            terminal.error(f"Invalid format: {pair!r}. Use NAME=VALUE.")
            raise SystemExit(1)

        name, value = pair.split("=", 1)
        res = client.secrets.create_secret(
            CreateSecretRequest(name=name.strip(), value=value.strip())
        )
        if not res.ok:
            terminal.error(f"Failed to create {name}: {res.err_msg}")
            raise SystemExit(1)

        terminal.success(f"Secret \"{name}\" created.")


@secret.command("list")
@pass_service_client
def list_secrets(client: ServiceClient):
    """List all secrets (names only, no values)."""
    res = client.secrets.list_secrets(ListSecretsRequest())
    if not res.ok:
        terminal.error(f"Failed: {res.err_msg}")
        raise SystemExit(1)

    if not res.secrets:
        terminal.info("No secrets. Create one with 'capsule secret create NAME=VALUE'.")
        return

    from rich.console import Console

    table = Table(title="Secrets")
    table.add_column("Name")
    table.add_column("Created")
    table.add_column("Updated")

    for s in res.secrets:
        table.add_row(s.name, s.created_at, s.updated_at)

    Console().print(table)


@secret.command("delete")
@click.argument("name")
@pass_service_client
def delete(client: ServiceClient, name: str):
    """Delete a secret by name."""
    res = client.secrets.delete_secret(DeleteSecretRequest(name=name))
    if not res.ok:
        terminal.error(f"Failed: {res.err_msg}")
        raise SystemExit(1)

    terminal.success(f"Secret \"{name}\" deleted.")
