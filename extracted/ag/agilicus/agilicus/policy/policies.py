import copy
import datetime
import json
import os
from ..input_helpers import (
    get_org_from_input_or_ctx,
    model_from_dict,
    strip_none,
)

from .. import context

from agilicus import (
    create_or_update,
    LabelName,
    PolicyTemplateInstance,
    PolicyTemplateInstanceSpec,
    MFAPolicyTemplate,
    SourceInfoPolicyTemplate,
    SimpleResourcePolicyTemplateStructureNode,
    SimpleResourcePolicyTemplateStructure,
    SimpleResourcePolicyTemplate,
    StandaloneRuleName,
    RuleAction,
    ResourceConfig,
    RulesConfig,
    RuleCondition,
    HttpRuleCondition,
    EmptiableObjectType,
)

from ..output.table import (
    format_table,
    spec_column,
    metadata_column,
    subtable,
    column,
)
from ..resources import query_resources
from ..resources import reconcile_default_policy


class InstanceAddInfo:
    def __init__(self, apiclient):
        super().__init__()


def set_multifactor_policy(ctx, name, duration, label=None, description=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    mfa = MFAPolicyTemplate(
        seconds_since_last_challenge=duration,
        labels=[LabelName(la) for la in (label or [])],
        template_type="mfa",
    )

    spec = PolicyTemplateInstanceSpec(
        org_id=org_id,
        name=name,
        template=mfa,
    )

    if description is not None:
        spec.description = description

    tmpl = PolicyTemplateInstance(spec=spec)
    templates_api = apiclient.policy_templates_api
    resp, _ = create_or_update(
        tmpl,
        lambda obj: templates_api.create_policy_template_instance(obj),
        lambda guid, obj: templates_api.replace_policy_template_instance(
            guid, policy_template_instance=obj
        ),
        to_dict=False,
    )
    return resp


def ruleset_labelled(ruleset, label):
    for ruleset_label in ruleset.spec.labels or []:
        if str(ruleset_label) == label:
            return True
    return False


def list_multifactor_policies(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    result = apiclient.policy_templates_api.list_policy_template_instances(
        org_id=org_id, template_type="mfa"
    )
    return result.policy_template_instances


def format_multifactor_policies(ctx, templates):
    mfa_columns = [
        column("seconds_since_last_challenge"),
        column("labels"),
    ]
    mfa_table = subtable(ctx, "spec.template", mfa_columns)
    columns = [
        spec_column("org_id"),
        spec_column("name"),
        spec_column("template.template_type", "type"),
        mfa_table,
    ]

    return format_table(ctx, templates, columns)


def list_policy_templates(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)
    result = apiclient.policy_templates_api.list_policy_template_instances(**kwargs)
    return result.policy_template_instances


def delete_policy_template(ctx, instance_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)
    apiclient.policy_templates_api.delete_policy_template_instance(instance_id, **kwargs)


def get_policy_template(ctx, instance_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)
    return apiclient.policy_templates_api.get_policy_template_instance(
        instance_id, **kwargs
    )


def format_policy_templates(ctx, templates):
    columns = [
        spec_column("org_id"),
        metadata_column("id"),
        spec_column("name"),
        spec_column("template.template_type", "type"),
        spec_column("description"),
        spec_column("template"),
    ]

    return format_table(ctx, templates, columns)


def set_source_info_policy(
    ctx,
    name,
    action,
    source_subnet,
    iso_country_code,
    invert,
    log_message=None,
    label=None,
    description=None,
    **kwargs,
):
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    tmpl = SourceInfoPolicyTemplate(
        action=action,
        source_subnets=list(source_subnet or []),
        iso_country_codes=list(iso_country_code or []),
        invert=invert,
        labels=[LabelName(la) for la in (label or [])],
        template_type="source_info",
    )

    if log_message:
        tmpl.log_message = log_message

    spec = PolicyTemplateInstanceSpec(
        org_id=org_id,
        name=name,
        template=tmpl,
    )

    if description is not None:
        spec.description = description

    tmpl = PolicyTemplateInstance(spec=spec)
    templates_api = apiclient.policy_templates_api
    resp, _ = create_or_update(
        tmpl,
        lambda obj: templates_api.create_policy_template_instance(obj),
        lambda guid, obj: templates_api.replace_policy_template_instance(
            guid, policy_template_instance=obj
        ),
        to_dict=False,
    )
    return resp


def migrate_policy_rules(ctx, org_id=None, dump_dir=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    kwargs = strip_none(kwargs)
    if not kwargs.get("resource_id"):
        print("  migrating all applications")
    for res in query_resources(
        ctx, resource_type="application", org_id=org_id, **kwargs
    ):
        migrate_resource(ctx, res, dump_dir=dump_dir)


def fetch_resource_rules(ctx, org_id=None, dump_dir=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    kwargs = strip_none(kwargs)
    if not kwargs.get("resource_id"):
        print("  fetching all applications")
    for res in query_resources(
        ctx, resource_type="application", org_id=org_id, **kwargs
    ):
        fetch_resource(ctx, res, dump_dir=dump_dir)


def migrate_resource(ctx, resource, dump_dir=None):
    print(f"  migrating resource: {resource.spec.name}")
    resource.spec.config = resource.spec.config or ResourceConfig()
    resource.spec.config.rules_config = (
        resource.spec.config.rules_config or RulesConfig()
    )

    rules = resource.spec.config.rules_config.rules or []
    policy_structures = []
    for rule in rules:
        node = SimpleResourcePolicyTemplateStructureNode(
            priority=rule.priority or 0,
            rule_name=StandaloneRuleName(rule.name),
            children=[],
        )
        policy_structures.append(
            SimpleResourcePolicyTemplateStructure(
                name=StandaloneRuleName(rule.name),
                root_node=node,
            )
        )
    template = SimpleResourcePolicyTemplate(
        rules=[_migrate_http_rule(rule) for rule in rules],
        policy_structure=policy_structures,
        template_type="simple_resource",
    )
    instance_spec = PolicyTemplateInstanceSpec(
        org_id=resource.spec.org_id,
        template=template,
        name="resource-policy",
        object_id=resource.metadata.id,
        object_type=EmptiableObjectType(resource.spec.resource_type.value),
    )

    tmpl = PolicyTemplateInstance(
        spec=instance_spec,
    )

    # ensure the resource has been reconciled
    resource = reconcile_default_policy(
        ctx, resource.metadata.id, org_id=resource.spec.org_id
    )

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    templates_api = apiclient.policy_templates_api

    def do_update(guid, obj):
        return templates_api.replace_policy_template_instance(
            guid, policy_template_instance=obj
        )

    updater = do_update
    # If there are no rules, don't blow away any previously create config. This allows us
    # to reapply the policy from scratch using a new config if needed, but at the same
    # time, ensures we don't blow away config if we run the same migration twice (since
    # the first migration will clear the rules, meaning the second will set an empty
    # policy. )
    if not rules:
        updater = None
    resp, _ = create_or_update(
        tmpl,
        lambda obj: templates_api.create_policy_template_instance(obj),
        updater,
        to_dict=False,
    )

    if rules:
        _clear_old_rules(apiclient, resource, dump_dir)
    return resp


def fetch_resource(ctx, resource, dump_dir=None):
    print(f"  fetching resource: {resource.spec.name}")
    resource.spec.config = resource.spec.config or ResourceConfig()
    resource.spec.config.rules_config = (
        resource.spec.config.rules_config or RulesConfig()
    )

    if dump_dir:
        _dump_resource_rules(resource, dump_dir)
    else:
        print(resource.spec.config.rules_config.to_dict())


def _dump_resource_rules(resource, dump_dir):
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    file_name = f"{resource.spec.org_id}-{resource.spec.name}-{now}.json"
    with open(os.path.join(dump_dir, file_name), "w") as f:
        json.dump(resource.spec.config.rules_config.to_dict(), f)


def _clear_old_rules(apiclient, resource, dump_dir):
    if dump_dir:
        _dump_resource_rules(resource, dump_dir)

    resource.spec.config.rules_config = RulesConfig(rules=[])

    apiclient.resources_api.replace_resource(resource.metadata.id, resource=resource)


def _migrate_http_rule(input_rule):
    if input_rule.extended_condition is not None:
        return input_rule

    new_rule = copy.deepcopy(input_rule)
    new_rule.actions = new_rule.actions or [RuleAction(action="allow")]
    input_cond = new_rule.condition.to_dict()
    input_cond["condition_type"] = "http_rule_condition"
    cond = model_from_dict(HttpRuleCondition, input_cond)
    new_rule.extended_condition = RuleCondition(
        condition=cond,
        negated=False,
    )
    del new_rule["condition"]
    return new_rule


def create_policy_template(ctx, template_dict, **kwargs):
    template_as_instance = model_from_dict(PolicyTemplateInstance, template_dict)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.policy_templates_api.create_policy_template_instance(
        template_as_instance
    )


def replace_policy_template(ctx, instance_id, template_dict, **kwargs):
    template_as_instance = model_from_dict(PolicyTemplateInstance, template_dict)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.policy_templates_api.replace_policy_template_instance(
        instance_id, policy_template_instance=template_as_instance
    )


def kick_policy_template(ctx, instance_id, org_id=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    existing = apiclient.policy_templates_api.get_policy_template_instance(
        instance_id,
        org_id=org_id,
    )
    return apiclient.policy_templates_api.replace_policy_template_instance(
        instance_id,
        policy_template_instance=existing,
    )
