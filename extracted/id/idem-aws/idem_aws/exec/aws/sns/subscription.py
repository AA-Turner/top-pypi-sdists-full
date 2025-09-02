"""Exec module for managing SNS Subscription."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    topic_arn: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Get Subscription from either topic arn or resource id.

    Args:
        name(str):
            An Idem name of the state for logging.

        topic_arn(str, Optional):
            Topic ARN

        resource_id(str, Optional):
            Subscription ARN
    """
    result = dict(comment=[], result=True, ret=None)

    ret = await hub.exec.aws.sns.subscription.list(
        ctx, name=name, topic_arn=topic_arn, resource_id=resource_id
    )
    if not ret["result"]:
        result["result"] = False
        result["comment"] += list(ret["comment"])
        return result

    filtered = ret["ret"]
    result["comment"] = ret["comment"]

    if filtered:
        result["ret"] = filtered[0]
        if len(filtered) > 1:
            result["comment"].append(
                f"More than one aws.sns.subscription resource was found. Use resource {filtered[0].get('resource_id')}"
            )

    return result


async def list_(
    hub, ctx, name: str = None, topic_arn: str = None, resource_id: str = None
) -> Dict:
    """Use an un-managed Subscription as a data-source.

    Args:
        name(str):
            The name of the Idem state.

        topic_arn(str, Optional):
            Topic ARN

        resource_id(str, Optional):
            Subscription ARN

    """
    result = dict(comment=[], result=True, ret=[])
    ret = None
    if topic_arn:
        ret = await hub.exec.boto3.client.sns.list_subscriptions_by_topic(
            ctx, TopicArn=topic_arn
        )
        if not ret["result"]:
            if "NotFoundException" in str(ret["comment"]):
                result["comment"].append(
                    hub.tool.aws.comment_utils.get_empty_comment(
                        resource_type="aws.sns.subscription", name=name
                    )
                )
                result["comment"] += list(ret["comment"])
                return result
            result["result"] = False
            result["comment"] += list(ret["comment"])
            return result
    else:
        ret = await hub.exec.boto3.client.sns.list_subscriptions(ctx)
        if not ret["result"]:
            result["result"] = False
            result["comment"] += list(ret["comment"])
            return result
        if resource_id:
            filtered = list(
                filter(
                    lambda subs: subs["SubscriptionArn"] == resource_id,
                    ret["ret"]["Subscriptions"],
                )
            )
            ret["ret"]["Subscriptions"] = filtered

    if not ret["ret"]["Subscriptions"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.sns.subscription", name=name
            )
        )
        return result

    for subscription in ret["ret"]["Subscriptions"]:
        subscription_id = subscription.get("SubscriptionArn")

        if subscription_id == "Deleted" or subscription_id == "PendingConfirmation":
            continue

        resource = await hub.tool.boto3.resource.create(
            ctx, "sns", "Subscription", arn=subscription_id
        )
        raw_resource = await hub.tool.boto3.resource.describe(resource)

        result["ret"].append(
            hub.tool.aws.sns.conversion_utils.convert_raw_subscription_to_present(
                raw_resource=raw_resource, idem_resource_name=subscription_id
            )
        )

    return result
