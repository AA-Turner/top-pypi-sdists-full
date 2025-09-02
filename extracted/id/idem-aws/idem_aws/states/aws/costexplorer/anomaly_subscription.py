"""State module for managing Amazon anomaly subscription."""
import copy
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    monitor_arn_list: List,
    subscribers: List,
    threshold: float,
    frequency: str,
    subscription_name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Adds a subscription to a cost anomaly detection monitor.

    You can use each subscription to define subscribers with email or SNS notifications.
    Email subscribers can set a dollar threshold and a time frequency for receiving notifications.

    Args:
        name (str):
            An Idem name of the resource - The name for the subscription.
        AnomalySubscription (dict)
            The cost anomaly subscription object that you want to create.
                * MonitorArnList (list)
                    An Idem list of cost anomaly monitors.
                * Subscribers (list)
                    A list of subscribers to notify.
                        * (dict)
                            The recipient of AnomalySubscription notifications.
                                * Address (str)
                                    The email address or SNS Amazon Resource Name (ARN). This depends on the Type .
                                * Type (str)
                                    The notification delivery channel.
                                * Status (str)
                                    Indicates if the subscriber accepts the notifications.
                * Threshold (float)
                    The dollar value that triggers a notification if the threshold is exceeded.
                * Frequency (str)
                    The frequency that anomaly reports are sent over email.
                * SubscriptionName (str)
                    The name for the subscription.
        resource_id (str, Optional):
            Subscription ARN to identify the resource

    Request Syntax:
      .. code-block:: sls

        [subscription_name]:
          aws.costexplorer.anomaly_subscription.present:
            - resource_id: "string"
            - monitor_arn_list: list
            - subscribers:
                - Address: "string"
                  Status: "string"
                  Type: "string"
            - threshold: float
            - frequency: "string"
            - subscription_name: "string"

    Returns:
        Dict[str, str]

    Examples:
      .. code-block:: sls

        arn:aws:ce::12345678910:anomalysubscription/12345678-1234-1234-1234-1234567891011:
          aws.costexplorer.anomaly_subscription.present:
            - resource_id: arn:aws:ce::12345678910:anomalysubscription/12345678-1234-1234-1234-1234567891011
            - monitor_arn_list:
                - arn:aws:ce::12345678910:anomalymonitor/12345678-1234-1234-1234-1234567891011
            - subscribers:
                - Address: abc@email.com
                  Status: CONFIRMED
                  Type: EMAIL
            - threshold: 10.0
            - frequency: DAILY
            - subscription_name: test_subscription
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    before = None

    if resource_id:
        before = await hub.exec.boto3.client.ce.get_anomaly_subscriptions(
            ctx, SubscriptionArnList=[resource_id]
        )
        if not before["result"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        if before["result"] and before["ret"].get("AnomalySubscriptions"):
            before = before["ret"]["AnomalySubscriptions"][0]
        else:
            before = None

    if before:
        result[
            "old_state"
        ] = hub.tool.aws.costexplorer.conversion_utils.convert_raw_subscription_to_present(
            ctx,
            raw_resource=before,
            idem_resource_name=name,
        )
        plan_state = copy.deepcopy(result["old_state"])

        update_ret = await hub.tool.aws.costexplorer.anomaly_subscription.update_anomaly_subscription(
            ctx,
            before=before,
            subscription_arn=resource_id,
            threshold=threshold,
            frequency=frequency,
            monitor_arn_list=monitor_arn_list,
            subscribers=subscribers,
            subscription_name=subscription_name,
        )

        result["comment"] += update_ret["comment"]
        result["result"] = update_ret["result"]
        resource_updated = resource_updated or bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            for key, value in update_ret["ret"].items():
                plan_state[key] = value
        if not resource_updated:
            result["comment"] += [
                f"aws.costexplorer.anomaly_subscription {name} already exists"
            ]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "monitor_arn_list": monitor_arn_list,
                    "subscribers": subscribers,
                    "threshold": threshold,
                    "frequency": frequency,
                    "subscription_name": subscription_name,
                },
            )
            result["comment"] += [
                f"Would create aws.costexplorer.anomaly_subscription {name}"
            ]
            return result

        anomaly_subscription = {
            "MonitorArnList": monitor_arn_list,
            "Subscribers": subscribers,
            "Threshold": threshold,
            "Frequency": frequency,
            "SubscriptionName": subscription_name,
        }
        ret = await hub.exec.boto3.client.ce.create_anomaly_subscription(
            ctx, AnomalySubscription=anomaly_subscription
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] += [f"Created aws.costexplorer.anomaly_subscription '{name}'"]
        resource_id = ret["ret"]["SubscriptionArn"]

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.boto3.client.ce.get_anomaly_subscriptions(
                ctx, SubscriptionArnList=[resource_id]
            )
            result[
                "new_state"
            ] = hub.tool.aws.costexplorer.conversion_utils.convert_raw_subscription_to_present(
                ctx,
                raw_resource=after["ret"]["AnomalySubscriptions"][0],
                idem_resource_name=name,
            )
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes a cost anomaly subscription.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            Subscription ARN to identify the resource

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.costexplorer.anomaly_subscription.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.costexplorer.anomaly_subscription", name=name
        )
        return result

    before = await hub.exec.boto3.client.ce.get_anomaly_subscriptions(
        ctx, SubscriptionArnList=[resource_id]
    )
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    if before["result"] and before["ret"].get("AnomalySubscriptions"):
        before = before["ret"]["AnomalySubscriptions"][0]
    else:
        before = None

    if not before:
        result["comment"] += [
            f"aws.costexplorer.anomaly_subscription '{name}' already absent"
        ]
    else:
        result[
            "old_state"
        ] = hub.tool.aws.costexplorer.conversion_utils.convert_raw_subscription_to_present(
            ctx,
            raw_resource=before,
            idem_resource_name=name,
        )
        if ctx.get("test", False):
            result["comment"] += [
                f"Would delete aws.costexplorer.anomaly_subscription {name}"
            ]
            return result
        else:
            ret = await hub.exec.boto3.client.ce.delete_anomaly_subscription(
                ctx, SubscriptionArn=resource_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result

            result["comment"] += [
                f"Deleted aws.costexplorer.anomaly_subscription '{name}'"
            ]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Retrieves the cost anomaly subscription objects for the account.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.costexplorer.anomaly_subscription
    """
    result = {}

    ret = await hub.exec.boto3.client.ce.get_anomaly_subscriptions(ctx)

    if not ret["result"]:
        hub.log.warning(
            f"Could not describe cost anomaly subscriptions {ret['comment']}"
        )
        return {}

    for subscription in ret["ret"]["AnomalySubscriptions"]:
        resource_id = subscription.get("SubscriptionArn")

        resource_translated = hub.tool.aws.costexplorer.conversion_utils.convert_raw_subscription_to_present(
            ctx, raw_resource=subscription, idem_resource_name=resource_id
        )

        result[resource_translated["resource_id"]] = {
            "aws.costexplorer.anomaly_subscription.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
