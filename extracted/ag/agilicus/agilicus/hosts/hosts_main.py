import click
from ..output.table import output_entry
from . import hosts


@click.command(name="add-host")
@click.argument("hostname")
@click.option("--org-id", default=None)
@click.option("--port", default=None)
@click.option("--path", default=None)
@click.option("--label", type=str, multiple=True)
@click.pass_context
def cli_command_add_host(ctx, *args, label, **kwargs):
    result = hosts.add_host(
        ctx,
        *args,
        labels=list(label),
        **kwargs,
    )
    output_entry(ctx, result.to_dict())


@click.command(name="show-host")
@click.argument("host-id")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_show_host(ctx, **kwargs):
    result = hosts.get_host(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="delete-host")
@click.argument("host-id")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_host(ctx, *args, **kwargs):
    hosts.delete_host(ctx, *args, **kwargs)


@click.command(name="add-host-label")
@click.argument("label", nargs=-1)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_host_label(ctx, label, **kwargs):
    for _label in label:
        result = hosts.add_label(ctx, label=_label, **kwargs)
        output_entry(ctx, result.to_dict())


@click.command(name="list-host-labels")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_list_host_labels(ctx, **kwargs):
    results = hosts.list_labels(ctx, **kwargs)
    print(hosts.format_labels(ctx, results))


@click.command(name="list-host-orgs")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_list_hosts_orgs(ctx, **kwargs):
    results = hosts.list_orgs(ctx, **kwargs)
    print(hosts.format_orgs(ctx, results))


@click.command(name="list-hosts")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_list_hosts(ctx, **kwargs):
    results = hosts.list_hosts(ctx, **kwargs)
    print(hosts.format_hosts_as_text(ctx, results))


@click.command(name="add-host-bundle")
@click.argument("bundle")
@click.option("--org-id", default=None)
@click.option("--label", default=None)
@click.option("--label-org-id", default=None)
@click.option("--exclude", is_flag=True, default=None)
@click.pass_context
def cli_command_add_hosts_bundle(ctx, **kwargs):
    result = hosts.add_bundle(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="add-host-bundle-label")
@click.argument("bundle-id")
@click.argument("label")
@click.option("--label-org-id", default=None)
@click.option("--exclude", is_flag=True, default=None)
@click.pass_context
def cli_command_add_hosts_bundle_label(ctx, **kwargs):
    result = hosts.add_bundle_label(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="delete-host-bundle")
@click.argument("bundle-id", nargs=-1)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_hosts_bundle(ctx, bundle_id, **kwargs):
    for _bundle_id in bundle_id:
        hosts.delete_bundle(ctx, bundle_id=_bundle_id, **kwargs)


@click.command(name="list-host-bundles")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_list_hosts_bundle(ctx, **kwargs):
    results = hosts.list_bundles(ctx, **kwargs)
    print(hosts.format_bundles(ctx, results))


@click.command(name="get-host-bundle")
@click.argument("bundle-id")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_get_hosts_bundle(ctx, **kwargs):
    result = hosts.get_bundle(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
