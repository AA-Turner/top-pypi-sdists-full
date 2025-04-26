import json

import click
import click_extension

from .. import context
from . import rules
from ..output.table import output_entry


@click.command(name="add-host-prefix-rule")
@click.option("--hostname", required=True)
@click.option("--name", required=True)
@click.option("--action", required=True, multiple=True, type=click.Choice(rules.ACTIONS))
@click.option("--prefix", default=None)
@click.option("--purpose", default=None)
@click.option("--org-id", default=None)
@click.option("--standalone-rule-policy-id", default=None)
@click.pass_context
def cli_command_add_host_prefix_rule(ctx, action, **kwargs):
    output_entry(ctx, rules.add_hostprefix_rule(ctx, actions=action, **kwargs))


@click.command(name="add-mfa-proof-rule")
@click.option("--name", required=True)
@click.option("--max-seconds", required=True, type=int)
@click.option("--org-id", default=None)
@click.option("--purpose", default=None)
@click.option("--action", required=True, multiple=True, type=click.Choice(rules.ACTIONS))
@click.option("--standalone-rule-policy-id", default=None)
@click.pass_context
def cli_command_add_mfa_proof_rule(ctx, action, **kwargs):
    output_entry(ctx, rules.add_mfa_proof_rule(ctx, actions=action, **kwargs))


@click.command(name="add-standalone-rules-from-file")
@click.option("--rule-json-file", required=True, type=click_extension.JSONFile("r"))
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_rules_from_file(ctx, rule_json_file, **kwargs):
    print(rules.add_rules(ctx, rules=rule_json_file, **kwargs))


@click.command(name="list-standalone-rules")
@click.option("--name", default=None)
@click.option("--prefix", default=None)
@click.option("--org-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--rule-id", default=None)
@click.option("--standalone-rule-policy-id", multiple=True, default=None)
@click.pass_context
def cli_command_list_rules(ctx, **kwargs):
    result = rules.list_rules(ctx, **kwargs)
    print(rules.format_rules(ctx, result))


@click.command(name="get-standalone-rule")
@click.option("--rule-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_get_rule(ctx, **kwargs):
    output_entry(ctx, rules.get_rule(ctx, **kwargs).to_dict())


@click.command(name="delete-standalone-rule")
@click.option("--rule-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_rule(ctx, **kwargs):
    rules.delete_rule(ctx, **kwargs)


@click.command(name="update-host-prefix-rule")
@click.option("--rule-id", required=True)
@click.option("--hostname", default=None)
@click.option("--name", default=None)
@click.option("--action", default=None, multiple=True, type=click.Choice(rules.ACTIONS))
@click.option("--prefix", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_replace_host_prefix_rule(ctx, action, **kwargs):
    output_entry(
        ctx, rules.replace_hostprefix_rule(ctx, actions=action, **kwargs).to_dict()
    )


@click.command(name="add-standalone-rule-tree")
@click.option("--name", required=True)
@click.option("--rule-name", default=None, multiple=True)
@click.option("--child-tree-name", default=None, multiple=True)
@click.option("--description", default=None)
@click.option("--org-id", default=None)
@click.option("--scope", default=None, multiple=True)
@click.option("--standalone-rule-policy-id", default=None)
@click.pass_context
def cli_command_add_rule_tree(ctx, rule_name, child_tree_name, scope, **kwargs):
    if len(rule_name) == 0 and len(child_tree_name) == 0:
        raise ValueError("must provide at least one tree-name or child-tree-name")
    output_entry(
        ctx,
        rules.add_rule_tree(
            ctx, rules=rule_name, children=child_tree_name, scopes=scope, **kwargs
        ),
    )


@click.command(name="add-standalone-rule-trees-from-file")
@click.option("--rule-tree-json-file", required=True, type=click_extension.JSONFile("r"))
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_rule_trees_from_file(ctx, rule_tree_json_file, **kwargs):
    print(rules.add_trees(ctx, trees=rule_tree_json_file, **kwargs))


@click.command(name="list-standalone-rule-trees")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--rule-tree-id", default=None)
@click.option("--standalone-rule-policy-id", multiple=True, default=None)
@click.pass_context
def cli_command_list_rule_trees(ctx, **kwargs):
    result = rules.list_rule_trees(ctx, **kwargs)
    print(rules.format_rule_trees(ctx, result))


@click.command(name="get-standalone-rule-tree")
@click.option("--rule-tree-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_get_rule_tree(ctx, **kwargs):
    output_entry(ctx, rules.get_rule_tree(ctx, **kwargs).to_dict())


@click.command(name="update-standalone-rule-tree")
@click.option("--rule-tree-id", required=True)
@click.option("--name", default=None)
@click.option("--rule-name", default=None, multiple=True)
@click.option("--child-tree-name", default=None, multiple=True)
@click.option("--description", default=None)
@click.option("--org-id", default=None)
@click.option("--scope", default=None, multiple=True)
@click.option("--standalone-rule-policy-id", default=None)
@click.pass_context
def cli_command_update_rule_tree(ctx, rule_name, child_tree_name, scope, **kwargs):
    output_entry(
        ctx,
        rules.replace_rule_tree(
            ctx, rules=rule_name, children=child_tree_name, scopes=scope, **kwargs
        ),
    )


@click.command(name="delete-standalone-rule-tree")
@click.option("--rule-tree-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_rule_tree(ctx, **kwargs):
    rules.delete_rule_tree(ctx, **kwargs)


@click.command(name="add-standalone-ruleset")
@click.option("--name", required=True)
@click.option("--tree-name", default=None, multiple=True)
@click.option("--label", default=None, multiple=True)
@click.option("--org-id", default=None)
@click.option("--scope", default=None, multiple=True)
@click.option("--standalone-rule-policy-id", default=None)
@click.pass_context
def cli_command_add_ruleset(ctx, tree_name, label, scope, **kwargs):
    output_entry(
        ctx,
        rules.add_ruleset(ctx, trees=tree_name, labels=label, scopes=scope, **kwargs),
    )


@click.command(name="add-standalone-rulesets-from-file")
@click.option("--ruleset-json-file", required=True, type=click_extension.JSONFile("r"))
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_rulesets_from_file(ctx, ruleset_json_file, **kwargs):
    print(rules.add_rulesets(ctx, rulesets=ruleset_json_file, **kwargs))


@click.command(name="list-standalone-rulesets")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--standalone-rule-policy-id", multiple=True, default=None)
@click.pass_context
def cli_command_list_rulesets(ctx, **kwargs):
    result = rules.list_rulesets(ctx, **kwargs)
    print(rules.format_rulesets(ctx, result))


@click.command(name="get-standalone-ruleset")
@click.option("--ruleset-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_get_ruleset(ctx, **kwargs):
    output_entry(ctx, rules.get_ruleset(ctx, **kwargs).to_dict())


@click.command(name="update-standalone-ruleset")
@click.option("--ruleset-id", required=True)
@click.option("--name", default=None)
@click.option("--tree-name", default=None, multiple=True)
@click.option("--label", default=None, multiple=True)
@click.option("--org-id", default=None)
@click.option("--scope", default=None, multiple=True)
@click.option("--standalone-rule-policy-id", default=None)
@click.pass_context
def cli_command_update_ruleset(ctx, tree_name, label, scope, **kwargs):
    output_entry(
        ctx,
        rules.replace_ruleset(
            ctx, trees=tree_name, labels=label, scopes=scope, **kwargs
        ),
    )


@click.command(name="delete-standalone-ruleset")
@click.option("--ruleset-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_ruleset(ctx, **kwargs):
    rules.delete_ruleset(ctx, **kwargs)


@click.command(name="add-standalone-ruleset-label")
@click.argument("label", nargs=-1)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_host_label(ctx, label, **kwargs):
    for _label in label:
        result = rules.add_label(ctx, label=_label, **kwargs)
        output_entry(ctx, result.to_dict())


@click.command(name="list-standalone-ruleset-labels")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_list_ruleset_labels(ctx, **kwargs):
    results = rules.list_labels(ctx, **kwargs)
    print(rules.format_labels(ctx, results))


@click.command(name="add-standalone-ruleset-bundle")
@click.option("--name", required=True)
@click.option("--org-id", default=None)
@click.option("--label", default=None)
@click.option("--label-org-id", default=None)
@click.option("--exclude", is_flag=True, default=None)
@click.pass_context
def cli_command_add_rulesets_bundle(ctx, **kwargs):
    result = rules.add_bundle(ctx, **kwargs)
    output_entry(ctx, result)


@click.command(name="add-standalone-ruleset-bundle-label")
@click.argument("bundle-id")
@click.argument("label")
@click.option("--label-org-id", default=None)
@click.option("--exclude", is_flag=True, default=None)
@click.option("--priority", type=int, default=0)
@click.pass_context
def cli_command_add_rulesets_bundle_label(ctx, **kwargs):
    result = rules.add_bundle_label(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="delete-standalone-ruleset-bundle-label")
@click.argument("bundle-id")
@click.argument("label")
@click.option("--label-org-id", default=None)
@click.pass_context
def cli_command_delete_rulesets_bundle_label(ctx, **kwargs):
    result = rules.delete_bundle_label(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="delete-standalone-ruleset-bundle")
@click.argument("bundle-id", nargs=-1)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_rulesets_bundle(ctx, bundle_id, **kwargs):
    for _bundle_id in bundle_id:
        rules.delete_bundle(ctx, bundle_id=_bundle_id, **kwargs)


@click.command(name="list-standalone-ruleset-bundles")
@click.option("--org-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--get-rulesets", is_flag=True, default=None)
@click.option("--standalone-ruleset-bundles-etag", default=None)
@click.option("--limit", default=None, type=int)
@click.pass_context
def cli_command_list_rulesets_bundle(ctx, **kwargs):
    results = rules.list_bundles(ctx, **kwargs)
    if context.output_console(ctx):
        print(rules.format_bundles(ctx, results.standalone_ruleset_bundles))
        return
    output_entry(ctx, results.to_dict())


@click.command(name="get-standalone-ruleset-bundle")
@click.argument("bundle-id")
@click.option("--org-id", default=None)
@click.option("--get-rulesets", is_flag=True, default=None)
@click.option("--standalone-rulesets-etag", default=None)
@click.pass_context
def cli_command_get_rulesets_bundle(ctx, **kwargs):
    result = rules.get_bundle(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="add-standalone-rule-policy")
@click.option("--object-type", default="")
@click.option("--object-id", default="")
@click.option("--policy-class", default="")
@click.option("--policy-instance", default="")
@click.option("--description", default=None)
@click.option("--annotations-json", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_rule_policy(ctx, annotations_json, **kwargs):
    annotations = None
    if annotations_json is not None:
        annotations = json.loads(annotations_json)
    output_entry(
        ctx,
        rules.add_rule_policy(ctx, annotations=annotations, **kwargs).to_dict(),
    )


@click.command(name="list-standalone-rule-policies")
@click.option("--org-id", default=None)
@click.option("--object-type")
@click.option("--object-id")
@click.option("--policy-class", multiple=True)
@click.option("--policy-instance")
@click.pass_context
def cli_command_list_rule_policies(ctx, **kwargs):
    result = rules.list_rule_policies(ctx, **kwargs)
    print(rules.format_rule_policies(ctx, result))


@click.command(name="get-standalone-rule-policy")
@click.option("--policy-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_get_rule_policy(ctx, **kwargs):
    output_entry(ctx, rules.get_rule_policy(ctx, **kwargs).to_dict())


@click.command(name="update-standalone-rule-policy")
@click.option("--policy-id", required=True)
@click.option("--object-type")
@click.option("--object-id")
@click.option("--policy-class")
@click.option("--policy-instance")
@click.option("--description", default=None)
@click.option("--annotations-json", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_update_rule_policy(ctx, annotations_json, **kwargs):
    annotations = None
    if annotations_json is not None:
        annotations = json.loads(annotations_json)
    output_entry(
        ctx,
        rules.replace_rule_policy(ctx, annotations=annotations, **kwargs).to_dict(),
    )


@click.command(name="delete-standalone-rule-policy")
@click.option("--policy-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_rule_policy(ctx, **kwargs):
    rules.delete_rule_policy(ctx, **kwargs)


@click.command(name="add-agilicus-default-expose-allow")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_agilicus_default_expose_allow(ctx, **kwargs):
    rules.add_agilicus_default_expose_allow(ctx, **kwargs)


@click.command(name="add-scope-condition-rule")
@click.option("--name", required=True)
@click.option("--action", required=True, multiple=True, type=click.Choice(rules.ACTIONS))
@click.option("--purpose", default=None)
@click.option("--org-id", default=None)
@click.option("--standalone-rule-policy-id", default=None)
@click.option("--scope", default=None, multiple=True)
@click.pass_context
def cli_command_add_scope_condition_rule(ctx, action, scope, **kwargs):
    output_entry(
        ctx, rules.add_scope_condition_rule(ctx, actions=action, scopes=scope, **kwargs)
    )


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
