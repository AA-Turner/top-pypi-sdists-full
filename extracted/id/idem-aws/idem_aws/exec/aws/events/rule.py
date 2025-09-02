"""Exec module for managing Cloudwatch Event Rule."""
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name,
    resource_id: str,
    event_bus_name: str = None,
) -> Dict:
    """Get an event rule resource.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str):
            The name of the AWS CloudWatch Events rule to identify the resource.

        event_bus_name(str, Optional):
            The name or ARN of the event bus to associate with this rule.
            If you omit this, the default event bus is used.

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": list, "ret": None|dict}

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.events.rule.get name="asg_1" resource_id="resource_id"

        Calling this exec module function from within a state module in pure python

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id):
                ret = await hub.exec.aws.events.rule.get(
                    ctx=ctx,
                    name=name,
                    resource_id=resource_id
                )

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.events.rule.get
                - kwargs:
                    name: my_resources
                    resource_id: idem-test-events-rule48f593a7-e5ff-48ee-ab30-422241a7e693
    """
    result = dict(comment=[], ret=None, result=True)

    resource_ret = await hub.exec.boto3.client.events.describe_rule(
        ctx, Name=resource_id, EventBusName=event_bus_name
    )

    if not resource_ret["result"]:
        if "ResourceNotFoundException" in str(resource_ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.events.rule", name=name
                )
            )
            result["comment"] += list(resource_ret["comment"])
            return result
        result["comment"] += list(resource_ret["comment"])
        result["result"] = False
        return result

    if not resource_ret["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.events.rule", name=name
            )
        )
        return result

    rule = resource_ret["ret"]
    tags = await hub.exec.boto3.client.events.list_tags_for_resource(
        ctx, ResourceARN=rule.get("Arn")
    )

    if not tags["result"]:
        result["result"] = False
        result["comment"] += list(tags["comment"])
        return result

    resource_converted = await hub.tool.aws.events.conversion_utils.convert_raw_cloud_watch_rule_to_present_async(
        ctx,
        raw_resource=rule,
        idem_resource_name=rule.get("Name"),
        tags=tags.get("ret").get("Tags"),
    )

    if not resource_converted["result"]:
        result["comment"] += list(resource_converted["comment"])
        result["result"] = False

    result["ret"] = resource_converted["ret"]

    return result


async def list_(hub, ctx, name: str = None) -> Dict:
    """List event rules from AWS.

    Args:
        name(str, Optional):
            The name of the Idem state.

    Returns:
        Dict[str, Any]

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.events.rule.list name="my_resources"

        Calling this exec module function from within a state module in pure python.

        .. code-block:: python

            async def state_function(hub, ctx, name):
                await hub.exec.aws.events.rule.list(
                    ctx=ctx,
                    name=name
                )

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.events.rule.list
                - kwargs:
                    name: my_resources
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.events.list_rules(ctx)
    if not ret["result"]:
        result["comment"] = list(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"]["Rules"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.events.rule", name=name
            )
        )
        return result
    result["ret"] = []

    for rule in ret["ret"]["Rules"]:
        tags = await hub.exec.boto3.client.events.list_tags_for_resource(
            ctx, ResourceARN=rule.get("Arn")
        )

        if not tags["result"]:
            hub.log.warning(
                f"Could not retrieve tags for aws.events.rule '{rule.get('Name')}' "
                f"with error {tags['comment']}"
            )
        resource_converted = await hub.tool.aws.events.conversion_utils.convert_raw_cloud_watch_rule_to_present_async(
            ctx,
            raw_resource=rule,
            idem_resource_name=rule.get("Name"),
            tags=tags.get("ret").get("Tags") if tags.get("result") else None,
        )
        if not resource_converted["result"]:
            hub.log.warning(
                f"Could not convert aws.events.rule '{rule.get('Name')}' "
                f"with error {resource_converted['comment']}"
            )
        else:
            result["ret"].append(resource_converted["ret"])

    return result
