import typer
from rich.table import Table

from arraylake import AsyncClient
from arraylake.cli.utils import coro, rich_console, simple_progress

app = typer.Typer(help="Manage Arraylake organizations", no_args_is_help=True)


def _orgs_table(orgs) -> Table:
    table = Table(title="Arraylake Organizations", min_width=60)
    table.add_column("Name", justify="left", style="cyan", no_wrap=True, min_width=30)
    table.add_column("Display Name", justify="left", style="green", min_width=20)
    table.add_column("Status", justify="right", style="green", min_width=10)

    for org in orgs:
        table.add_row(org.name, org.display_name or org.name, org.status)

    return table


@app.command(name="list")
@coro
async def list_orgs():
    """**List** all organizations for the authenticated user

    **Examples**

    - List all orgs

        ```
        $ arraylake org list
        ```
    """
    with simple_progress("Listing orgs..."):
        orgs = await AsyncClient().get_orgs()

    if orgs:
        rich_console.print(_orgs_table(orgs))
    else:
        rich_console.print("\nNo organizations found")
