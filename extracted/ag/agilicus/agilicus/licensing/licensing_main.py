import click
import click_extension

from ..output.table import output_entry

from agilicus.command_helpers import Command

from . import product_table_versions
from . import licenses

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


@cmd.command(name="list-licenses")
@click.option("--version", default=None)
@click.option("--published", default=None, type=bool)
@click.option("--page-at-version", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_licenses(ctx, **kwargs):
    resources = licenses.list_licenses(ctx, **kwargs)
    table = licenses.format_licenses(ctx, resources)
    print(table)


@cmd.command(name="add-license")
@click.option("--product-table-version", type=str, required=True)
@click.option("--product-name", type=str, required=True)
@click.option(
    "--constraints",
    type=click_extension.JSONFile("r"),
    help="a constraints file; - for stdin",
)
@click.option(
    "--vars",
    type=click_extension.JSONFile("r"),
    help="a constraint variables file; - for stdin",
)
@click.pass_context
def add_license(ctx, **kwargs):
    """
    adds a license. Override constraints may be specified in a JSON file.
    """
    result = licenses.add_license(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cmd.command(name="replace-license")
@click.option("--license-id", required=True)
@click.option(
    "--product-table-version",
    type=str,
)
@click.option(
    "--product-name",
    type=str,
)
@click.option(
    "--constraints",
    type=click_extension.JSONFile("r"),
    help="a constraints file; - for stdin",
)
@click.option(
    "--vars",
    type=click_extension.JSONFile("r"),
    help="a constraint variables file; - for stdin",
)
@click.option(
    "--replace-constraints",
    type=bool,
    is_flag=True,
)
@click.option(
    "--replace-vars",
    type=bool,
    is_flag=True,
)
@click.pass_context
def replace_license(ctx, **kwargs):
    """
    replaces a license. Override constraints may be specified in a JSON file.
    By default constraints and variables are added to/merged. Specify
    --replace-constraints or --replace-vars to replace them entirely.
    """
    result = licenses.update_license(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cmd.command(name="show-license")
@click.option("--license-id", required=True)
@click.pass_context
def show_license(ctx, **kwargs):
    """
    Shows a license by id
    """
    result = licenses.show_license(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cmd.command(name="delete-license")
@click.argument("license-id", required=True)
@click.pass_context
def delete_license(ctx, license_id, **kwargs):
    licenses.delete_license(ctx, license_id, **kwargs)


@cmd.command(name="list-license-details")
@click.option("--org-id", default=None)
@click.option("--license-id", multiple=True, default=None)
@click.option("--page-at-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_license_details(ctx, license_id, **kwargs):
    if not license_id:
        license_id = None
    result = licenses.list_license_details(ctx, license_ids=license_id, **kwargs)
    table = licenses.format_license_details(ctx, result)
    print(table)


@cmd.command(name="list-license-evaluation-contexts")
@click.option("--org-id", default=None)
@click.option("--license-id", multiple=True, default=None)
@click.option("--page-at-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_license_evaluation_contexts(ctx, license_id, **kwargs):
    if not license_id:
        license_id = None
    result = licenses.list_license_evaluation_contexts(
        ctx, license_ids=license_id, **kwargs
    )
    table = licenses.format_license_evaluation_contexts(ctx, result)
    print(table)


def add_commands(cli):
    cmd.add_to_cli(cli)
