from collections import OrderedDict
from datetime import timezone
from typing import Any
from typing import Dict


UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


async def convert_raw_budget_to_present_async(
    hub, ctx, account_id: str, raw_resource: Dict[str, Any], idem_resource_name: str
) -> Dict[str, Any]:
    resource_id = raw_resource.get("BudgetName")
    resource_parameters = OrderedDict(
        {
            "BudgetName": "budget_name",
            "BudgetLimit": "budget_limit",
            "CostFilters": "cost_filters",
            "CostTypes": "cost_types",
            "TimeUnit": "time_unit",
            "TimePeriod": "time_period",
            "CalculatedSpend": "calculated_spend",
            "ForecastedSpend": "forecasted_spend",
            "BudgetType": "budget_type",
        }
    )

    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if "TimePeriod" in raw_resource:
        local_start_time = raw_resource.get("TimePeriod")["Start"].astimezone()
        start_time = local_start_time.astimezone(timezone.utc).strftime(UTC_FORMAT)
        resource_translated["time_period"]["Start"] = start_time

        local_end_time = raw_resource.get("TimePeriod")["End"].astimezone()
        end_time = local_end_time.astimezone(timezone.utc).strftime(UTC_FORMAT)
        resource_translated["time_period"]["End"] = end_time

    ret_tag = await hub.exec.boto3.client.budgets.describe_notifications_for_budget(
        ctx, AccountId=account_id, BudgetName=resource_id
    )
    if ret_tag["result"]:
        notifications = ret_tag["ret"]["Notifications"]
        if notifications:
            resource_translated["notifications_with_subscribers"] = []
            for notification in notifications:
                ret_sub = await hub.exec.boto3.client.budgets.describe_subscribers_for_notification(
                    ctx,
                    AccountId=account_id,
                    BudgetName=resource_id,
                    Notification=notification,
                )
                notification_with_subscriber = {
                    "Notification": notification,
                    "Subscribers": ret_sub["ret"]["Subscribers"],
                }
                resource_translated["notifications_with_subscribers"].append(
                    notification_with_subscriber
                )

    return resource_translated


def convert_raw_budget_action_to_present(
    hub, ctx, raw_resource: Dict[str, Any], idem_resource_name: str
) -> Dict[str, Any]:
    resource_id = raw_resource.get("ActionId")
    resource_parameters = OrderedDict(
        {
            "BudgetName": "budget_name",
            "NotificationType": "notification_type",
            "ActionType": "action_type",
            "ActionThreshold": "action_threshold",
            "Definition": "definition",
            "ExecutionRoleArn": "execution_role_arn",
            "ApprovalModel": "approval_model",
            "Subscribers": "subscribers",
        }
    )

    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated
