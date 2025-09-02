"""State module for managing AWS Budget Actions."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    budget_name: str,
    notification_type: str,
    action_type: str,
    action_threshold: make_dataclass(
        "ActionThreshold",
        [("ActionThresholdValue", float), ("ActionThresholdType", str)],
    ),
    definition: make_dataclass(
        "Definition",
        [
            (
                "IamActionDefinition",
                make_dataclass(
                    "IamActionDefinition",
                    [
                        ("PolicyArn", str),
                        ("Roles", List[str], field(default=None)),
                        ("Groups", List[str], field(default=None)),
                        ("Users", List[str], field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "ScpActionDefinition",
                make_dataclass(
                    "ScpActionDefinition", [("PolicyId", str), ("TargetIds", List[str])]
                ),
                field(default=None),
            ),
            (
                "SsmActionDefinition",
                make_dataclass(
                    "SsmActionDefinition",
                    [
                        ("ActionSubType", str),
                        ("Region", str),
                        ("InstanceIds", List[str]),
                    ],
                ),
                field(default=None),
            ),
        ],
    ),
    execution_role_arn: str,
    approval_model: str = None,
    subscribers: List[
        make_dataclass("Subscriber", [("SubscriptionType", str), ("Address", str)])
    ] = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Creates an AWS Budget Action with the requested name and rules.

    Args:
        name(str):
            The unique name of the Budget Action.
        budget_name(str):
            A string that represents the budget name. The ":" and "" characters aren't allowed.
        notification_type(str):
            The type of a notification. It must be ACTUAL or FORECASTED.
        action_type(str):
            The type of action. This defines the type of tasks that can be carried out by this action. This field also
            determines the format for definition.
        action_threshold(dict[str, Any]):
            The trigger threshold of the action.

            * ActionThresholdValue (float):
                The threshold of a notification.

            * ActionThresholdType (str):
                The type of threshold for a notification.
        definition(dict[str, Any]):
            Specifies all of the type-specific parameters.

            * IamActionDefinition (dict[str, Any], Optional):
                The Identity and Access Management (IAM) action definition details.

                * PolicyArn (str):
                    The Amazon Resource Name (ARN) of the policy to be attached.

                * Roles (list[str], Optional):
                    A list of roles to be attached. There must be at least one role.

                * Groups (list[str], Optional):
                    A list of groups to be attached. There must be at least one group.

                * Users (list[str], Optional):
                    A list of users to be attached. There must be at least one user.

            * ScpActionDefinition (dict[str, Any], Optional):
                The service control policies (SCPs) action definition details.

                * PolicyId (str):
                    The policy ID attached.

                * TargetIds (list[str]):
                    A list of target IDs.

            * SsmActionDefinition (dict[str, Any], Optional):
                The Amazon Web Services Systems Manager (SSM) action definition details.

                * ActionSubType (str):
                    The action subType.

                * Region (str):
                    The Region to run the SSM document.

                * InstanceIds (list[str]):
                    The EC2 and RDS instance IDs.
        execution_role_arn(str):
            The role passed for action execution and reversion. Roles and actions must be in the same account.
        approval_model (str):
            This specifies if the action needs manual or automatic approval.
        subscribers(list[dict[str, Any]]):
            A list of subscribers.

            The subscriber to a budget notification consists of a subscription type and either an Amazon SNS topic or
            an email address.

            For example, an email subscriber has the following parameters:
              * A `subscriptionType` of `EMAIL`
              * An `address` of `example@example.com`

            * SubscriptionType (str):
                The type of notification that Amazon Web Services sends to a subscriber.

            * Address (str):
                The address that Amazon Web Services sends budget notifications to, either an SNS topic or an
                email.

                When you create a subscriber, the value of `Address` can't contain line breaks.
        resource_id(str, Optional):
            Action ID to identify the resource.

    Request Syntax:
      .. code-block:: sls

        [action-resource-id]:
          aws.budgets.budget_action.present:
            - resource_id: "string"
            - budget_name: "string"
            - notification_type: "string"
            - action_type: "string"
            - action_threshold:
                ActionThresholdType: "string"
                ActionThresholdValue: int
            - definition:
                IamActionDefinition:
                  PolicyArn: "string"
                  Users:
                    - "string"
            - execution_role_arn: "string"
            - approval_model: "string"
            - status: "string"
            - subscribers:
                - Address: "string"
                  SubscriptionType: "string"


    Returns:
        Dict[str, str]

    Examples:
        .. code-block:: sls

            12345a12-126d-1234-1ab2-1f4dca2a1234:
              aws.budgets.budget_action.present:
                - name: 12345a12-126d-1234-1ab2-1f4dca2a1234
                - resource_id: 12345a12-126d-1234-1ab2-1f4dca2a1234
                - budget_name: test_budget
                - notification_type: ACTUAL
                - action_type: APPLY_IAM_POLICY
                - action_threshold:
                    ActionThresholdType: PERCENTAGE
                    ActionThresholdValue: 123.0
                - definition:
                    IamActionDefinition:
                      PolicyArn: arn:aws:iam::123456789101:policy/budget_policy
                      Users:
                        - plokare
                - execution_role_arn: arn:aws:iam::123456789101:role/budget_role
                - approval_model: AUTOMATIC
                - status: STANDBY
                - subscribers:
                    - Address: abc@test.com
                      SubscriptionType: EMAIL

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before = None
    resource_updated = False
    account_details = await hub.exec.boto3.client.sts.get_caller_identity(ctx)
    account_id = account_details["ret"]["Account"]

    if resource_id:
        before = await hub.exec.boto3.client.budgets.describe_budget_action(
            ctx, AccountId=account_id, BudgetName=budget_name, ActionId=resource_id
        )
        if not before["result"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

    if before:
        result[
            "old_state"
        ] = hub.tool.aws.budgets.conversion_utils.convert_raw_budget_action_to_present(
            ctx, raw_resource=before["ret"]["Action"], idem_resource_name=name
        )
        plan_state = copy.deepcopy(result["old_state"])

        update_ret = await hub.tool.aws.budgets.budget_action.update(
            ctx,
            before=before["ret"]["Action"],
            account_id=account_id,
            notification_type=notification_type,
            action_threshold=action_threshold,
            definition=definition,
            execution_role_arn=execution_role_arn,
            approval_model=approval_model,
            subscribers=subscribers,
        )
        result["comment"] += update_ret["comment"]
        result["result"] = update_ret["result"]
        resource_updated = resource_updated or bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            plan_state = update_ret["ret"]

        if resource_updated:
            if ctx.get("test", False):
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.budgets.budget_action", name=name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.budgets.budget_action", name=name
                )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "budget_name": budget_name,
                    "notification_type": notification_type,
                    "action_type": action_type,
                    "action_threshold": action_threshold,
                    "definition": definition,
                    "execution_role_arn": execution_role_arn,
                    "approval_model": approval_model,
                    "subscribers": subscribers,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.budgets.budget_action", name=name
            )
            return result

        ret = await hub.exec.boto3.client.budgets.create_budget_action(
            ctx,
            AccountId=account_id,
            BudgetName=budget_name,
            NotificationType=notification_type,
            ActionType=action_type,
            ActionThreshold=action_threshold,
            Definition=definition,
            ExecutionRoleArn=execution_role_arn,
            ApprovalModel=approval_model,
            Subscribers=subscribers,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.budgets.budget_action", name=name
        )
        resource_id = ret["ret"]["ActionId"]

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.boto3.client.budgets.describe_budget_action(
                ctx, AccountId=account_id, BudgetName=budget_name, ActionId=resource_id
            )
            if not after["result"]:
                result["result"] = False
                result["comment"] = after["comment"]
                return result
            result[
                "new_state"
            ] = hub.tool.aws.budgets.conversion_utils.convert_raw_budget_action_to_present(
                ctx,
                raw_resource=after["ret"]["Action"],
                idem_resource_name=name,
            )
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(
    hub, ctx, name: str, budget_name: str = None, resource_id: str = None
) -> Dict[str, Any]:
    """Deletes an AWS Budget Action.

    Args:
        name(str): An Idem name of the AWS Budget Action.
        budget_name(str, Optional): Budget Name
        resource_id(str, Optional): Budget Action ID to identify the resource.
            Idem automatically considers this resource being absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            [action-resource-id]:
              aws.budgets.budget_action.absent:
                - name: value
                - budget_name: value
                - resource_id: value

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.budgets.budget_action.absent:
                - name: value
                - budget_name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    account_details = await hub.exec.boto3.client.sts.get_caller_identity(ctx)
    account_id = account_details["ret"]["Account"]

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.budgets.budget_action", name=name
        )
        return result

    if not account_id or not budget_name:
        result["comment"] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
            resource_type="aws.budgets.budget_action",
            name=name,
            args=["account_id", "budget_name"],
        )
        result["result"] = False
        return result

    before = await hub.exec.boto3.client.budgets.describe_budget_action(
        ctx, AccountId=account_id, BudgetName=budget_name, ActionId=resource_id
    )

    if not before:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.budgets.budget_action", name=name
        )
    elif ctx.get("test", False):
        result[
            "old_state"
        ] = hub.tool.aws.budgets.conversion_utils.convert_raw_budget_action_to_present(
            ctx, raw_resource=before["ret"]["Action"], idem_resource_name=name
        )
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.budgets.budget_action", name=name
        )
        return result
    else:
        result[
            "old_state"
        ] = hub.tool.aws.budgets.conversion_utils.convert_raw_budget_action_to_present(
            ctx, raw_resource=before["ret"]["Action"], idem_resource_name=name
        )
        ret = await hub.exec.boto3.client.budgets.delete_budget_action(
            ctx, AccountId=account_id, BudgetName=budget_name, ActionId=resource_id
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.budgets.budget_action", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Lists the AWS Budget Actions.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.budgets.budget_action
    """
    result = {}

    account_details = await hub.exec.boto3.client.sts.get_caller_identity(ctx)
    account_id = account_details["ret"]["Account"]

    ret = await hub.exec.boto3.client.budgets.describe_budget_actions_for_account(
        ctx, AccountId=account_id
    )

    if not ret["result"]:
        hub.log.warning(f"Could not list Budget Actions {ret['comment']}")
        return {}

    for action in ret["ret"]["Actions"]:
        resource_id = action.get("ActionId")

        resource_translated = (
            hub.tool.aws.budgets.conversion_utils.convert_raw_budget_action_to_present(
                ctx,
                raw_resource=action,
                idem_resource_name=resource_id,
            )
        )
        result[resource_id] = {
            "aws.budgets.budget_action.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
