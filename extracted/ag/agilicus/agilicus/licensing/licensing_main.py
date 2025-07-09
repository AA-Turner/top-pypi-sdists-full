import click
import click_extension

from ..output.table import output_entry

from agilicus.command_helpers import Command

from . import product_table_versions

cmd = Command()


@cmd.command(name="list-product-table-versions")
@click.option("--version", default=None)
@click.option("--published", default=None, type=bool)
@click.option("--page-at-version", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_product_table_versions(ctx, **kwargs):
    resources = product_table_versions.list_product_table_versions(ctx, **kwargs)
    table = product_table_versions.format_product_table_versions(ctx, resources)
    print(table)


@cmd.command(name="apply-product-table-version")
@click.option(
    "--input-file",
    required=True,
    type=click_extension.JSONFile("r"),
    help="the filename; - for stdin",
)
@click.pass_context
def add_product_table_version(ctx, **kwargs):
    """
    adds or updates a product table version as specified in a json file. If the
    table exists, it matches based on the version.
    """
    result = product_table_versions.apply_product_table_version(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cmd.command(name="show-product-table-version")
@click.option("--product-table-version-id")
@click.option("--version")
@click.pass_context
def show_product_table_version(ctx, **kwargs):
    """
    Shows a product table version, either by ID or version.
    """
    result = product_table_versions.show_product_table_version(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cmd.command(name="delete-product-table-version")
@click.argument("product-table-version-id")
@click.pass_context
def delete_product_table_version(ctx, product_table_version_id, **kwargs):
    product_table_versions.delete_product_table_version(
        ctx, product_table_version_id, **kwargs
    )


def add_commands(cli):
    cmd.add_to_cli(cli)
