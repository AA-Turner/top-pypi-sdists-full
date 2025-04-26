import click

from . import public_file_org_links
from ..output.table import output_entry


@click.command(name="add-public-file-org-link")
@click.option("--link-org-id", required=True)
@click.option("--target-org-id", required=True)
@click.option("--file-tag", required=True)
@click.pass_context
def cli_command_add_public_file_org_link(ctx, **kwargs):
    output_entry(ctx, public_file_org_links.add_public_file_org_link(ctx, **kwargs))


@click.command(name="list-public-file-org-links")
@click.option("--link-org-id", default=None)
@click.option("--tag", default=None)
@click.option("--page-at-id", default=None)
@click.pass_context
def cli_command_list_public_file_org_links(ctx, **kwargs):
    result = public_file_org_links.list_public_file_org_links(ctx, **kwargs)
    print(public_file_org_links.format_public_file_org_links(ctx, result))


@click.command(name="get-public-file-org-link")
@click.option("--public-file-org-link-id", required=True)
@click.option("--link-org-id", required=True)
@click.pass_context
def cli_command_get_public_file_org_link(ctx, **kwargs):
    output_entry(
        ctx, public_file_org_links.get_public_file_org_link(ctx, **kwargs).to_dict()
    )


@click.command(name="delete-public-file-org-link")
@click.option("--public-file-org-link-id", required=True)
@click.option("--link-org-id", required=True)
@click.pass_context
def cli_command_delete_public_file_org_link(ctx, **kwargs):
    public_file_org_links.delete_public_file_org_link(ctx, **kwargs)


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
