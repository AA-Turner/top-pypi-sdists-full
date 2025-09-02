from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List

from dict_tools import data


async def update_events_rule(
    hub,
    ctx,
    name,
    plan_state: Dict[str, Any],
    resource_id: str,
    old_targets: List = None,
    new_targets: List = None,
    schedule_expression: str = None,
    event_pattern: str = None,
    state: str = None,
    description: str = None,
    role_arn: str = None,
    event_bus_name: str = None,
):
    """Updates the specified rule.

    If you are updating an existing rule, the rule is replaced with what you specify in this
    update_events_rule. If you omit arguments in update_events_rule , the old values for those arguments are not kept.
    Instead, they are replaced with null values.

    When you create or update a rule, incoming events might not immediately start matching to new or updated rules.
    Allow a short period of time for changes to take effect.

    A rule must contain at least an event_pattern or schedule_expression. Rules with event_pattern are triggered when a
    matching event is observed. Rules with schedule_expression self-trigger based on the given schedule. A rule can
    have both an event_pattern and a schedule_expression, in which case the rule triggers on matching events as well as
    on a schedule.

    Args:
        plan_state(dict): idem ``--test`` state for update on AWS Lambda.
        resource_id: The name of the AWS CloudWatch Events Rule.
        old_targets(list, Optional): Existing targets associated with given CloudWatchEvent Rule.
        new_targets(list, Optional): The targets to update or add to the rule.
        schedule_expression (str, Optional): Scheduling expression.
            For example, ``"cron(0 20 * * ? *)"`` or ``"rate(5 minutes)"``.
        event_pattern (str, Optional): Rules use event patterns to select events and route them to targets. A pattern
            either matches an event or it doesn't. Event patterns are represented as JSON objects with a structure that
            is similar to that of events.
        state (str, Optional): Indicates whether the rule is enabled or disabled.
        description (str, Optional): A description of the rule.
        role_arn (str, Optional): The Amazon Resource Name (ARN) of the IAM role associated with the rule.
            If you're setting an event bus in another account as the target and that account granted permission to your
            account through an organization instead of directly by the account ID, you must specify a RoleArn with proper
            permissions in the Target structure, instead of here in this parameter.
        event_bus_name (str, Optional) : The name or ARN of the event bus to

    Returns:
        {"result": True|False, "comment": Tuple, "ret": Dict}

    """
    result = dict(comment=[], result=True, ret=None)
    update_params = OrderedDict(
        {
            "rule_status": state,
            "schedule_expression": schedule_expression,
            "event_bus_name": event_bus_name,
            "description": description,
            "role_arn": role_arn,
            "name": resource_id,
        }
    )
    modified_params = {}
    for key, value in update_params.items():
        if value and value != plan_state.get(key):
            modified_params[key] = value
            plan_state[key] = value

    if event_pattern and not hub.tool.aws.state_comparison_utils.are_policies_equal(
        plan_state.get("event_pattern", "{}"), event_pattern
    ):
        modified_params["event_pattern"] = event_pattern
        plan_state["event_pattern"] = event_pattern

    if modified_params:
        if not ctx.get("test", False):
            update_rule = await hub.exec.boto3.client.events.put_rule(
                ctx=ctx,
                Name=plan_state.get("name"),
                ScheduleExpression=plan_state.get("schedule_expression"),
                EventPattern=plan_state.get("event_pattern"),
                State=plan_state.get("rule_status"),
                Description=plan_state.get("description"),
                RoleArn=plan_state.get("role_arn"),
                EventBusName=plan_state.get("event_bus_name"),
            )
            result["result"] = update_rule["result"]
            if not result["result"]:
                result["comment"] = update_rule["comment"]
                return result
    target_diff = data.recursive_diff(old_targets, new_targets, ignore_order=True)
    if new_targets and target_diff:
        modified_params["targets"] = new_targets
        plan_state["targets"] = new_targets
        targets_to_put = target_diff.get("new")
        targets_to_remove = target_diff.get("old")
        if not ctx.get("test", False):
            if targets_to_remove:
                remove_target = await hub.exec.boto3.client.events.remove_targets(
                    ctx,
                    Rule=plan_state.get("name"),
                    Ids=[target["Id"] for target in targets_to_remove],
                    EventBusName=plan_state.get("event_bus_name"),
                )
                result["result"] = remove_target["result"]
                if not result["result"]:
                    result["comment"] += remove_target["comment"]
                    return result
            if targets_to_put:
                put_targets = await hub.exec.boto3.client.events.put_targets(
                    ctx,
                    Rule=plan_state.get("name"),
                    Targets=targets_to_put,
                    EventBusName=plan_state.get("event_bus_name"),
                )
                result["result"] = put_targets["result"]
                if not result["result"]:
                    result["comment"] += put_targets["comment"]
                    return result
    if modified_params:
        if not ctx.get("test", False):
            result["comment"] += hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.events.rule", name=name
            )
        else:
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.events.rule", name=name
            )
        result["ret"] = modified_params
    return result


def compare_and_return_target_ids(old_targets: List, new_targets: List):
    """Compares old_targets and new targets and return the new list of target ids that need to be updated.

    Args:
        old_targets(list): Existing targets associated with the given rule.
        new_targets(list): Newer list of targets to be associated with rule.

    Returns:
        {"result": True|False, "comment": ("A tuple",), "ret": Dict}

    """
    result = dict(comment=[], result=True, ret=None)
    targets_to_remove = []
    old_targets_map = {target.get("Id"): target for target in old_targets or []}
    if new_targets is not None:
        for target in new_targets:
            if target.get("Id") in old_targets_map:
                if target != old_targets_map.get(target.get("Id")):
                    targets_to_remove.append(target.get("Id"))

        old_targets_map = {target.get("Id"): target for target in old_targets or []}
        for id in targets_to_remove:
            del old_targets_map[id]
        final_targets = list(old_targets_map.values()) + new_targets
        result["ret"] = {"final_result": final_targets}
    return result
