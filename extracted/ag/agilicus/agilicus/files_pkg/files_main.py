import os.path
import sys
import click
import shutil
import zipfile

from . import file_templates
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


@click.command(name="add-file-template")
@click.option("--parameter", multiple=True, help="the parameters the template will use")
@click.option("--content-type", required=True)
@click.option("--purpose", default="")
@click.option("--descriptive-text", default="")
@click.option("--rendered-file-name", required=True)
@click.option(
    "--file-to-upload",
    type=str,
    default=None,
    help="path to the template file to upload",
)
@click.option("--delimiter", default=None)
@click.option(
    "--default-argument", multiple=True, type=click.Tuple([str, str]), default=None
)
@click.option(
    "--associated-object", multiple=True, type=click.Tuple([str, str, str]), default=None
)
@click.pass_context
def cli_command_add_file_template(
    ctx, parameter, default_argument, associated_object, **kwargs
):
    output_entry(
        ctx,
        file_templates.add_file_template(
            ctx,
            parameters=parameter,
            default_arguments=default_argument,
            associated_objects=associated_object,
            **kwargs,
        ),
    )


@click.command(name="replace-file-template")
@click.option("--file-template-id", required=True)
@click.option("--parameter", multiple=True, help="the parameters the template will use")
@click.option("--content-type")
@click.option("--purpose", default="")
@click.option("--descriptive-text", default="")
@click.option("--rendered-file-name")
@click.option("--template-file", type=str, default=None, help="template file id")
@click.option("--delimiter", default=None)
@click.option(
    "--default-argument", multiple=True, type=click.Tuple([str, str]), default=None
)
@click.option(
    "--associated-object", multiple=True, type=click.Tuple([str, str, str]), default=None
)
@click.option(
    "--clear-associated-object",
    multiple=True,
    type=click.Tuple([str, str, str]),
    default=None,
)
@click.pass_context
def cli_command_replace_file_template(
    ctx, parameter, default_argument, associated_object, **kwargs
):
    output_entry(
        ctx,
        file_templates.replace_file_template(
            ctx,
            parameters=parameter,
            default_arguments=default_argument,
            associated_objects=associated_object,
            **kwargs,
        ),
    )


@click.command(name="list-file-templates")
@click.option("--org-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--limit", default=None)
@click.option("--purpose", default=None)
@click.option("--object-type", multiple=True, default=None)
@click.option("--object-id", multiple=True, default=None)
@click.pass_context
def cli_command_list_file_templates(ctx, object_id=None, object_type=None, **kwargs):
    result = file_templates.list_file_templates(
        ctx, object_ids=object_id, object_types=object_type, **kwargs
    )
    print(file_templates.format_file_templates(ctx, result))


@click.command(name="get-file-template")
@click.option("--file-template-id", required=True)
@click.option("--org-id")
@click.pass_context
def cli_command_get_file_template(ctx, **kwargs):
    output_entry(ctx, file_templates.get_file_template(ctx, **kwargs).to_dict())


@click.command(name="delete-file-template")
@click.option("--file-template-id", required=True)
@click.option("--org-id")
@click.pass_context
def cli_command_delete_file_template(ctx, **kwargs):
    file_templates.delete_file_template(ctx, **kwargs)


@click.command(name="render-file-template")
@click.option("--file-template-id", required=True)
@click.option("--include-user", is_flag=True)
@click.option("--user-id")
@click.option("--resource-id")
@click.option(
    "--template-argument", multiple=True, type=click.Tuple([str, str]), default=None
)
@click.option(
    "--outfile", type=click.File("wb"), default=None, help="defaults to stdout"
)
@click.option("--org-id")
@click.option("--compressed", is_flag=True)
@click.pass_context
def cli_command_render_file_template(
    ctx, template_argument, outfile, compressed, **kwargs
):
    result = file_templates.render_file_template(
        ctx, template_arguments=template_argument, **kwargs
    )
    if outfile is None:
        outfile = sys.stdout.buffer
    if compressed:
        outfile = zipfile.ZipFile(outfile, "w", zipfile.ZIP_DEFLATED)
        outfile.writestr(os.path.basename(result.name), result.read())
        outfile.close()
        return

    shutil.copyfileobj(result, outfile)


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
