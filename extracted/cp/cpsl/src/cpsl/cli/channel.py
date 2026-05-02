"""CLI commands for managing channel resources."""

from http import HTTPStatus

import click
import requests
from rich.console import Console
from rich.table import Table

from .. import terminal
from .http import api_base


def _http_base() -> tuple[str, dict[str, str]]:
    """Return (base_url, headers) for the channel HTTP API."""
    return api_base("/channels")


@click.group()
def channel():
    """Manage channel resources."""
    pass


@channel.command("create")
@click.argument("name")
@click.option(
    "--type", "channel_type", required=True, type=click.Choice(["telegram", "slack", "whatsapp"])
)
@click.option("--credentials", "-c", multiple=True, help="key=value credential pairs (repeatable).")
def create(name: str, channel_type: str, credentials: tuple[str, ...]):
    """Create a named channel resource.

    Example:

        capsule channel create my-tg-bot --type telegram -c bot_token=123:ABC
    """
    creds = {}
    for pair in credentials:
        if "=" not in pair:
            terminal.error(f"Invalid credential format: {pair!r}. Expected key=value.")
            raise SystemExit(1)
        k, v = pair.split("=", 1)
        creds[k.strip()] = v.strip()

    if not creds:
        terminal.error("At least one --credentials (-c) key=value is required.")
        raise SystemExit(1)

    base, headers = _http_base()
    r = requests.post(
        base,
        json={"name": name, "type": channel_type, "credentials": creds},
        headers=headers,
    )

    if r.status_code == HTTPStatus.CONFLICT:
        terminal.error(f"Channel name '{name}' already exists.")
        raise SystemExit(1)
    if r.status_code not in (HTTPStatus.OK, HTTPStatus.CREATED):
        terminal.error(f"Failed: {r.text}")
        raise SystemExit(1)

    data = r.json().get("channel", {})
    terminal.success(f"Channel '{name}' created.")
    terminal.detail(f"  id: {data.get('id', '')}")
    terminal.detail(f"  webhook_id: {data.get('webhook_id', '')}")


@channel.command("list")
def list_channels():
    """List all channel resources."""
    base, headers = _http_base()
    r = requests.get(base, headers=headers)

    if r.status_code != HTTPStatus.OK:
        terminal.error(f"Failed: {r.text}")
        raise SystemExit(1)

    channels = r.json().get("channels", [])
    if not channels:
        terminal.info(
            "No channels. Create one with 'capsule channel create <name> --type <type> -c key=value'."
        )
        return

    table = Table(title="Channels")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Bound To")
    table.add_column("Version")
    table.add_column("ID")
    table.add_column("Created")

    for ch in channels:
        bound = ch.get("bound_to") or "—"
        if ch.get("bound_to") and ch.get("version") is not None:
            version_col = f"v{ch['version']}"
        else:
            version_col = "—"
        table.add_row(
            ch["name"],
            ch["channel_type"],
            bound,
            version_col,
            ch["id"],
            ch.get("created_at", ""),
        )

    Console().print(table)


@channel.command("info")
@click.argument("name")
def info(name: str):
    """Show details for a channel resource."""
    base, headers = _http_base()

    # List and find by name
    r = requests.get(base, headers=headers)
    if r.status_code != HTTPStatus.OK:
        terminal.error(f"Failed: {r.text}")
        raise SystemExit(1)

    channels = r.json().get("channels", [])
    match = next((c for c in channels if c["name"] == name), None)
    if not match:
        terminal.error(f"Channel '{name}' not found.")
        raise SystemExit(1)

    terminal.header("Channel", name)
    terminal.detail(f"  ID:         {match['id']}")
    terminal.detail(f"  Type:       {match['channel_type']}")
    terminal.detail(f"  Webhook ID: {match['webhook_id']}")
    terminal.detail(f"  Created:    {match.get('created_at', '')}")

    bound = match.get("bound_to")
    if bound:
        terminal.detail(f"  Bound to:   {bound}")
        if match.get("version") is not None:
            terminal.detail(f"  Version:    v{match['version']}")
    else:
        terminal.detail("  Bound to:   (unbound)")


@channel.command("delete")
@click.argument("name")
@click.option("--force", is_flag=True, help="Unbind and delete even if currently bound.")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation.")
def delete(name: str, force: bool, yes: bool):
    """Delete a channel resource."""
    base, headers = _http_base()

    # Look up ID by name
    r = requests.get(base, headers=headers)
    if r.status_code != HTTPStatus.OK:
        terminal.error(f"Failed: {r.text}")
        raise SystemExit(1)

    channels = r.json().get("channels", [])
    match = next((c for c in channels if c["name"] == name), None)
    if not match:
        terminal.error(f"Channel '{name}' not found.")
        raise SystemExit(1)

    if not yes:
        click.confirm(f"Delete channel '{name}'? This cannot be undone", abort=True)

    params = {"force": "true"} if force else {}
    r = requests.delete(f"{base}/{match['id']}", headers=headers, params=params)

    if r.status_code == HTTPStatus.CONFLICT:
        terminal.error("Channel is bound to an app. Use --force to unbind and delete.")
        raise SystemExit(1)
    if r.status_code not in (HTTPStatus.OK, HTTPStatus.NO_CONTENT):
        terminal.error(f"Failed: {r.text}")
        raise SystemExit(1)

    terminal.success(f"Channel '{name}' deleted.")


@channel.command("bind")
@click.argument("name")
@click.option("--app", "app_name", required=True, help="App name to bind the channel to.")
@click.option(
    "--version",
    "version",
    type=int,
    default=None,
    help="Pin to a specific app version. Omit to pin to the current latest deploy.",
)
@click.option("--force", is_flag=True, help="Unbind from current app first if already bound.")
def bind(name: str, app_name: str, version: int | None, force: bool):
    """Bind a channel to a specific app version.

    Bindings are always pinned to a concrete deploy version — they do not
    track future deploys. Omit --version to pin to the app's current
    latest deploy. Rebind to roll forward.

    Use --force to unbind the channel from its current app before rebinding.
    """
    base, headers = _http_base()

    r = requests.get(base, headers=headers)
    if r.status_code != HTTPStatus.OK:
        terminal.error(f"Failed: {r.text}")
        raise SystemExit(1)

    channels = r.json().get("channels", [])
    match = next((c for c in channels if c["name"] == name), None)
    if not match:
        terminal.error(f"Channel '{name}' not found.")
        raise SystemExit(1)

    if force and match.get("bound_to"):
        terminal.info(f"Unbinding '{name}' from {match['bound_to']}...")
        r = requests.post(f"{base}/{match['id']}/unbind", headers=headers)
        if r.status_code not in (HTTPStatus.OK, HTTPStatus.CONFLICT):
            terminal.error(f"Unbind failed: {r.text}")
            raise SystemExit(1)

    payload: dict = {"app_name": app_name}
    if version is not None:
        payload["version"] = version

    r = requests.post(f"{base}/{match['id']}/bind", json=payload, headers=headers)

    if r.status_code == HTTPStatus.CONFLICT:
        terminal.error(r.json().get("message", "bind failed"))
        raise SystemExit(1)
    if r.status_code != HTTPStatus.OK:
        terminal.error(f"Failed: {r.text}")
        raise SystemExit(1)

    result = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    version_label = f"v{result['version']}" if result.get("version") is not None else "?"
    terminal.success(f"Channel '{name}' bound to {app_name} ({version_label}).")


@channel.command("unbind")
@click.argument("name")
def unbind(name: str):
    """Unbind a channel from its current app."""
    base, headers = _http_base()

    r = requests.get(base, headers=headers)
    if r.status_code != HTTPStatus.OK:
        terminal.error(f"Failed: {r.text}")
        raise SystemExit(1)

    channels = r.json().get("channels", [])
    match = next((c for c in channels if c["name"] == name), None)
    if not match:
        terminal.error(f"Channel '{name}' not found.")
        raise SystemExit(1)

    r = requests.post(f"{base}/{match['id']}/unbind", headers=headers)

    if r.status_code == HTTPStatus.CONFLICT:
        terminal.error("Channel is not bound to any app.")
        raise SystemExit(1)
    if r.status_code != HTTPStatus.OK:
        terminal.error(f"Failed: {r.text}")
        raise SystemExit(1)

    terminal.success(f"Channel '{name}' unbound.")
