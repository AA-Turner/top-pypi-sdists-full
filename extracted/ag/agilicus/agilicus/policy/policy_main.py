import click
import click_extension

from . import policies
from ..output.table import output_entry


@click.command(name="set-multifactor-policy")
@click.option("--name", required=True)
@click.option("--label", multiple=True, type=str)
@click.option("--duration", required=True, type=int)
@click.option("--description", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_set_multifactor_policy(ctx, **kwargs):
    output_entry(ctx, policies.set_multifactor_policy(ctx, **kwargs).to_dict())


@click.command(name="set-source-info-policy")
@click.option("--name", required=True)
@click.option("--action", type=click.Choice(["allow", "deny"]), required=True)
@click.option("--label", multiple=True, type=str)
@click.option("--description", default=None)
@click.option("--org-id", default=None)
@click.option("--source-subnet", multiple=True, type=str)
@click.option("--iso-country-code", multiple=True, type=str)
@click.option("--log-message", default=None)
@click.option("--invert", type=bool, default=False)
@click.pass_context
def cli_command_set_source_info_policy(ctx, **kwargs):
    output_entry(ctx, policies.set_source_info_policy(ctx, **kwargs).to_dict())


@click.command(name="list-multifactor-policies")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_list_multifactor_policies(ctx, **kwargs):
    results = policies.list_multifactor_policies(ctx, **kwargs)
    print(policies.format_multifactor_policies(ctx, results))


@click.command(name="list-policy-templates", help="shows all policy templates")
@click.option("--org-id", default=None)
@click.option("--template-type", default=None)
@click.option("--include-invalid", type=bool, default=None)
@click.option("--object-id", type=str, default=None)
@click.option("--name", default=None)
@click.pass_context
def cli_command_list_policy_templates(ctx, **kwargs):
    results = policies.list_policy_templates(ctx, **kwargs)
    print(policies.format_policy_templates(ctx, results))


@click.command(name="get-policy-template")
@click.option("--instance-id", default=None, required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_get_policy_template(ctx, **kwargs):
    output_entry(ctx, policies.get_policy_template(ctx, **kwargs).to_dict())


@click.command(name="create-policy-template")
@click.option("--template-json-file", required=True, type=click_extension.JSONFile("r"))
@click.pass_context
def cli_command_create_policy_template(ctx, template_json_file, **kwargs):
    output_entry(
        ctx,
        policies.create_policy_template(
            ctx, template_dict=template_json_file, **kwargs
        ).to_dict(),
    )


@click.command(name="replace-policy-template")
@click.option("--instance-id", required=True, type=str)
@click.option("--template-json-file", required=True, type=click_extension.JSONFile("r"))
@click.pass_context
def cli_command_replace_policy_template(ctx, template_json_file, **kwargs):
    output_entry(
        ctx,
        policies.replace_policy_template(
            ctx, template_dict=template_json_file, **kwargs
        ).to_dict(),
    )


@click.command(name="kick-policy-template")
@click.option("--instance-id", required=True, type=str)
@click.option("--org-id", type=str)
@click.pass_context
def cli_command_kick_policy_template(ctx, **kwargs):
    output_entry(
        ctx,
        policies.kick_policy_template(ctx, **kwargs).to_dict(),
    )


@click.command(name="delete-policy-template")
@click.option("--instance-id", default=None, required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_policy_template(ctx, **kwargs):
    policies.delete_policy_template(ctx, **kwargs)


@click.command(name="migrate-policy-rules")
@click.option("--org-id", default=None)
@click.option("--resource-id", default=None)
@click.option("--dump-dir", default=None, help="A directory to cache migrated rules")
@click.pass_context
def cli_command_migrate_policy_rules(ctx, **kwargs):
    policies.migrate_policy_rules(ctx, **kwargs)


@click.command(name="fetch-resource-rules")
@click.option("--org-id", default=None)
@click.option("--resource-id", default=None)
@click.option("--dump-dir", default=None, help="A directory to cache rules")
@click.pass_context
def cli_command_fetch_resource_rules(ctx, **kwargs):
    policies.fetch_resource_rules(ctx, **kwargs)


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
