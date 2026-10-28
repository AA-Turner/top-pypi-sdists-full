import os

import httpx
import typer
from rich.align import Align
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel

from arraylake.cli.utils import (
    coro,
    error_console,
    print_logo,
    print_logo_mini,
    rich_console,
)
from arraylake.config import default_service_uri, default_token
from arraylake.token import AuthException, TokenHandler, describe_token, get_auth_handler

auth = typer.Typer(help="Manage Arraylake authentication")

NOT_LOGGED_IN_MESSAGE = "⚠️  Not logged in, please log in with: `al auth login`"

# `al auth token` refreshes tokens that expire sooner than this, so the printed token stays usable for a while.
TOKEN_MIN_VALID_SECONDS = 300

# Uncolored notices on stderr, keeping stdout machine-readable.
notice_console = Console(stderr=True)

SERVICE_URI_OPTION = typer.Option(
    None,
    "--service-uri",
    help=(
        "Arraylake API endpoint to act on, e.g. **https://dev.api.earthmover.io**. Defaults to the configured "
        "**service.uri**. Tokens are stored per endpoint, so this need not be persisted to config — unless "
        "**service.token_path** is set, which makes all endpoints share one token file."
    ),
)


def _resolve_service_uri(service_uri: str | None) -> str:
    return service_uri if service_uri else default_service_uri()


@auth.command()
@coro  # type: ignore
async def login(
    browser: bool = typer.Option(True, "--browser/--no-browser", " /--nobrowser", help="Whether to automatically open a browser window."),
    service_uri: str | None = SERVICE_URI_OPTION,
):
    """**Log in** to Arraylake

    This will automatically open a browser window. If **--no-browser** is specified, a link will be printed.

    **Examples**

    - Log in without automatically opening a browser window

        ```
        $ al auth login --no-browser
        ```

    - Log in to a non-default Arraylake deployment

        ```
        $ al auth login --service-uri https://dev.api.earthmover.io
        ```
    """
    print_logo()
    handler = get_auth_handler(api_endpoint=_resolve_service_uri(service_uri))
    await handler.login(browser=browser)


@auth.command()
@coro  # type: ignore
async def refresh(service_uri: str | None = SERVICE_URI_OPTION) -> None:
    """**Refresh** Arraylake's auth token"""
    handler = get_auth_handler(api_endpoint=_resolve_service_uri(service_uri))
    if handler.tokens is not None:
        try:
            await handler.refresh_token()
        except Exception as e:
            error_console.print(f"\n[bold red]❌  {e}[/bold red]")
            raise typer.Exit(code=1)
    else:
        rich_console.print(Align(f"[yellow]{NOT_LOGGED_IN_MESSAGE}[/yellow]", align="center"))
        raise typer.Exit(code=1)


@auth.command()
@coro  # type: ignore
async def logout(service_uri: str | None = SERVICE_URI_OPTION) -> None:
    """**Logout** of Arraylake

    **Examples**

    - Logout of arraylake

        ```
        $ al auth logout
        ```

    - Log out of a non-default Arraylake deployment

        ```
        $ al auth logout --service-uri https://dev.api.earthmover.io
        ```
    """
    try:
        handler = get_auth_handler(api_endpoint=_resolve_service_uri(service_uri))
        await handler.logout()
    except AuthException as e:
        error_console.print(e)
        raise typer.Exit(code=1)


def _configured_token_name() -> str:
    return "ARRAYLAKE_TOKEN" if os.environ.get("ARRAYLAKE_TOKEN", "").strip() else "The `token` arraylake config setting"


async def _check_configured_token(handler: TokenHandler, token: str) -> bool:
    """Report on a configured token, which clients use instead of the cached login. Returns whether it is valid."""
    name = _configured_token_name()
    rich_console.print(
        Align(f"[yellow]{name} is set ({describe_token(token)}) and takes precedence over your cached login.[/yellow]", align="center")
    )
    try:
        async with handler._create_async_client() as client:
            response = await client.get(
                f"{handler.api_endpoint}/user", headers={"Authorization": f"Bearer {token}", **handler.arraylake_headers}
            )
    except httpx.HTTPError as e:
        rich_console.print(Align(f"[yellow]⚠️  Could not verify {name}: {escape(str(e))}[/yellow]", align="center"))
        return False
    if response.status_code != httpx.codes.OK:
        hint = "`unset ARRAYLAKE_TOKEN`" if name == "ARRAYLAKE_TOKEN" else "remove it"
        rich_console.print(
            Align(f"[red]❌ {name} was rejected ({response.status_code}); {hint} to use your cached login.[/red]", align="center")
        )
        return False
    rich_console.print(Align(f"[green][bold]🔓 {name} is valid ({response.json().get('email', 'unknown')})[/bold][/green]", align="center"))
    return True


@auth.command()
@coro  # type: ignore
async def status(service_uri: str | None = SERVICE_URI_OPTION):
    """Verify and display information about your authentication **status**

    Reports **ARRAYLAKE_TOKEN** (or the **token** config setting) first when set, since clients use it instead of
    the cached login.
    """
    endpoint = _resolve_service_uri(service_uri)
    print_logo_mini()
    rich_console.print(Align(Panel.fit(f"[bold]Arraylake API Endpoint[/bold]: {endpoint}"), align="center"))

    handler = get_auth_handler(api_endpoint=endpoint)
    configured_token = default_token()
    configured_token_ok = await _check_configured_token(handler, configured_token) if configured_token else None
    try:
        user = await handler._get_user()  # checks that the new tokens are valid
        rich_console.print(Align(f"[green][bold]🔓 Logged in as {user.email}[/green][/bold]", align="center"))
    except AuthException:
        if configured_token_ok is None:
            rich_console.print(Align(f"[yellow]{NOT_LOGGED_IN_MESSAGE}[/yellow]", align="center"))
            raise typer.Exit(code=1)
        rich_console.print(Align("[dim]No valid cached login (`al auth login`) for this endpoint.[/dim]", align="center"))
    if configured_token_ok is False:
        raise typer.Exit(code=1)


@auth.command()
@coro  # type: ignore
async def token(service_uri: str | None = SERVICE_URI_OPTION):
    """Print your login's ID **token**, refreshing it first if it has expired or is about to

    Only the token goes to stdout, so it can be captured, e.g. **PGPASSWORD="$(al auth token)"**. Make sure
    **--service-uri** matches the deployment you will send the token to.
    """
    endpoint = _resolve_service_uri(service_uri)
    handler = get_auth_handler(api_endpoint=endpoint)
    if handler.tokens is None:
        error_console.print(NOT_LOGGED_IN_MESSAGE)
        raise typer.Exit(code=1)
    try:
        token_value = await handler.get_fresh_id_token(min_valid_seconds=TOKEN_MIN_VALID_SECONDS)
    except AuthException as e:
        error_console.print(f"❌ {escape(str(e))}")
        raise typer.Exit(code=1)
    notice_console.print(f"[dim]ID token for {endpoint} ({describe_token(token_value)})[/dim]", highlight=False)
    if default_token():
        notice_console.print(
            f"[yellow]Note: {_configured_token_name()} is set and takes precedence over this login in Arraylake clients.[/yellow]"
        )
    typer.echo(token_value)
