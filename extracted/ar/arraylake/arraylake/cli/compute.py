from datetime import datetime
from enum import StrEnum

import typer
from rich import print_json
from rich.table import Table

from arraylake import Client
from arraylake.cli.utils import coro, rich_console, simple_progress
from arraylake.client import AsyncClient
from arraylake.log_util import get_logger

app = typer.Typer(help="Manage Arraylake compute services", no_args_is_help=True)
logger = get_logger(__name__)


class ListOutputType(StrEnum):
    rich = "rich"
    json = "json"


def _services_table(services, org):
    table = Table(title=f"Arraylake compute services for [bold]{org}[/bold]", min_width=80)
    table.add_column("Name", justify="left", style="cyan", no_wrap=True, min_width=10)
    table.add_column("Service Type", justify="right", style="green", min_width=10)
    table.add_column("Org", justify="right", style="green", min_width=10)
    table.add_column("Public", justify="right", style="green", min_width=10)
    table.add_column("URL", justify="right", style="green", min_width=10)
    table.add_column("Status", justify="right", style="green", min_width=10)

    status_colors = {"available": "green", "progressing": "yellow", "error": "red", "unknown": "grey"}

    for service in services:
        table.add_row(
            service.name,
            service.config.service_type,
            service.config.org,
            str(service.config.is_public),
            service.url,
            service.status,
            style=status_colors[service.status],
        )

    return table


@app.command(name="enable")
def enable_service(
    org: str = typer.Argument(..., help="The organization to enable the service for"),
    protocol: str = typer.Argument(..., help="The protocol to enable. Must be one of: dap2, edr, wms, tiles, zarr"),
    is_public: bool = typer.Option(False, help="Whether the service is public"),
    deployment_name: str | None = typer.Option(
        None,
        "--deployment-name",
        "-n",
        help="Custom deployment name (defaults to protocol name). Must be lowercase alphanumeric with dashes, max 16 chars.",
    ),
):
    """**Enable** a new service

    **Examples**

    - Enable a new DAP service for _my-org_

        ```
        $ arraylake compute enable my-org dap2
        ```

    - Enable a tiles service with a custom deployment name

        ```
        $ arraylake compute enable my-org tiles --deployment-name my-tiles
        ```
    """
    kwargs = {}
    if deployment_name is not None:
        kwargs["deployment_name"] = deployment_name

    with simple_progress(f"Creating [bold]{protocol}[/bold] service for [bold]{org}[/bold]..."):
        status = Client().get_services(org).enable(protocol, is_public, **kwargs)
    rich_console.print(status["message"])


@app.command(name="list")
def list_services(
    org: str = typer.Argument(..., help="The organization name"),
    output: ListOutputType = typer.Option(ListOutputType.rich, help="Output format"),
):
    """**List** enabled services in the specified organization

    **Examples**

    - List services in _my-org_

        ```
        $ arraylake compute list my-org
        ```
    """
    with simple_progress(f"Listing services for [bold]{org}[/bold]..."):
        services = Client().get_services(org).list_enabled()

    if output == "json":
        services = [service.dict() for service in services]  # type: ignore
        print_json(data=services)
    elif services:
        rich_console.print(_services_table(services, org))
    else:
        rich_console.print("\nNo results")


@app.command(name="status")
def get_service_status(
    org: str = typer.Argument(..., help="The organization where the service is enabled"),
    service_id: str = typer.Argument(..., help="The service ID"),
):
    """**Get** the status of a service

    **Examples**

    - Get the status of a service with ID edr-1234567

        ```
        $ arraylake compute status my-org edr-1234567
        ```
    """
    with simple_progress(f"Getting service status for [bold]{service_id}[/bold]..."):
        status = Client().get_services(org).get_status(service_id)

    rich_console.print(status)


@app.command(name="logs")
@coro  # type: ignore
async def get_service_logs(
    org: str = typer.Argument(..., help="The organization where the service is enabled"),
    service_id: str = typer.Argument(..., help="The service ID"),
    tail: int | None = typer.Option(None, help="The number of lines to return from the end of the log"),
    since: str | None = typer.Option(None, help="The start time of the logs to display, in ISO 8601 format"),
    until: str | None = typer.Option(None, help="The end time of the logs to display, in ISO 8601 format"),
    follow: bool = typer.Option(False, help="Follow the logs as they are written"),
    follow_timeout: int = typer.Option(
        30, min=1, max=10 * 60, help="The timeout for following the logs in seconds. Maximum is 10 minutes."
    ),
):
    """**Get** the logs of a service

    **Examples**

    - Get the logs of a service with ID edr-1234567

        ```
        $ arraylake compute logs my-org edr-1234567
        ```
    """
    try:
        since_datetime = None
        until_datetime = None
        if since:
            since_datetime = datetime.fromisoformat(since)
        if until:
            until_datetime = datetime.fromisoformat(until)

        if not since_datetime and not until_datetime and not tail and not follow:
            tail = 100
    except ValueError:
        rich_console.print("[bold red]Invalid date format, please use ISO 8601 format[/bold red]")
        raise typer.Exit(code=1)

    try:
        with simple_progress(f"Getting service logs for [bold]{service_id}[/bold]..."):
            log_stream = (
                await AsyncClient()
                .get_services(org)
                .stream_logs(
                    service_id, follow=follow, tail=tail, since=since_datetime, until=until_datetime, follow_timeout=follow_timeout
                )
            )

        async for log in log_stream:
            rich_console.print(log)
    except RuntimeError:
        rich_console.print(f"[bold red]No logs found for {org}/{service_id}. Please try again later.[/bold red]")
        raise typer.Exit(code=1)


@app.command(name="disable")
def disable_service(
    org: str = typer.Argument(..., help="The organization that the service belongs to"),
    service_id: str = typer.Argument(..., help="The service ID to disable"),
):
    """**Disable** a service

    **Examples**

    - Disable a service with ID edr-1234567

        ```
        $ arraylake compute disable my-org edr-1234567
        ```
    """
    with simple_progress(f"Disabling service [bold]{service_id}[/bold]..."):
        status = Client().get_services(org).disable(service_id)

    rich_console.print(status["message"])
