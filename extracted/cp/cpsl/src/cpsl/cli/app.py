import click
from rich.table import Table

from .. import terminal
from ..channel import ServiceClient, pass_service_client
from ..clients.capsule import CreateAppRequest, GetAppRequest, ListAppsRequest
from ..config import app_url


@click.group()
def app():
    """Manage apps."""
    pass


@app.command("create")
@click.option("--name", required=True, help="App name")
@click.option("--price", default=0, type=int, help="Price in cents (0 for free)")
@click.option(
    "--pricing-type",
    default="one_time",
    type=click.Choice(["one_time", "monthly"], case_sensitive=False),
    help="Charge once or as a monthly subscription",
)
@pass_service_client
def create(client: ServiceClient, name: str, price: int, pricing_type: str):
    """Create a new app."""
    res = client.capsule.create_app(
        CreateAppRequest(
            name=name,
            price_in_cents=price,
            pricing_type=pricing_type.lower(),
        )
    )
    if not res.ok:
        terminal.error(f"Failed: {res.err_msg}")
        raise SystemExit(1)

    terminal.success(f'Created app "{res.app.name}" at {app_url(res.app.hostname)}')
    terminal.info(f"  ID:       {res.app.id}")
    terminal.info(f"  Hostname: {res.app.hostname}")
    if res.app.price_in_cents <= 0:
        terminal.info("  Price:    free")
    else:
        terminal.info(
            f"  Price:    {res.app.price_in_cents}¢ / {res.app.pricing_type.replace('_', ' ')}"
        )


@app.command("list")
@pass_service_client
def list_apps(client: ServiceClient):
    """List your apps."""
    res = client.capsule.list_apps(ListAppsRequest())
    if not res.ok:
        terminal.error(f"Failed: {res.err_msg}")
        raise SystemExit(1)

    if not res.apps:
        terminal.info("No apps yet. Create one with 'capsule app create'.")
        return

    from rich.console import Console

    table = Table(title="Apps")
    table.add_column("Name")
    table.add_column("ID")
    table.add_column("Hostname")
    table.add_column("Price")
    table.add_column("Pricing")
    table.add_column("Created")

    for a in res.apps:
        price_label = "free" if a.price_in_cents <= 0 else f"{a.price_in_cents}¢"
        pricing_label = "-" if a.price_in_cents <= 0 else a.pricing_type.replace("_", " ")
        table.add_row(a.name, a.id, a.hostname, price_label, pricing_label, a.created_at)

    Console().print(table)


@app.command("get")
@click.argument("app_id")
@pass_service_client
def get(client: ServiceClient, app_id: str):
    """Get details of an app by ID."""
    res = client.capsule.get_app(GetAppRequest(id=app_id))
    if not res.ok:
        terminal.error(f"Failed: {res.err_msg}")
        raise SystemExit(1)

    a = res.app
    terminal.header(a.name)
    terminal.info(f"  ID:       {a.id}")
    terminal.info(f"  Hostname: {a.hostname}")
    terminal.info(f"  Owner:    {a.owner_id}")
    if a.price_in_cents <= 0:
        terminal.info("  Price:    free")
    else:
        terminal.info(f"  Price:    {a.price_in_cents}¢ / {a.pricing_type.replace('_', ' ')}")
    terminal.info(f"  Created:  {a.created_at}")
