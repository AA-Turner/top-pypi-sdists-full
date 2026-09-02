"""Strict dispatcher for ``runlayer://`` desktop protocol URLs."""

from __future__ import annotations

import webbrowser
from typing import Literal, cast
from urllib.parse import urlsplit

from click.core import Context as ClickContext
import typer

from runlayer_cli.commands.auth import login
from runlayer_cli.commands.setup import sync as setup_sync
from runlayer_cli.config import load_config, normalize_url


UrlAction = Literal["login", "sync", "dashboard"]
_ACTIONS: frozenset[str] = frozenset({"login", "sync", "dashboard"})


def parse_runlayer_url(url: str) -> UrlAction:
    """Return an allowlisted action for an exact, parameter-free protocol URL."""
    parsed = urlsplit(url)
    if (
        not url.startswith("runlayer://")
        or parsed.scheme != "runlayer"
        or parsed.netloc not in _ACTIONS
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Unsupported Runlayer URL")
    return cast(UrlAction, parsed.netloc)


def _context_host(ctx: typer.Context) -> str | None:
    current: ClickContext | None = ctx
    while current is not None:
        if current.obj and current.obj.get("host"):
            return normalize_url(current.obj["host"])
        current = current.parent
    return None


def _resolve_configured_host(ctx: typer.Context) -> str | None:
    return _context_host(ctx) or load_config().default_host


def _validated_dashboard_url(host: str | None) -> str:
    if host is None:
        raise ValueError("No dashboard host configured")
    normalized = normalize_url(host)
    parsed = urlsplit(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Dashboard host must be an HTTP(S) URL")
    return normalized


def handle_url(
    ctx: typer.Context,
    url: str = typer.Argument(..., help="runlayer:// URL to dispatch"),
) -> None:
    """Handle an OS protocol URL without accepting commands or parameters."""
    try:
        action = parse_runlayer_url(url)
        host = _resolve_configured_host(ctx)
        if action == "login":
            login(host=host, ca_bundle=None)
        elif action == "sync":
            setup_sync(
                ctx=ctx,
                client=None,
                header=None,
                secret=None,
                host=host,
                yes=True,
            )
        else:
            dashboard_url = _validated_dashboard_url(host)
            if not webbrowser.open(dashboard_url):
                raise RuntimeError("Could not open dashboard")
    except ValueError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(2) from None
    # typer.Exit subclasses RuntimeError, so the dispatched command's own exit
    # code has to pass through before the generic handler rewrites it to 1.
    except typer.Exit:
        raise
    except RuntimeError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(1) from None
