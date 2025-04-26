import click

from . import labels
from .. import resources
from ..output.table import output_entry


@click.command(name="add-label")
@click.option("--name", required=True)
@click.option("--description", default=None)
@click.option("--org-id", default=None)
@click.option("--navigation-enabled", type=bool, default=None)
@click.pass_context
def cli_command_add_label(ctx, **kwargs):
    output_entry(ctx, labels.add_label(ctx, **kwargs))


@click.command(name="list-labels")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--navigation-enabled", type=bool, default=None)
@click.pass_context
def cli_command_list_labels(ctx, **kwargs):
    result = labels.list_labels(ctx, **kwargs)
    print(labels.format_labels(ctx, result))


@click.command(name="get-label")
@click.option("--label-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_get_label(ctx, **kwargs):
    output_entry(ctx, labels.get_label(ctx, **kwargs).to_dict())


@click.command(name="delete-label")
@click.option("--label-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_label(ctx, **kwargs):
    labels.delete_label(ctx, **kwargs)


@click.command(name="update-label")
@click.option("--label-id", required=True)
@click.option("--name", default=None)
@click.option("--description", default=None)
@click.option("--org-id", default=None)
@click.option("--navigation-enabled", type=bool, default=None)
@click.pass_context
def cli_command_replace_label(ctx, **kwargs):
    output_entry(ctx, labels.replace_label(ctx, **kwargs).to_dict())


@click.command(name="add-label-icon", help="Add an icon to a label")
@click.option("--label-id", required=True)
@click.option("--org-id", default=None)
@click.option("--uri", required=True)
@click.option("--purpose", multiple=True, default=None)
@click.option("--height-px", type=int, default=None)
@click.option("--width-px", type=int, default=None)
@click.pass_context
def cli_command_add_display_info_icon(ctx, **kwargs):
    result = labels.add_display_info_icon(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="delete-label-icon")
@click.option("--label-id", required=True)
@click.option("--org-id", default=None)
@click.option("--uri", required=True)
@click.pass_context
def cli_command_delete_display_info_icon(ctx, **kwargs):
    result = labels.delete_display_info_icon(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="add-labelled-object")
@click.option("--object-id", required=True)
@click.option("--object-type", required=True)
@click.option("--org-id", default=None)
@click.option("--label", multiple=True, default=None)
@click.pass_context
def cli_command_add_labelled_object(ctx, **kwargs):
    output_entry(ctx, labels.add_labelled_object(ctx, **kwargs))


@click.command(name="list-labelled-objects")
@click.option("--org-id", default=None)
@click.option("--object-id", default=None)
@click.option("--object-type", default=None)
@click.option("--includes-any-label", multiple=True, default=None)
@click.option("--excludes-any-label", multiple=True, default=None)
@click.option("--page-at-id", default=None)
@click.option("--limit", type=int, default=None)
@click.pass_context
def cli_command_list_labelled_objects(ctx, **kwargs):
    result = labels.list_labelled_objects(ctx, **kwargs)
    print(labels.format_labelled_objects(ctx, result))


@click.command(name="get-labelled-object")
@click.option("--object-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_get_labelled_object(ctx, **kwargs):
    output_entry(ctx, labels.get_labelled_object(ctx, **kwargs).to_dict())


@click.command(name="delete-labelled-object")
@click.option("--object-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_labelled_object(ctx, **kwargs):
    labels.delete_labelled_object(ctx, **kwargs)


@click.command(name="update-labelled-object")
@click.option("--object-id", required=True)
@click.option("--org-id", default=None)
@click.option("--label", multiple=True, default=None)
@click.pass_context
def cli_command_replace_labelled_object(ctx, **kwargs):
    output_entry(ctx, labels.replace_labelled_object(ctx, **kwargs).to_dict())


@click.command(name="add-labelled-object-label")
@click.option("--object-id", required=True)
@click.option("--label", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_labelled_object_label(ctx, **kwargs):
    output_entry(ctx, labels.add_labelled_object_label(ctx, **kwargs).to_dict())


@click.command(name="delete-labelled-object-label")
@click.option("--object-id", required=True)
@click.option("--label", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_labelled_object_label(ctx, **kwargs):
    labels.delete_labelled_object_label(ctx, **kwargs)


@click.command(name="add-labels-to-resources")
@click.option("--label", multiple=True, required=True)
@click.option("--resource-name", default=None)
@click.option(
    "--resource-type",
    default=None,
    type=resources.resource_type_enum,
)
@click.option(
    "--exclude-resource-type",
    default=None,
    multiple=True,
    type=resources.resource_type_enum,
)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_labels_to_resources(ctx, **kwargs):
    labels.add_labels_to_resources(ctx, **kwargs)


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
