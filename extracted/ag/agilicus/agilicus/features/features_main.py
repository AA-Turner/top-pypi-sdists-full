import click
from . import features
from ..output.table import output_entry
from .. import billing
from ..input_helpers import get_org_from_input_or_ctx
from ..context import get_apiclient_from_ctx
from agilicus.output.table import make_columns
from agilicus.output.table import format_table


@click.command(name="list-features")
@click.pass_context
@click.option("--show-columns", type=str, default=None)
@click.option("--reset-columns", is_flag=True, default=False)
def cli_command_list_features(ctx, show_columns, reset_columns, **kwargs):
    results = features.list_features(ctx, **kwargs)
    spec = """
       - metadata.id(newname=id)
       - spec.name(newname=name)
       - spec.priority(newname=priority)
       - spec.key(newname=key)
       - spec.value(newname=value)
       - status.products(out_name=products):
           - spec.label(newname=label)
    """
    columns = make_columns(
        ctx,
        results,
        spec,
        show=show_columns,
        clear=reset_columns,
    )
    print(format_table(ctx, results, columns))


@click.command(name="add-feature")
@click.argument("name")
@click.argument("key")
@click.option("--priority", default=None, type=int)
@click.option("--description", default=None)
@click.option("--min", type=int, default=None)
@click.option("--max", type=int, default=None)
@click.option("--enabled", type=bool, default=None)
@click.pass_context
def cli_command_add_feature(ctx, **kwargs):
    result = features.add_feature(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="delete-feature")
@click.argument("feature-id")
@click.pass_context
def cli_command_delete_feature(ctx, *args, **kwargs):
    features.delete_feature(ctx, *args, **kwargs)


@click.command(name="show-feature")
@click.argument("feature_id")
@click.pass_context
def cli_command_show_features(ctx, *args, **kwargs):
    result = features.get_features(ctx, *args, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="update-feature")
@click.argument("feature_id")
@click.option("--name", default=None)
@click.option("--priority", default=None, type=int)
@click.option("--description", default=None)
@click.option("--min", type=int, default=None)
@click.option("--max", type=int, default=None)
@click.option("--enabled", type=bool, default=None)
@click.pass_context
def cli_command_update_feature(ctx, *args, **kwargs):
    result = features.update_feature(ctx, *args, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="list-feature-subscriptions")
@click.argument("feature_id")
@click.pass_context
def cli_command_list_feature_subscriptions(ctx, **kwargs):
    results = features.list_feature_subscriptions(ctx, **kwargs)
    print(billing.format_subscriptions(ctx, results))


@click.command(name="list-org-features")
@click.option("--org-id", default=None)
@click.option("--show-columns", type=str, default=None)
@click.option("--reset-columns", is_flag=True, default=False)
@click.pass_context
def cli_command_list_org_features(ctx, show_columns, reset_columns, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    api = get_apiclient_from_ctx(ctx).org_api
    results = api.get_org_features(org_id).features
    columns = make_columns(
        ctx,
        results,
        """
          - metadata.id(newname=id)
          - spec.name(newname=name)
          - spec.priority(newname=priority)
          - spec.key(newname=key)
          - spec.value(newname=value)
        """,
        show=show_columns,
        clear=reset_columns,
    )
    print(format_table(ctx, results, columns))


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
