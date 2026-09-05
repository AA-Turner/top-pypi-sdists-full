import click

from ..output.table import output_entry

from agilicus.command_helpers import Command

from . import printers
from ..input_helpers import page_sort_order_values, search_direction_values

cmd = Command()


@cmd.command(name="list-printers")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--name-slug", default=None)
@click.option("--updated-since", default=None, type=click.DateTime())
@click.option("--resource-id", default=None)
@click.option("--limit", default=500)
@click.option(
    "--page-on", multiple=True, type=click.Choice(printers.page_fields), default=None
)
@click.option("--page-at-key", multiple=True, type=str, default=None)
@click.option(
    "--page-sort", multiple=True, type=click.Choice(page_sort_order_values), default=None
)
@click.option(
    "--search-direction", type=click.Choice(search_direction_values), default=None
)
@click.pass_context
def list_printers(ctx, name=None, **kwargs):
    results = printers.list_printers(ctx, name=name, **kwargs)
    table = printers.format_printers_as_text(ctx, results)
    print(table)


@cmd.command(name="add-printer")
@click.option("--name", default=None, required=True)
@click.option("--printer-name", default=None, required=True)
@click.option("--hostname", default=None, required=True)
@click.option("--port", default=631, type=int)
@click.option("--path", default="/ipp/print", type=str)
@click.option("--driver-name", default="Microsoft IPP Class Driver", type=str)
@click.option(
    "--raw-stream",
    default=False,
    is_flag=True,
    help="Upstream printer is a raw (JetDirect) stream",
)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None, required=True)
@click.pass_context
def add_printer(
    ctx,
    name,
    printer_name,
    hostname,
    port,
    path,
    driver_name,
    **kwargs,
):
    if kwargs.get("raw_stream") and port == 631:
        # Raw (JetDirect/AppSocket) printers default to the JetDirect port.
        # The port is user-configurable — rawness is conveyed by the
        # raw_stream flag itself, not inferred from the port.
        port = 9100
    result = printers.add_printer(
        ctx,
        name=name,
        printer_name=printer_name,
        hostname=hostname,
        port=port,
        path=path,
        driver_name=driver_name,
        **kwargs,
    )
    output_entry(ctx, result)


@cmd.command(name="update-printer")
@click.argument("printer-id")
@click.option("--name", default=None)
@click.option("--printer-name", default=None)
@click.option("--hostname", default=None)
@click.option("--port", default=None, type=int)
@click.option("--path", default=None, type=str)
@click.option("--driver-name", default=None, type=str)
@click.option(
    "--raw-stream",
    default=None,
    is_flag=True,
    help="Upstream printer is a raw (JetDirect) stream",
)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None)
@click.option("--name-slug", default=None)
@click.option("--published", type=click.Choice(["no", "public"]), default=None)
@click.pass_context
def update_printer(ctx, printer_id, published, **kwargs):
    result = printers.update_printer(ctx, printer_id, published=published, **kwargs)
    output_entry(ctx, result)


@cmd.command(name="show-printer")
@click.argument("printer-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_printer(ctx, printer_id, **kwargs):
    result = printers.show_printer(ctx, printer_id, **kwargs)
    output_entry(ctx, result)


@cmd.command(name="delete-printer")
@click.argument("printer-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_printer(ctx, printer_id, **kwargs):
    printers.delete_printer(ctx, printer_id, **kwargs)


def add_commands(cli):
    cmd.add_to_cli(cli)
