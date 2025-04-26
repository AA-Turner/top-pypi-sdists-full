import click
from ..output.table import output_entry
from . import policy_config


@click.command(name="get-authz-bundle")
@click.pass_context
@click.option("--org-id", default=None)
@click.option("--if-none-match", default=None)
def cli_command_get_authz_bundle(ctx, **kwargs):
    result, status, headers = policy_config.get_authz_bundle(ctx, **kwargs)
    output_entry(ctx, result.to_dict(), headers)


@click.command(name="delete-authz-bundle")
@click.pass_context
@click.option("--org-id", default=None)
def cli_command_delete_authz_bundle(ctx, **kwargs):
    policy_config.delete_authz_bundle(ctx, **kwargs)


@click.command(name="get-resource-url-bundle", help="high level resource map")
@click.pass_context
@click.option(
    "--if-none-match", default=None, help="use sha256 of last fetched to short-circuit"
)
def cli_command_get_resource_url_bundle(ctx, **kwargs):
    result, status, headers = policy_config.get_resource_url_bundle(ctx, **kwargs)
    output_entry(ctx, result.to_dict(), headers)


@click.command(name="delete-resource-url-bundle")
@click.pass_context
def cli_command_delete_resource_url_bundle(ctx, **kwargs):
    policy_config.delete_resource_url_bundle(ctx, **kwargs)


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
