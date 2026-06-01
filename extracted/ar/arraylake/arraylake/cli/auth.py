import typer
from rich.align import Align
from rich.panel import Panel

from arraylake import config
from arraylake.cli.utils import (
    coro,
    error_console,
    print_logo,
    print_logo_mini,
    rich_console,
)
from arraylake.config import default_service_uri
from arraylake.token import AuthException, get_auth_handler

auth = typer.Typer(help="Manage Arraylake authentication")

NOT_LOGGED_IN_MESSAGE = "⚠️  Not logged in, please log in with: `arraylake auth login`"


@auth.command()
@coro  # type: ignore
async def login(
    browser: bool = typer.Option(True, "--browser/--no-browser", " /--nobrowser", help="Whether to automatically open a browser window."),
):
    """**Log in** to Arraylake

    This will automatically open a browser window. If **--no-browser** is specified, a link will be printed.

    **Examples**

    - Log in without automatically opening a browser window

        ```
        $ arraylake auth login --no-browser
        ```
    """
    print_logo()
    handler = get_auth_handler(api_endpoint=default_service_uri())
    await handler.login(browser=browser)


@auth.command()
@coro  # type: ignore
async def refresh() -> None:
    """**Refresh** Arraylake's auth token"""
    handler = get_auth_handler(api_endpoint=default_service_uri())
    if handler.tokens is not None:
        try:
            await handler.refresh_token()
        except Exception as e:
            error_console.print(f"\n[bold red]❌  {e}[/bold red]")
    else:
        rich_console.print(Align(f"[yellow]{NOT_LOGGED_IN_MESSAGE}[/yellow]", align="center"))
        raise typer.Exit(code=1)


@auth.command()
@coro  # type: ignore
async def logout() -> None:
    """**Logout** of Arraylake

    **Examples**

    - Logout of arraylake

        ```
        $ arraylake auth logout
        ```
    """
    try:
        handler = get_auth_handler(api_endpoint=default_service_uri())
        await handler.logout()
    except AuthException as e:
        error_console.print(e)
        raise typer.Exit(code=1)


@auth.command()
@coro
async def status():
    """Verify and display information about your authentication **status**"""
    print_logo_mini()
    rich_console.print(Align(Panel.fit(f"[bold]Arraylake API Endpoint[/bold]: {config.get('service.uri')}"), align="center"))

    try:
        handler = get_auth_handler(api_endpoint=default_service_uri())
        user = await handler._get_user()  # checks that the new tokens are valid
        rich_console.print(Align(f"[green][bold]🔓 Logged in as {user.email}[/green][/bold]", align="center"))
    except AuthException:
        rich_console.print(Align(f"[yellow]{NOT_LOGGED_IN_MESSAGE}[/yellow]", align="center"))
        raise typer.Exit(code=1)


@auth.command()
def token():
    """Display your authentication **token**"""
    handler = get_auth_handler(api_endpoint=default_service_uri())
    if handler.tokens is None:
        rich_console.print(Align(f"[yellow]{NOT_LOGGED_IN_MESSAGE}[/yellow]", align="center"))
        raise typer.Exit(code=1)
    try:
        token_value = handler.tokens.id_token.get_secret_value()
        typer.echo(token_value)
    except (AuthException, AttributeError):
        rich_console.print(Align(f"[yellow]{NOT_LOGGED_IN_MESSAGE}[/yellow]", align="center"))
        raise typer.Exit(code=1)
