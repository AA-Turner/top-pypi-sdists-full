from collections import OrderedDict
from typing import Any
from typing import Dict


async def update_budget(
    hub,
    ctx,
    account_id: str,
    before: Dict[str, Any],
    budget_limit: Dict[str, Any],
    planned_budget_limits: Dict[str, Any],
    cost_filters: Dict[str, Any],
    cost_types: Dict[str, Any],
    time_unit: str,
    time_period: Dict[str, Any],
    budget_type: str,
    auto_adjust_data: Dict[str, Any],
):
    """
    Updates a budget. You can change every part of a budget except for the budgetName
    and the calculatedSpend. When you modify a budget, the calculatedSpend drops to zero
    until Amazon Web Services has new usage data to use for forecasting.
    Args:
        hub: hub
        ctx: ctx
        account_id(str): AWS account id
        before: existing budget resource
        budget_limit(Dict[str, Any]): The total amount of cost that you want to track with your budget.
        planned_budget_limits(Dict[str, Any]): A map containing multiple BudgetLimit , including current or future limits.
        cost_filters(Dict[str, Any]): The cost filters, such as Region , Service , member account , Tag , or Cost Category , that are applied to a budget.
        cost_types(Dict[str, Any]): The types of costs that are included in this COST budget.
        time_unit(str): The length of time until a budget resets the actual and forecasted spend.
        time_period(Dict[str, Any]): The period of time that's covered by a budget. You set the start date and end date.
        budget_type(str): Specifies whether this budget tracks costs, usage, RI utilization, RI coverage, Savings Plans utilization, or Savings Plans coverage.
        auto_adjust_data(Dict[str, Any]): The parameters that determine the budget amount for an auto-adjusting budget.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": None}
    """

    result = dict(comment=[], result=True, ret=None)

    # certain params are required in payload even if those are not changed.
    update_payload = {}
    payload = {}

    if budget_limit:
        payload["BudgetLimit"] = budget_limit
        if budget_limit != before.get("budget_limit"):
            update_payload["BudgetLimit"] = budget_limit

    if planned_budget_limits:
        payload["PlannedBudgetLimits"] = planned_budget_limits
        if planned_budget_limits != before.get("planned_budget_limits"):
            update_payload["PlannedBudgetLimits"] = planned_budget_limits

    if cost_types and cost_types != before.get("cost_types"):
        update_payload["CostTypes"] = cost_types
        payload["CostTypes"] = cost_types

    if time_period and (
        time_period["Start"] != before.get("time_period")["Start"]
        or time_period["End"] != before.get("time_period")["End"]
    ):
        update_payload["TimePeriod"] = time_period
        payload["TimePeriod"] = time_period

    if auto_adjust_data:
        payload["AutoAdjustData"] = auto_adjust_data
        if auto_adjust_data != before.get("auto_adjust_data"):
            update_payload["AutoAdjustData"] = auto_adjust_data

    # below params are mandatory, required in payload even if not changed.
    if cost_filters and cost_filters != before.get("cost_filters"):
        update_payload["CostFilters"] = cost_filters
    payload["CostFilters"] = cost_filters

    if time_unit and time_unit != before.get("time_unit"):
        update_payload["TimeUnit"] = time_unit
    payload["TimeUnit"] = time_unit

    if budget_type and budget_type != before.get("budget_type"):
        update_payload["BudgetType"] = budget_type
    payload["BudgetType"] = budget_type

    payload["BudgetName"] = before.get("budget_name")

    if update_payload:
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.budgets.update_budget(
                ctx,
                AccountId=account_id,
                NewBudget=payload,
            )
            if not update_ret["result"]:
                result["comment"] += update_ret["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.budgets.budget", name=before.get("budget_name")
            )
        result["ret"] = {}
        result = update_result(result, update_payload)

    return result


def update_result(
    result: Dict[str, Any], update_payload: Dict[str, Any]
) -> Dict[str, Any]:
    parameters = OrderedDict(
        {
            "BudgetLimit": "budget_limit",
            "PlannedBudgetLimits": "planned_budget_limits",
            "CostFilters": "cost_filters",
            "CostTypes": "cost_types",
            "TimeUnit": "time_unit",
            "TimePeriod": "time_period",
            "BudgetType": "budget_type",
            "AutoAdjustData": "auto_adjust_data",
        }
    )

    for raw_parameter, present_parameter in parameters.items():
        if raw_parameter in update_payload:
            result["ret"][present_parameter] = update_payload[raw_parameter]
            result["comment"] += [
                f"Update {present_parameter}: {update_payload[raw_parameter]}"
            ]
    return result
