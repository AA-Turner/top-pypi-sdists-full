import typer
from rich.align import Align
from rich.panel import Panel

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

SERVICE_URI_OPTION = typer.Option(
    None,
    "--service-uri",
    help=(
        "Arraylake API endpoint to act on, e.g. **https://api.dev.earthmover.io**. Defaults to the configured "
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
        $ arraylake auth login --no-browser
        ```

    - Log in to a non-default Arraylake deployment

        ```
        $ arraylake auth login --service-uri https://api.dev.earthmover.io
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
        $ arraylake auth logout
        ```

    - Log out of a non-default Arraylake deployment

        ```
        $ arraylake auth logout --service-uri https://api.dev.earthmover.io
        ```
    """
    try:
        handler = get_auth_handler(api_endpoint=_resolve_service_uri(service_uri))
        await handler.logout()
    except AuthException as e:
        error_console.print(e)
        raise typer.Exit(code=1)


@auth.command()
@coro  # type: ignore
async def status(service_uri: str | None = SERVICE_URI_OPTION):
    """Verify and display information about your authentication **status**"""
    endpoint = _resolve_service_uri(service_uri)
    print_logo_mini()
    rich_console.print(Align(Panel.fit(f"[bold]Arraylake API Endpoint[/bold]: {endpoint}"), align="center"))

    try:
        handler = get_auth_handler(api_endpoint=endpoint)
        user = await handler._get_user()  # checks that the new tokens are valid
        rich_console.print(Align(f"[green][bold]🔓 Logged in as {user.email}[/green][/bold]", align="center"))
    except AuthException:
        rich_console.print(Align(f"[yellow]{NOT_LOGGED_IN_MESSAGE}[/yellow]", align="center"))
        raise typer.Exit(code=1)


@auth.command()
def token(service_uri: str | None = SERVICE_URI_OPTION):
    """Display your authentication **token**"""
    handler = get_auth_handler(api_endpoint=_resolve_service_uri(service_uri))
    if handler.tokens is None:
        rich_console.print(Align(f"[yellow]{NOT_LOGGED_IN_MESSAGE}[/yellow]", align="center"))
        raise typer.Exit(code=1)
    try:
        token_value = handler.tokens.id_token.get_secret_value()
        typer.echo(token_value)
    except (AuthException, AttributeError):
        rich_console.print(Align(f"[yellow]{NOT_LOGGED_IN_MESSAGE}[/yellow]", align="center"))
        raise typer.Exit(code=1)
