import copy
import datetime
import json
import os
import time
from ..input_helpers import (
    get_org_from_input_or_ctx,
    update_org_from_input_or_ctx,
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
    TimeperiodPolicyTemplate,
    TimeOfDayCondition,
)

from ..output.table import (
    format_table,
    spec_column,
    metadata_column,
    subtable,
    column,
)
from ..output import json as out_json
from ..resources import query_resources
from ..resources import reconcile_default_policy
from .. import orgs


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


def list_policy_templates(ctx, apiclient=None, **kwargs):
    if not apiclient:
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


def add_default_to_resource_policies(
    ctx,
    org_id=None,
    start_org=None,
    dump_dir=None,
    dry_run=False,
    delay=None,
    replace=False,
):
    org_objs = []
    if start_org is not None:
        org_objs = orgs.query(ctx, page_at_id=start_org, enabled=True, page_size=150)
    else:
        org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
        org_objs = [orgs.get_raw(ctx, org_id)]

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    for org in org_objs:
        print(f"Adding default to {org.organisation}, {org.id}")
        _add_default_to_resource_policies(
            ctx,
            org.id,
            apiclient=apiclient,
            dump_dir=dump_dir,
            dry_run=dry_run,
            delay=delay,
            replace=replace,
        )


def find_duplicate_resource_policies(
    ctx,
    org_id=None,
    start_org=None,
    dump_dir=None,
    dry_run=False,
    delay=None,
    replace=False,
):
    org_objs = []
    if start_org is not None:
        org_objs = orgs.query(
            ctx, page_at_id=start_org, org_id="", enabled=True, page_size=150
        )
    else:
        org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
        org_objs = [orgs.get_raw(ctx, org_id)]

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    for org in org_objs:
        print(f"finding duplicates from {org.organisation}, {org.id}")
        dupes = _find_policy_templates_with_dupes(
            ctx,
            org.id,
            apiclient=apiclient,
            dump_dir=dump_dir,
            dry_run=dry_run,
            delay=delay,
            replace=replace,
        )

        for key, templates in dupes:
            for t in templates:
                print(f"\t {key}: {t.metadata.id}")


def update_resource_policy(
    ctx,
    instance_id,
    org_id=None,
    clear_default_actions=None,
    default_action=None,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs = {}
    update_org_from_input_or_ctx(kwargs, ctx, org_id=org_id)

    policy = apiclient.policy_templates_api.get_policy_template_instance(
        instance_id=instance_id, **kwargs
    )
    template_type = policy.spec.template.template_type
    if template_type != "simple_resource":
        raise TypeError(
            f"instance {instance_id} is {template_type}; expected 'simple_resource'"
        )

    default_actions = None
    if default_action and len(default_action) > 0:
        default_actions = list(default_action)
    elif clear_default_actions:
        default_actions = []

    if default_actions is not None:
        policy.spec.template.default_actions = [
            RuleAction(action=a) for a in default_actions
        ]

    return apiclient.policy_templates_api.replace_policy_template_instance(
        instance_id=instance_id, policy_template_instance=policy
    )


def _dump_policy_template(ctx, policy, dump_dir):
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    file_name = (
        f"{policy.spec.org_id}-{policy.spec.object_type}-{policy.metadata.id}"
        f"-{policy.spec.object_id}-{now}.json"
    )
    out_json.output_json_to_file(
        ctx, policy.to_dict(), os.path.join(dump_dir, file_name)
    )


def _find_policy_templates_with_dupes(
    ctx, org_id, apiclient, dump_dir=None, dry_run=False, delay=None, replace=False
):
    """
    Walks through all resource policies for an organisation, ensuring that they have
    a default rule. Can optionally back up the existing policies in case something
    goes wrong in the migration so that they may be reapplied. If replace is True, the
    default rule be rewritten if present.
    """
    object_to_templates = {}
    templates = list_policy_templates(
        ctx, org_id=org_id, template_type="simple_resource", apiclient=apiclient
    )

    for template in templates:
        spec = template.spec
        if not spec.object_id:
            continue
        obj_tmpls = object_to_templates.setdefault(spec.object_id, [])
        obj_tmpls.append(template)

    return [pair for pair in object_to_templates.items() if len(pair[1]) > 1]


def _add_default_to_resource_policies(
    ctx, org_id, apiclient, dump_dir=None, dry_run=False, delay=None, replace=False
):
    """
    Walks through all resource policies for an organisation, ensuring that they have
    a default rule. Can optionally back up the existing policies in case something
    goes wrong in the migration so that they may be reapplied. If replace is True, the
    default rule be rewritten if present.
    """
    templates = list_policy_templates(
        ctx, org_id=org_id, template_type="simple_resource", apiclient=apiclient
    )

    for orig_template in templates:
        template = copy.deepcopy(orig_template)
        spec = template.spec
        print(
            f"\t - {template.metadata.id}, res={spec.object_id}, name={spec.name}...",
            end="",
        )
        should_migrate = add_default_rule(spec.template, replace=replace)
        if not should_migrate:
            print(" [SKIPPED]")
            continue

        if dump_dir:
            _dump_policy_template(ctx, orig_template, dump_dir)

        try:
            if not dry_run:
                apiclient.policy_templates_api.replace_policy_template_instance(
                    template.metadata.id,
                    policy_template_instance=template,
                )
                if delay:
                    time.sleep(delay)
        except Exception as exc:
            print(f" [FAILED] {exc}")
            continue

        print(" [DONE]")


def fetch_resource_rules(ctx, org_id=None, dump_dir=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    kwargs = strip_none(kwargs)
    if not kwargs.get("resource_id"):
        print("  fetching all applications")
    for res in query_resources(
        ctx, resource_type="application", org_id=org_id, **kwargs
    ):
        fetch_resource(ctx, res, dump_dir=dump_dir)


def add_default_rule(template, replace=False):
    """
    Builds a default rule for the resource template. The rule matches only if the
    request is http (so we don't hit the network layer policy), and we insert it
    at the lowest priority for the policy. The default rule applies the 'no permission'
    action. Users may override the behaviour, since it is just a normal rule under
    their control.
    """
    if template.default_actions and not replace:
        return False

    template.default_actions = [RuleAction(action="no_permissions")]
    return True


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
    new_rules = [_migrate_http_rule(rule) for rule in rules]

    template = SimpleResourcePolicyTemplate(
        rules=new_rules,
        policy_structure=policy_structures,
        template_type="simple_resource",
    )
    add_default_rule(template)
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


def parse_time_of_day_string(time_of_day) -> TimeOfDayCondition:
    split_str = time_of_day.split(":")
    hour = split_str[0]
    minute = 0
    if len(split_str) > 1:
        minute = split_str[0]
    return TimeOfDayCondition(hour=int(hour), minute=int(minute))


def set_timeperiod_policy(
    ctx, name, timezone, day, start_time_of_day, end_time_of_day, label=None, **kwargs
):
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    timeperiod = TimeperiodPolicyTemplate(
        timezone,
        list(day),
        list(label or []),
        start_time_of_day=parse_time_of_day_string(start_time_of_day),
        end_time_of_day=parse_time_of_day_string(end_time_of_day),
        template_type="timeperiod",
    )

    spec = PolicyTemplateInstanceSpec(
        org_id=org_id,
        name=name,
        template=timeperiod,
    )

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
