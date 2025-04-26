import click

from ..output.table import output_entry

from agilicus.command_helpers import Command

from . import databases

cmd = Command()


@cmd.command(name="list-database-resources")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--name-slug", default=None)
@click.option("--updated-since", default=None, type=click.DateTime())
@click.option("--resource-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_database_resources(ctx, name=None, **kwargs):
    resources = databases.list_database_resources(ctx, name=name, **kwargs)
    table = databases.format_database_as_text(ctx, resources)
    print(table)


@cmd.command(name="add-database-resource")
@click.option("--name", default=None, required=True)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None)
@click.option("--address", default=None, required=True)
@click.option("--port", type=int, default=None, required=True)
@click.option("--data-source-name", type=str)
@click.option("--runtime-parameter", type=(str, str), multiple=True)
@click.option(
    "--database-protocol", type=click.Choice(databases.PROTOCOLS), required=True
)
@click.pass_context
def add_database_resource(ctx, name, port, runtime_parameter, **kwargs):
    result = databases.add_database_resource(
        ctx, name=name, port=port, runtime_parameters=runtime_parameter, **kwargs
    )
    output_entry(ctx, result)


@cmd.command(name="update-database-resource")
@click.argument("database-resource-id")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None)
@click.option("--address", default=None)
@click.option("--port", type=int, default=None)
@click.option("--username", default=None)
@click.option("--published", type=click.Choice(["no", "public"]), default=None)
@click.option("--runtime-parameter", type=str, multiple=True)
@click.option(
    "--replace-runtime-parameters",
    is_flag=True,
    help="if set, replaces runtime parameters with given values",
)
@click.option("--data-source-name", type=str, default=None)
@click.option(
    "--database-protocol", type=click.Choice(databases.PROTOCOLS), default=None
)
@click.pass_context
def update_database_resource(
    ctx, database_resource_id, port, published, runtime_parameter, **kwargs
):
    result = databases.update_database_resource(
        ctx,
        database_resource_id,
        port,
        published,
        runtime_parameters=runtime_parameter,
        **kwargs,
    )
    output_entry(ctx, result)


@cmd.command(name="show-database-resource")
@click.argument("database-resource-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_database_resource(ctx, database_resource_id, **kwargs):
    result = databases.show_database_resource(ctx, database_resource_id, **kwargs)
    output_entry(ctx, result)


@cmd.command(name="delete-database-resource")
@click.argument("database-resource-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_database_resource(ctx, database_resource_id, **kwargs):
    databases.delete_database_resource(ctx, database_resource_id, **kwargs)


def add_commands(cli):
    cmd.add_to_cli(cli)
