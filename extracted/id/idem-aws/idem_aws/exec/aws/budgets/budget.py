"""Exec module for managing budgets."""
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, name: str, resource_id: str) -> Dict:
    """Retrieves the budget details.

    Args:
        name(str): An Idem name of the AWS Budget.
        resource_id(str): Resource ID to identify the AWS Budget.

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The AWS budget in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.budgets.budget.get name="idem_name" resource_id="budget_name"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.budgets.budget.get(
                    ctx, name=name, resource_id=resource_id
                )
    """
    result = dict(comment=[], ret=None, result=True)
    account_details = await hub.exec.boto3.client.sts.get_caller_identity(ctx)
    account_id = account_details["ret"]["Account"]
    ret = await hub.exec.boto3.client.budgets.describe_budget(
        ctx, AccountId=account_id, BudgetName=resource_id
    )
    if not ret["result"]:
        if "NotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.budgets.budget", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    result[
        "ret"
    ] = await hub.tool.aws.budgets.conversion_utils.convert_raw_budget_to_present_async(
        ctx,
        account_id=account_id,
        raw_resource=ret["ret"].get("Budget"),
        idem_resource_name=name,
    )
    return result


async def list_(
    hub,
    ctx,
) -> Dict:
    """Fetch a list of budgets from AWS.

    The function returns empty list when no resource is found.

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The AWS budget list in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.budgets.budget.list

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.budgets.budget.list(ctx)

    """
    result = dict(comment=[], ret=[], result=True)
    account_details = await hub.exec.boto3.client.sts.get_caller_identity(ctx)
    account_id = account_details["ret"]["Account"]
    ret = await hub.exec.boto3.client.budgets.describe_budgets(
        ctx, AccountId=account_id
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Budgets"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.budgets.budget", name="Budgets"
            )
        )
        return result
    for budget in ret["ret"]["Budgets"]:
        result["ret"].append(
            await hub.tool.aws.budgets.conversion_utils.convert_raw_budget_to_present_async(
                ctx,
                account_id=account_id,
                raw_resource=budget,
                idem_resource_name=budget.get("BudgetName"),
            )
        )
    return result
