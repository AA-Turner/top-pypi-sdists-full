"""State module for managing AWS Budgets."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    budget_name: str,
    time_unit: str,
    budget_type: str,
    budget_limit: make_dataclass("Spend", [("Amount", str), ("Unit", str)]) = None,
    planned_budget_limits: Dict[
        str, make_dataclass("Spend", [("Amount", str), ("Unit", str)])
    ] = None,
    cost_filters: Dict[str, List[str]] = None,
    cost_types: make_dataclass(
        "CostTypes",
        [
            ("IncludeTax", bool, field(default=None)),
            ("IncludeSubscription", bool, field(default=None)),
            ("UseBlended", bool, field(default=None)),
            ("IncludeRefund", bool, field(default=None)),
            ("IncludeCredit", bool, field(default=None)),
            ("IncludeUpfront", bool, field(default=None)),
            ("IncludeRecurring", bool, field(default=None)),
            ("IncludeOtherSubscription", bool, field(default=None)),
            ("IncludeSupport", bool, field(default=None)),
            ("IncludeDiscount", bool, field(default=None)),
            ("UseAmortized", bool, field(default=None)),
        ],
    ) = None,
    time_period: make_dataclass(
        "TimePeriod",
        [
            ("Start", datetime, field(default=None)),
            ("End", datetime, field(default=None)),
        ],
    ) = None,
    auto_adjust_data: make_dataclass(
        "AutoAdjustData",
        [
            ("AutoAdjustType", str),
            (
                "HistoricalOptions",
                make_dataclass(
                    "HistoricalOptions",
                    [
                        ("BudgetAdjustmentPeriod", int),
                        ("LookBackAvailablePeriods", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("LastAutoAdjustTime", str, field(default=None)),
        ],
    ) = None,
    notifications_with_subscribers: List[
        make_dataclass(
            "NotificationWithSubscribers",
            [
                (
                    "Notification",
                    make_dataclass(
                        "Notification",
                        [
                            ("NotificationType", str),
                            ("ComparisonOperator", str),
                            ("Threshold", float),
                            ("ThresholdType", str, field(default=None)),
                            ("NotificationState", str, field(default=None)),
                        ],
                    ),
                ),
                (
                    "Subscribers",
                    List[
                        make_dataclass(
                            "Subscriber", [("SubscriptionType", str), ("Address", str)]
                        )
                    ],
                ),
            ],
        )
    ] = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Creates an AWS Budget and, if included, notifications and subscribers.

    Args:
        name(str):
            An Idem name of the AWS Budget.
        resource_id(str):
            Resource ID to identify the AWS Budget.
        budget_name(str):
            The name of a budget. The name must be unique within an account. The ":" and "\\" characters aren't allowed
            in `budget_name`.
        time_unit(str):
            The length of time until a budget resets the actual and forecasted spend.
            'DAILY'|'MONTHLY'|'QUARTERLY'|'ANNUALLY'
        budget_type(str):
            Specifies whether this budget tracks costs, usage, RI utilization, RI coverage, Savings Plans utilization,
            or Savings Plans coverage.
        budget_limit(dict, Optional):
            The total amount of cost, usage, RI utilization, RI coverage, Savings Plans utilization, or Savings Plans
            coverage that you want to track with your budget.

            `budget_limit` is required for cost or usage budgets, but optional for RI or Savings Plans utilization
            or coverage budgets. RI and Savings Plans utilization or coverage budgets default to `100`. This is the
            only valid value for RI or Savings Plans utilization or coverage budgets. You can't use `budget_limit`
            with `planned_budget_limits` for `CreateBudget` and `UpdateBudget actions`.

            * Amount (str): The cost or usage amount that's associated with a budget forecast, actual spend, or budget threshold.
            * Unit (str): The unit of measurement that's used for the budget forecast, actual spend, or budget threshold, such as USD or GBP.
        planned_budget_limits(dict[str, Any], Optional):
            A map containing multiple `budget_limit`, including current or future limits.

            `planned_budget_limits` is available for cost or usage budget and supports both monthly and quarterly
            `time_unit`.

            For monthly budgets, provide 12 months of PlannedBudgetLimits values. This must start from the current
            month and include the next 11 months. The key is the start of the month, UTC in epoch seconds.

            For quarterly budgets, provide four quarters of PlannedBudgetLimits value entries in standard calendar
            quarter increments. This must start from the current quarter and include the next three quarters. The key
            is the start of the quarter, UTC in epoch seconds.

            If the planned budget expires before 12 months for monthly or four quarters for quarterly, provide the
            PlannedBudgetLimits values only for the remaining periods. If the budget begins at a date in the future,
            provide PlannedBudgetLimits values from the start date of the budget. After all the budget_limit values in
            planned_budget_limits are used, the budget continues to use the last limit as the budget_limit. At that point,
            the planned budget provides the same experience as a fixed budget.

            The amount of cost or usage that's measured for a budget.

            * Amount (str): The cost or usage amount that's associated with a budget forecast, actual spend, or budget
            threshold.

            * Unit (str): The unit of measurement that's used for the budget forecast, actual spend, or budget threshold,
            such as USD or GBP.
        cost_filters(dict[str, list[str]], Optional):
            The cost filters, such as Region , Service , member account , Tag , or Cost Category , that are applied to
            a budget.

            Amazon Web Services Budgets supports the following services as a Service filter for RI budgets:
              * Amazon EC2
              * Amazon Redshift
              * Amazon Relational Database Service
              * Amazon ElasticCache
              * Amazon OpenSearch Service
        cost_types(dict[str, Any], Optional):
            The types of costs that are included in this COST budget.

            USAGE, RI_UTILIZATION, RI_COVERAGE, SAVINGS_PLANS_UTILIZATION, and SAVINGS_PLANS_COVERAGE budgets do
            not have `cost_types`.

            * IncludeTax (bool, Optional): Specifies whether a budget includes taxes. The default value is true.
            * IncludeSubscription (bool, Optional): Specifies whether a budget includes subscriptions. The default value is true.
            * UseBlended (bool, Optional): Specifies whether a budget uses a blended rate. The default value is false.
            * IncludeRefund (bool, Optional): Specifies whether a budget includes refunds. The default value is true.
            * IncludeCredit (bool, Optional): Specifies whether a budget includes credits. The default value is true.
            * IncludeUpfront (bool, Optional): Specifies whether a budget includes upfront RI costs. The default value is true.
            * IncludeRecurring (bool, Optional): Specifies whether a budget includes recurring fees such as monthly RI
                fees. The default value is true.
            * IncludeOtherSubscription (bool, Optional): Specifies whether a budget includes non-RI subscription costs.
                The default value is true.
            * IncludeSupport (bool, Optional): Specifies whether a budget includes support subscription fees. The
                default value is true.
            * IncludeDiscount (bool, Optional): Specifies whether a budget includes discounts. The default value is true.
            * UseAmortized (bool, Optional): Specifies whether a budget uses the amortized rate. The default value is false.

        time_period (dict[str, Any], Optional):
            The period of time that's covered by a budget. You set the start date and end date. The start
            date must come before the end date. The end date must come before `06/15/87 00:00 UTC`.

            If you create your budget and don't specify a start date, Amazon Web Services defaults to the start of
            your chosen time period (DAILY, MONTHLY, QUARTERLY, or ANNUALLY). For example, if you created
            your budget on January 24, 2018, chose `DAILY`, and didn't set a start date, Amazon Web Services
            set your start date to `01/24/18 00:00 UTC`. If you chose `MONTHLY`, Amazon Web Services set your
            start date to `01/01/18 00:00 UTC`. If you didn't specify an end date, Amazon Web Services set
            your end date to `06/15/87 00:00 UTC`. The defaults are the same for the Billing and Cost
            Management console and the API.

            You can change either date with the `UpdateBudget` operation. After the end date, Amazon Web Services deletes
            the budget and all the associated notifications and subscribers.

            * Start (datetime, Optional):
                The start date for a budget. If you created your budget and didn't specify a start date, Amazon
                Web Services defaults to the start of your chosen time period (DAILY, MONTHLY, QUARTERLY, or
                ANNUALLY). For example, if you created your budget on January 24, 2018, chose `DAILY`, and didn't
                set a start date, Amazon Web Services set your start date to `01/24/18 00:00 UTC`. If you chose
                `MONTHLY`, Amazon Web Services set your start date to `01/01/18 00:00 UTC`. The defaults are the
                same for the Billing and Cost Management console and the API. You can change your start date with the
                `UpdateBudget` operation.

            * End (datetime, Optional):
                The end date for a budget. If you didn't specify an end date, Amazon Web Services set your end date to
                `06/15/87 00:00 UTC`. The defaults are the same for the Billing and Cost Management console and the API.

                After the end date, Amazon Web Services deletes the budget and all the associated notifications and
                subscribers. You can change your end date with the `UpdateBudget` operation.
        auto_adjust_data (dict[str, Any], Optional):
            The parameters that determine the budget amount for an auto-adjusting budget.

            * AutoAdjustType (str):
                The string that defines whether your budget auto-adjusts based on historical or forecasted data.

            * HistoricalOptions (dict[str, Any], Optional):
                The parameters that define or describe the historical data that your auto-adjusting budget is based on.

                * BudgetAdjustmentPeriod (int):
                    The number of budget periods included in the moving-average calculation that determines your
                    auto-adjusted budget amount.
                    The maximum value depends on the `time_unit` granularity of the budget:

                    * For the `DAILY` granularity, the maximum value is `60`.
                    * For the `MONTHLY` granularity, the maximum value is `12`.
                    * For the `QUARTERLY` granularity, the maximum value is `4`.
                    * For the `ANNUALLY` granularity, the maximum value is `1`.

                * LookBackAvailablePeriods (int):
                    The integer that describes how many budget periods in your `BudgetAdjustmentPeriod` are included in
                    the calculation of your current `BudgetLimit`. If the first budget period in your
                    `BudgetAdjustmentPeriod` has no cost data, then that budget period isn’t included in the average
                    that determines your budget limit.

                    For example, if you set `BudgetAdjustmentPeriod` as `4` quarters, but your account had no cost data
                    in the first quarter, then only the last three quarters are included in the calculation. In this
                    scenario, `LookBackAvailablePeriods` returns `3`.

                    You can’t set your own LookBackAvailablePeriods. The value is automatically calculated from the
                    BudgetAdjustmentPeriod and your historical cost data.

            * LastAutoAdjustTime (datetime):
                The last time that your budget was auto-adjusted.

        notifications_with_subscribers(list[dict[str, Any]], Optional):
            A notification that you want to associate with a budget. A budget can have up to five notifications, and
            each notification can have one SNS subscriber and up to 10 email subscribers. If you include notifications
            and subscribers in your CreateBudget call, Amazon Web Services creates the notifications and subscribers
            for you.

            A notification with subscribers can have one SNS subscriber and up to 10 email subscribers, for a total of
            11 subscribers.

            * Notification (dict[str, Any]): The notification that's associated with a budget.

                * NotificationType (str):
                    Specifies whether the notification is for how much you have spent (ACTUAL) or for how much that
                    you're forecasted to spend (FORECASTED).

                * ComparisonOperator (str): The comparison that's used for this notification.

                * Threshold (float):
                    The threshold that's associated with a notification. Thresholds are always a percentage, and many
                    customers find value being alerted between 50% - 200% of the budgeted amount. The maximum limit for
                    your threshold is 1,000,000% above the budgeted amount.

                * ThresholdType (str):
                    The type of threshold for a notification. For `ABSOLUTE_VALUE` thresholds, Amazon Web Services
                    notifies you when you go over or are forecasted to go over your total cost threshold. For
                    `PERCENTAGE` thresholds, Amazon Web Services notifies you when you go over or are forecasted to go
                    over a certain percentage of your forecasted spend. For example, if you have a budget for 200
                    dollars, and you have a `PERCENTAGE` threshold of 80%, Amazon Web Services notifies you when you go
                    over 160 dollars.

                * NotificationState (str):
                    Specifies whether this notification is in alarm. If a budget notification is in the `ALARM` state,
                    you passed the set threshold for the budget.

            * Subscribers (list[dict[str, Any]]):
                A list of subscribers who are subscribed to this notification.

                The subscriber to a budget notification consists of a subscription type and either an Amazon SNS topic
                or an email address.

                For example, an email subscriber has the following parameters:
                  * A `subscriptionType` of `EMAIL`
                  * An `address` of `example@example.com`

                * SubscriptionType (str): The type of notification that Amazon Web Services sends to a subscriber.

                * Address (str):
                    The address that Amazon Web Services sends budget notifications to, either an SNS topic or an email.
                    When you create a subscriber, the value of `Address` can't contain line breaks.


    Request Syntax:
      .. code-block:: sls

        [budget-resource-id]:
          aws.budgets.budget.present:
            - resource_id: "string"
            - budget_name: "string"
            - time_unit: "string"
            - budget_type: "string"
            - budget_limit: "dict"
            - cost_filters: "dict"
            - cost_types: "dict"
            - time_period: "dict"
            - auto_adjust_data: "dict"
            - notifications_with_subscribers: "dict"

    Returns:
        Dict[str, str]

    Examples:
        .. code-block:: sls

            cost_budget1234:
              aws.budgets.budget.present:
                - budget_name: new-test-budget
                - budget_limit:
                    Amount: "700.0"
                    Unit: USD
                - cost_filters: {}
                - cost_types:
                    IncludeCredit: false
                    IncludeDiscount: true
                    IncludeOtherSubscription: true
                    IncludeRecurring: true
                    IncludeRefund: false
                    IncludeSubscription: true
                    IncludeSupport: true
                    IncludeTax: true
                    IncludeUpfront: true
                    UseAmortized: false
                    UseBlended: false
                - time_unit: MONTHLY
                - time_period:
                    End: 2087-06-15 05:30:00+05:30
                  Start: 2022-06-01 05:30:00+05:30
              - budget_type: COST

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    account_details = await hub.exec.boto3.client.sts.get_caller_identity(ctx)
    account_id = account_details["ret"]["Account"]
    resource_updated = False

    budget_parameters = {
        "BudgetName": budget_name,
        "CostFilters": cost_filters,
        "CostTypes": cost_types,
        "TimeUnit": time_unit,
        "TimePeriod": time_period,
        "BudgetType": budget_type,
    }

    if budget_limit:
        budget_parameters["BudgetLimit"] = budget_limit
    else:
        budget_parameters["PlannedBudgetLimits"] = planned_budget_limits
    if auto_adjust_data:
        budget_parameters["AutoAdjustData"] = auto_adjust_data

    if resource_id:
        before = await hub.exec.aws.budgets.budget.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.budgets.budget", name=name
        )
        result["old_state"] = copy.deepcopy(before["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])

        update_ret = await hub.tool.aws.budgets.budget.update_budget(
            ctx,
            account_id=account_id,
            before=before["ret"],
            budget_limit=budget_limit,
            planned_budget_limits=planned_budget_limits,
            cost_filters=cost_filters,
            cost_types=cost_types,
            time_unit=time_unit,
            time_period=time_period,
            budget_type=budget_type,
            auto_adjust_data=auto_adjust_data,
        )
        result["comment"] += update_ret["comment"]
        if not update_ret["result"]:
            result["result"] = False
            return result

        resource_updated = resource_updated or bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            result["new_state"].update(update_ret["ret"])
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.budgets.budget", name=name
            )
        if resource_updated and ctx.get("test", False):
            return result

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": budget_name,
                    "budget_name": budget_name,
                    "budget_limit": budget_limit,
                    "cost_filters": cost_filters,
                    "cost_types": cost_types,
                    "time_unit": time_unit,
                    "time_period": time_period,
                    "budget_type": budget_type,
                    "auto_adjust_data": auto_adjust_data,
                    "notifications_with_subscribers": notifications_with_subscribers,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.budgets.budget", name=name
            )
            return result
        create_ret = await hub.exec.boto3.client.budgets.create_budget(
            ctx,
            AccountId=account_id,
            Budget=budget_parameters,
            NotificationsWithSubscribers=notifications_with_subscribers,
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] = create_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.budgets.budget", name=name
        )
        resource_id = budget_name

    if (not result["old_state"]) or resource_updated:
        after_ret = await hub.exec.aws.budgets.budget.get(
            ctx, name=name, resource_id=resource_id
        )
        if not after_ret["result"] or not after_ret["ret"]:
            result["result"] = False
            result["comment"] += after_ret["comment"]
            return result
        result["new_state"] = after_ret["ret"]

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes an AWS Budget.

    Args:
        name(str): An Idem name of the AWS Budget.
        resource_id(str, Optional): Budget ID to identify the resource.
            Idem automatically considers this resource being absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            [budget-resource-id]:
              aws.budgets.budget.absent:
                - name: value
                - resource_id: value

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.budgets.budget.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    account_details = await hub.exec.boto3.client.sts.get_caller_identity(ctx)
    account_id = account_details["ret"]["Account"]

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.budgets.budget", name=name
        )
        return result

    before = await hub.exec.aws.budgets.budget.get(
        ctx, name=name, resource_id=resource_id
    )

    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.budgets.budget", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.budgets.budget", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        delete_ret = await hub.exec.boto3.client.budgets.delete_budget(
            ctx, AccountId=account_id, BudgetName=name
        )
        if not delete_ret["result"]:
            result["result"] = False
            result["comment"] = delete_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.budgets.budget", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Lists the AWS Budgets that are associated with an account.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.budgets.budget
    """
    result = {}
    ret = await hub.exec.aws.budgets.budget.list(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe budgets {ret['comment']}")
        return {}

    for budget in ret["ret"]:
        resource_id = budget.get("resource_id")
        result[resource_id] = {
            "aws.budgets.budget.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in budget.items()
            ]
        }
    return result
