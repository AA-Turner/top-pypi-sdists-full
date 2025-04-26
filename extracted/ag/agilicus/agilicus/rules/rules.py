from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .. import context
from ..input_helpers import (
    get_org_from_input_or_ctx,
    strip_none,
    build_updated_model_validate,
    model_from_dict,
)
import agilicus
from ..output.table import (
    spec_column,
    format_table,
    metadata_column,
    subtable,
    column,
)

from agilicus import create_or_update, find_guid

ACTIONS = ["allow", "deny", "redirect", "log", "none", "revocation_check", "mfa"]

ConditionTypes = Enum(
    "ConditionType",
    [
        "host_prefix_rule_condition",
        "mfa_rule_condition",
        "scope_condition",
        "network_protocol_condition",
    ],
)


def add_hostprefix_rule(
    ctx,
    hostname,
    name,
    actions,
    prefix=None,
    purpose=None,
    standalone_rule_policy_id=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs = strip_none(kwargs)

    cond = agilicus.HostPrefixRuleCondition(
        condition_type=ConditionTypes.host_prefix_rule_condition.name, host=hostname
    )
    extended_cond = agilicus.RuleCondition(condition=cond, negated=False)

    if prefix is not None:
        cond.prefix = prefix

    rule = agilicus.RuleConfig(
        name=name,
        extended_condition=extended_cond,
        actions=[agilicus.RuleAction(action=action) for action in actions],
    )

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    spec = agilicus.StandaloneRuleSpec(org_id=org_id, rule=rule)
    if purpose is not None:
        spec.purpose = purpose

    if standalone_rule_policy_id is not None:
        spec.standalone_rule_policy_id = standalone_rule_policy_id
    req = agilicus.StandaloneRule(spec=spec)
    result, _ = create_or_update(
        req,
        lambda obj: apiclient.rules_api.create_standalone_rule(obj),
        lambda guid, obj: apiclient.rules_api.replace_standalone_rule(
            guid, standalone_rule=obj
        ),
    )
    return result


def add_mfa_proof_rule(
    ctx,
    name,
    max_seconds,
    actions,
    purpose=None,
    standalone_rule_policy_id=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs = strip_none(kwargs)

    cond = agilicus.MaxMFAProofRuleCondition(
        condition_type=ConditionTypes.mfa_rule_condition.name, max_seconds=max_seconds
    )
    extended_cond = agilicus.RuleCondition(condition=cond, negated=False)

    rule = agilicus.RuleConfig(
        name=name,
        extended_condition=extended_cond,
        actions=[agilicus.RuleAction(action=action) for action in actions],
    )

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    spec = agilicus.StandaloneRuleSpec(org_id=org_id, rule=rule)
    if purpose is not None:
        spec.purpose = purpose
    if standalone_rule_policy_id is not None:
        spec.standalone_rule_policy_id = standalone_rule_policy_id
    req = agilicus.StandaloneRule(spec=spec)
    result, _ = create_or_update(
        req,
        lambda obj: apiclient.rules_api.create_standalone_rule(obj),
        lambda guid, obj: apiclient.rules_api.replace_standalone_rule(
            guid, standalone_rule=obj
        ),
    )
    return result


@dataclass
class AddResult:
    result_name: str
    result_id: Optional[str] = None
    exc: Optional[str] = None


def _obj_from_dict(klass, obj_dict, org_id):
    old_org_id = obj_dict["spec"]["org_id"]
    if old_org_id:
        org_id = old_org_id

    obj_dict["spec"]["org_id"] = org_id
    return model_from_dict(klass, obj_dict)


class AddInfo:
    def __init__(self):
        super().__init__()
        self.name_getter = name_in_spec
        self.guid_finder = find_guid


def name_in_spec(obj):
    return obj.spec.name


class RuleAddInfo(AddInfo):
    def __init__(self, apiclient):
        super().__init__()
        self.create_fn = lambda obj: apiclient.rules_api.create_standalone_rule(obj)
        self.replace_fn = lambda guid, obj: apiclient.rules_api.replace_standalone_rule(
            guid, standalone_rule=obj
        )
        self.name_getter = lambda obj: obj.spec.rule.name


class RuleTreeAddInfo(AddInfo):
    def __init__(self, apiclient):
        super().__init__()
        self.create_fn = lambda obj: apiclient.rules_api.create_standalone_rule_tree(obj)
        self.replace_fn = (
            lambda guid, obj: apiclient.rules_api.replace_standalone_rule_tree(
                guid, standalone_rule_tree=obj
            )
        )


class RulesetAddInfo(AddInfo):
    def __init__(self, apiclient):
        super().__init__()
        self.create_fn = lambda obj: apiclient.rules_api.create_standalone_ruleset(obj)
        self.replace_fn = (
            lambda guid, obj: apiclient.rules_api.replace_standalone_ruleset(
                guid, standalone_ruleset=obj
            )
        )


def add_list_of_resouces(ctx, as_dicts, klass, add_info, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    objs = [_obj_from_dict(klass, obj, org_id) for obj in as_dicts]

    return add_list_resources_sdk(ctx, objs, add_info)


def add_list_resources_sdk(ctx, objs, add_info, handle_failure=True):
    results = []
    for obj in objs:
        try:
            result, _ = create_or_update(
                obj,
                add_info.create_fn,
                add_info.replace_fn,
                to_dict=False,
                guid_finder=add_info.guid_finder,
            )
            results.append(
                AddResult(
                    result_name=add_info.name_getter(result),
                    result_id=add_info.guid_finder(result),
                )
            )
        except Exception as exc:
            if not handle_failure:
                raise

            results.append(
                AddResult(
                    result_name=add_info.name_getter(obj),
                    exc=str(exc),
                )
            )

    columns = [column("result_name", "name"), column("result_id", "id"), column("exc")]

    return format_table(ctx, results, columns)


def add_rules(ctx, rules, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return add_list_of_resouces(
        ctx,
        rules,
        agilicus.StandaloneRule,
        RuleAddInfo(apiclient),
    )


def replace_hostprefix_rule(
    ctx, rule_id, org_id, name=None, hostname=None, prefix=None, actions=None, **kwargs
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    base = apiclient.rules_api.get_standalone_rule(rule_id=rule_id, org_id=org_id)
    spec = base.spec
    rule = spec.rule

    cond = rule.extended_condition.condition
    if cond.condition_type != ConditionTypes.host_prefix_rule_condition.name:
        raise ValueError(f"existing rule has condition type {cond.condition_type}")

    if actions is not None and len(actions) > 0:
        actions = list(actions)

    new_values = {
        "prefix": prefix,
        "host": hostname,
        "actions": actions,
    }
    rule.extended_condition.condition = build_updated_model_validate(
        agilicus.StandaloneRulesetPrefixRuleCondition, cond, new_values
    )

    if name is not None:
        rule.name = name

    return apiclient.rules_api.replace_standalone_rule(
        base.metadata.id, standalone_rule=base
    )


def get_rule(ctx, rule_id, org_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    return apiclient.rules_api.get_standalone_rule(rule_id=rule_id, org_id=org_id)


def delete_rule(ctx, rule_id, org_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    return apiclient.rules_api.delete_standalone_rule(rule_id=rule_id, org_id=org_id)


def list_rules(ctx, standalone_rule_policy_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["standalone_rule_policy_ids"] = standalone_rule_policy_id
    kwargs = strip_none(kwargs)

    rules_resp = apiclient.rules_api.list_standalone_rules(**kwargs)
    return rules_resp.standalone_rules


def format_rules(ctx, rules):
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("rule.name", "name"),
        spec_column("rule.extended_condition.condition", "condition"),
        spec_column("rule.extended_condition.negated", "negated"),
        spec_column("rule.actions", "actions"),
    ]

    return format_table(ctx, rules, columns)


def _rule_ref_from_name(name):
    return agilicus.StandaloneRuleTreeRuleRef(
        rule_name=agilicus.StandaloneRuleName(name)
    )


def _rules_list_from_rules(rules):
    return [_rule_ref_from_name(rule) for rule in rules]


def _child_tree_from_children(children):
    child_nodes = []
    for idx, child in enumerate(children):
        node = agilicus.StandaloneRuleTreeNode(
            children=[], rules=_rules_list_from_rules([child])
        )
        child_node = agilicus.StandaloneRuleTreeNodeChild(
            node=node,
            priority=len(children) - idx,
        )
        child_nodes.append(child_node)
    return child_nodes


def add_rule_tree(
    ctx, name, rules, children, org_id=None, description=None, scopes=None, **kwargs
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)

    root = agilicus.StandaloneRuleTreeNode(
        children=_child_tree_from_children(children),
        rules=_rules_list_from_rules(rules),
    )

    kwargs = strip_none(kwargs)

    spec = agilicus.StandaloneRuleTreeSpec(
        tree=root, org_id=org_id, name=agilicus.StandaloneRuleName(name), **kwargs
    )

    _add_object_conditions(spec, scopes)

    if description is not None:
        spec.description = description

    req = agilicus.StandaloneRuleTree(spec=spec)
    result, _ = create_or_update(
        req,
        lambda obj: apiclient.rules_api.create_standalone_rule_tree(obj),
        lambda guid, obj: apiclient.rules_api.replace_standalone_rule_tree(
            guid, standalone_rule_tree=obj
        ),
    )
    return result


def add_trees(ctx, trees, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return add_list_of_resouces(
        ctx,
        trees,
        agilicus.StandaloneRuleTree,
        RuleTreeAddInfo(apiclient),
    )


def get_rule_tree(ctx, rule_tree_id, org_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.rules_api.get_standalone_rule_tree(
        standalone_rule_tree_id=rule_tree_id, org_id=org_id
    )


def delete_rule_tree(ctx, rule_tree_id, org_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    return apiclient.rules_api.delete_standalone_rule_tree(
        standalone_rule_tree_id=rule_tree_id, org_id=org_id
    )


def list_rule_trees(ctx, standalone_rule_policy_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["standalone_rule_policy_ids"] = standalone_rule_policy_id
    kwargs = strip_none(kwargs)

    rules_resp = apiclient.rules_api.list_standalone_rule_trees(**kwargs)
    return rules_resp.standalone_rule_trees


def replace_rule_tree(
    ctx,
    rule_tree_id,
    org_id,
    name=None,
    rules=None,
    children=None,
    description=None,
    scopes=None,
    standalone_rule_policy_id=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    base = apiclient.rules_api.get_standalone_rule_tree(
        standalone_rule_tree_id=rule_tree_id, org_id=org_id
    )
    spec = base.spec
    if rules is not None:
        spec.tree.rule = _rules_list_from_rules(rules)

    if children is not None:
        spec.tree.children = _child_tree_from_children(children)

    if name is not None:
        spec.name = name

    if description is not None:
        spec.description = description

    if standalone_rule_policy_id is not None:
        spec.standalone_rule_policy_id = standalone_rule_policy_id

    _add_object_conditions(spec, scopes)

    return apiclient.rules_api.replace_standalone_rule_tree(
        base.metadata.id, standalone_rule_tree=base
    ).to_dict()


def format_rule_trees(ctx, rule_trees):
    rules_table = [column("rule_name", "name")]
    child_columns = [column("priority"), column("node", "child")]
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("name"),
        spec_column("object_conditions"),
        subtable(ctx, "spec.tree.rules", rules_table, out_name="rules"),
        subtable(ctx, "spec.tree.children", child_columns, out_name="children"),
    ]

    return format_table(ctx, rule_trees, columns)


def _rule_tree_ref_list(trees):
    tree_refs = []
    for idx, tree in enumerate(trees):
        ref = agilicus.StandaloneRuleTreeRef(
            rule_tree_name=agilicus.StandaloneRuleName(tree),
            priority=len(trees) - idx,
        )
        tree_refs.append(ref)
    return tree_refs


def add_ruleset(
    ctx,
    name,
    trees,
    labels,
    org_id=None,
    scopes=None,
    standalone_rule_policy_id=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)

    spec = agilicus.StandaloneRulesetSpec(
        name=agilicus.StandaloneRuleName(name),
        org_id=org_id,
        rule_trees=_rule_tree_ref_list(trees),
        labels=[agilicus.StandaloneRulesetLabelName(label) for label in labels],
    )

    if standalone_rule_policy_id is not None:
        spec.standalone_rule_policy_id = standalone_rule_policy_id

    _add_object_conditions(spec, scopes)

    req = agilicus.StandaloneRuleset(spec=spec)
    result, _ = create_or_update(
        req,
        lambda obj: apiclient.rules_api.create_standalone_ruleset(obj),
        lambda guid, obj: apiclient.rules_api.replace_standalone_ruleset(
            guid, standalone_ruleset=obj
        ),
    )
    return result


def add_rulesets(ctx, rulesets, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return add_list_of_resouces(
        ctx,
        rulesets,
        agilicus.StandaloneRuleset,
        RulesetAddInfo(apiclient),
    )


def get_ruleset(ctx, ruleset_id, org_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.rules_api.get_standalone_ruleset(
        standalone_ruleset_id=ruleset_id, org_id=org_id
    )


def delete_ruleset(ctx, ruleset_id, org_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.rules_api.delete_standalone_ruleset(
        standalone_ruleset_id=ruleset_id, org_id=org_id
    )


def list_rulesets(ctx, standalone_rule_policy_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["standalone_rule_policy_ids"] = standalone_rule_policy_id
    kwargs = strip_none(kwargs)

    rules_resp = apiclient.rules_api.list_standalone_rulesets(**kwargs)
    return rules_resp.standalone_rulesets


def _add_object_conditions(spec, scopes):
    if scopes is None:
        return
    standalone_scopes = [agilicus.StandaloneRuleScope(scope) for scope in scopes]
    spec.object_conditions = agilicus.StandaloneObjectConditions(
        scopes=standalone_scopes
    )


def replace_ruleset(
    ctx,
    ruleset_id,
    org_id,
    name=None,
    trees=None,
    labels=None,
    scopes=None,
    standalone_rule_policy_id=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    base = apiclient.rules_api.get_standalone_ruleset(
        standalone_ruleset_id=ruleset_id, org_id=org_id
    )
    spec = base.spec
    if trees is not None:
        spec.rule_trees = _rule_tree_ref_list(trees)

    if labels is not None:
        spec.labels = [agilicus.StandaloneRulesetLabelName(label) for label in labels]

    if name is not None:
        spec.name = name

    if standalone_rule_policy_id is not None:
        spec.standalone_rule_policy_id = standalone_rule_policy_id

    _add_object_conditions(spec, scopes)

    return apiclient.rules_api.replace_standalone_ruleset(
        base.metadata.id, standalone_ruleset=base
    ).to_dict()


def format_rulesets(ctx, rulesets):
    trees_table = [column("priority"), column("rule_tree_name", "name")]
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("name"),
        spec_column("object_conditions"),
        subtable(ctx, "spec.rule_trees", trees_table, out_name="trees"),
    ]

    return format_table(ctx, rulesets, columns)


def add_label(ctx, label, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    labelName = agilicus.StandaloneRulesetLabelName(label)
    spec = agilicus.StandaloneRulesetLabelSpec(labelName, **kwargs)
    req = agilicus.StandaloneRulesetLabel(spec=spec)

    result, _ = create_or_update(
        req,
        lambda obj: apiclient.rules_api.create_ruleset_label(req),
    )
    return result


def list_labels(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.rules_api.list_ruleset_labels(
        **kwargs,
    ).standalone_ruleset_labels


def format_labels(ctx, labels):
    columns = [
        metadata_column("created"),
        spec_column("org_id"),
        spec_column("name"),
    ]
    return format_table(ctx, labels, columns)


def add_bundle(ctx, name, label=None, label_org_id=None, exclude=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    if label_org_id is None:
        label_org_id = org_id
    bundle_label = None
    if label is not None:
        label_name = agilicus.StandaloneRulesetLabelName(label)
        label_spec = agilicus.StandaloneRulesetLabelSpec(
            name=label_name, org_id=label_org_id
        )
        bundle_label = agilicus.StandaloneRulesetBundleLabel(label=label_spec)
        if exclude is not None:
            bundle_label.exclude = exclude

    bundle_name = agilicus.StandaloneRulesetBundleName(name)
    spec = agilicus.StandaloneRulesetBundleSpec(bundle_name, **kwargs)
    if bundle_label:
        spec.labels = []
        spec.labels.append(bundle_label)
    req = agilicus.StandaloneRulesetBundle(spec=spec)
    result, _ = create_or_update(
        req,
        lambda obj: apiclient.rules_api.create_standalone_ruleset_bundle(obj),
        lambda guid, obj: apiclient.rules_api.replace_standalone_ruleset_bundle(
            guid, standalone_ruleset_bundle=obj
        ),
    )
    return result


def add_bundle_label(
    ctx, bundle_id, label, label_org_id=None, exclude=None, priority=0, **kwargs
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    if label_org_id is None:
        label_org_id = org_id

    bundle = get_bundle(ctx, bundle_id, **kwargs)
    bundle_label = None
    label_name = agilicus.StandaloneRulesetLabelName(label)
    label_spec = agilicus.StandaloneRulesetLabelSpec(
        name=label_name,
        org_id=label_org_id,
    )
    bundle_label = agilicus.StandaloneRulesetBundleLabel(
        label=label_spec, priority=priority
    )
    if exclude is not None:
        bundle_label.exclude = exclude

    if not bundle.spec.labels:
        bundle.spec.labels = []

    bundle.spec.labels.append(bundle_label)
    return apiclient.rules_api.replace_standalone_ruleset_bundle(
        bundle_id, standalone_ruleset_bundle=bundle
    )


def delete_bundle_label(ctx, bundle_id, label, label_org_id=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    if label_org_id is None:
        label_org_id = org_id

    bundle = get_bundle(ctx, bundle_id, **kwargs)

    labels = []
    for _label in bundle.spec.labels or []:
        if _label.label.name.value == label and _label.label.org_id == label_org_id:
            continue
        labels.append(_label)

    bundle.spec.labels = labels
    return apiclient.rules_api.replace_standalone_ruleset_bundle(
        bundle_id, standalone_ruleset_bundle=bundle
    )


def delete_bundle(ctx, bundle_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    return apiclient.rules_api.delete_standalone_ruleset_bundle(bundle_id, **kwargs)


def list_bundles(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.rules_api.list_standalone_ruleset_bundles(
        **kwargs,
    )


def get_bundle(ctx, bundle_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.rules_api.get_standalone_ruleset_bundle(
        bundle_id,
        **kwargs,
    )


def format_bundles(ctx, bundles):
    label_columns = [
        column("label"),
    ]
    columns = [
        metadata_column("id"),
        metadata_column("created"),
        spec_column("org_id"),
        spec_column("name"),
        subtable(ctx, "spec.labels", label_columns),
    ]
    return format_table(ctx, bundles, columns)


def add_rule_policy(ctx, annotations, object_type, description=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    spec = agilicus.StandaloneRulePolicySpec(
        object_type=agilicus.EmptiableObjectType(object_type), **kwargs
    )
    if description is not None:
        spec.description = agilicus.StandaloneRulePolicyDescription(description)
    if annotations is not None:
        spec.annotations = annotations
    req = agilicus.StandaloneRulePolicy(spec=spec)
    return apiclient.rules_api.create_standalone_rule_policy(req)


def get_rule_policy(ctx, policy_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    policy = apiclient.rules_api.get_standalone_rule_policy(
        standalone_rule_policy_id=policy_id, org_id=org_id
    )

    return policy


def replace_rule_policy(
    ctx,
    policy_id,
    org_id,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    policy = apiclient.rules_api.get_standalone_rule_policy(
        standalone_rule_policy_id=policy_id, org_id=org_id
    )
    policy.spec = build_updated_model_validate(
        agilicus.StandaloneRulePolicySpec,
        policy.spec,
        kwargs,
        True,
    )
    return apiclient.rules_api.replace_standalone_rule_policy(
        standalone_rule_policy_id=policy.metadata.id,
        standalone_rule_policy=policy,
    )


def delete_rule_policy(ctx, policy_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    apiclient.rules_api.delete_standalone_rule_policy(
        standalone_rule_policy_id=policy_id, org_id=org_id
    )


def list_rule_policies(ctx, policy_class=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)
    if policy_class:
        kwargs["policy_classes"] = list(policy_class)
    rules_resp = apiclient.rules_api.list_standalone_rule_policies(**kwargs)
    return rules_resp.standalone_rule_policies


def format_rule_policies(ctx, policies):
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("object_type"),
        spec_column("object_id"),
        spec_column("policy_class"),
        spec_column("policy_instance"),
        spec_column("description"),
    ]
    return format_table(ctx, policies, columns)


def add_scope_condition_rule(
    ctx,
    name,
    actions,
    purpose=None,
    scopes=None,
    standalone_rule_policy_id=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs = strip_none(kwargs)

    if not scopes:
        raise Exception("require at least one scope")

    cond = agilicus.ScopeCondition(
        condition_type=ConditionTypes.scope_condition.name,
        scopes=[agilicus.StandaloneRuleScope(scope) for scope in scopes],
    )
    extended_cond = agilicus.RuleCondition(condition=cond, negated=False)

    rule = agilicus.RuleConfig(
        name=name,
        extended_condition=extended_cond,
        actions=[agilicus.RuleAction(action=action) for action in actions],
    )

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    spec = agilicus.StandaloneRuleSpec(org_id=org_id, rule=rule)
    if purpose is not None:
        spec.purpose = purpose

    if standalone_rule_policy_id is not None:
        spec.standalone_rule_policy_id = standalone_rule_policy_id

    req = agilicus.StandaloneRule(spec=spec)
    result, _ = create_or_update(
        req,
        lambda obj: apiclient.rules_api.create_standalone_rule(obj),
        lambda guid, obj: apiclient.rules_api.replace_standalone_rule(
            guid, standalone_rule=obj
        ),
    )
    return result


def add_network_protocol_condition_rule(
    ctx,
    name,
    actions,
    purpose=None,
    protocol=None,
    standalone_rule_policy_id=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs = strip_none(kwargs)

    cond = agilicus.NetworkProtocolCondition(
        condition_type=ConditionTypes.network_protocol_condition.name,
        protocol=protocol,
    )
    extended_cond = agilicus.RuleCondition(condition=cond, negated=False)

    rule = agilicus.RuleConfig(
        name=name,
        extended_condition=extended_cond,
        actions=[agilicus.RuleAction(action=action) for action in actions],
    )

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    spec = agilicus.StandaloneRuleSpec(org_id=org_id, rule=rule)
    if purpose is not None:
        spec.purpose = purpose

    if standalone_rule_policy_id is not None:
        spec.standalone_rule_policy_id = standalone_rule_policy_id

    req = agilicus.StandaloneRule(spec=spec)
    result, _ = create_or_update(
        req,
        lambda obj: apiclient.rules_api.create_standalone_rule(obj),
        lambda guid, obj: apiclient.rules_api.replace_standalone_rule(
            guid, standalone_rule=obj
        ),
    )
    return result


def add_agilicus_default_expose_allow(
    ctx,
    label="agilicus-defaults-policy",
    name="default_expose_network",
    action="allow",
    purpose=None,
    **kwargs,
):
    add_network_protocol_condition_rule(
        ctx,
        name,
        [action],
        protocol="tcp",
        **kwargs,
    )
    add_label(ctx, label=label, **kwargs)
    add_rule_tree(ctx, name, children=[], rules=[name], **kwargs)
    add_ruleset(ctx, name, trees=[name], labels=[label], **kwargs)


def add_agilicus_default_policy(
    ctx,
    **kwargs,
):
    add_agilicus_default_expose_allow(ctx)
