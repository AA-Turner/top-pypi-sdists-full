from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


async def update(
    hub,
    ctx,
    before: Dict[str, Any],
    account_id: str,
    notification_type: str,
    action_threshold: Dict[str, Any],
    definition: Dict[Any, Any],
    execution_role_arn: str,
    approval_model: str,
    subscribers: List[Dict[str, Any]],
):
    """
    Updates the Budget Action
    Args:
        before: existing resource
        account_id(str): Account ID
        notification_type(str): The type of a notification. It must be ACTUAL or FORECASTED.
        action_threshold(Dict): The trigger threshold of the action.
        definition(Dict[Any, Any]): Specifies all of the type-specific parameters. IamActionDefinition, ScpActionDefinition, SsmActionDefinition
        execution_role_arn(str): The role passed for action execution and reversion. Roles and actions must be in the same account.
        approval_model (str): This specifies if the action needs manual or automatic approval.
        subscribers (List[Dict[str, Any]]): A list of subscribers.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": None}

    """
    result = dict(comment=[], result=True, ret=None)
    update_payload = {}

    resource_parameters = OrderedDict(
        {
            "NotificationType": notification_type,
            "ActionThreshold": action_threshold,
            "Definition": definition,
            "ExecutionRoleArn": execution_role_arn,
            "ApprovalModel": approval_model,
        }
    )

    for key, value in resource_parameters.items():
        if key in before.keys():
            if (value is not None) and value != before[key]:
                update_payload[key] = resource_parameters[key]

    if not hub.tool.aws.state_comparison_utils.are_lists_identical(
        subscribers,
        before.get("Subscribers"),
    ):
        update_payload["Subscribers"] = subscribers

    if update_payload:
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.budgets.update_budget_action(
                ctx,
                AccountId=account_id,
                BudgetName=before.get("BudgetName"),
                ActionId=before.get("ActionId"),
                **update_payload,
            )
            if not update_ret["result"]:
                result["comment"] += update_ret["comment"]
                result["result"] = False
                return result
        result["ret"] = {}
        result = update_result(result, update_payload)

    return result


def update_result(
    result: Dict[str, Any], update_payload: Dict[str, Any]
) -> Dict[str, Any]:
    parameters = OrderedDict(
        {
            "NotificationType": "notification_type",
            "ActionThreshold": "action_threshold",
            "Definition": "definition",
            "ExecutionRoleArn": "execution_role_arn",
            "ApprovalModel": "approval_model",
            "Subscribers": "subscribers",
        }
    )

    for raw_parameter, present_parameter in parameters.items():
        if raw_parameter in update_payload:
            result["ret"][present_parameter] = update_payload[raw_parameter]
            result["comment"] += [
                f"Update {present_parameter}: {update_payload[raw_parameter]}"
            ]
    return result
