"""Exec module for managing Amazon Elasticache Replication Groups."""
from typing import Dict


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str,
) -> Dict:
    """Retrieves the specified AWS Elasticache Replication Group.

    Arg:
        name(str):
            An Idem name of the resource.
        resource_id(str):
            The ID of the replication group in Amazon Web Services.

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The Elasticache Replication Group in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.elasticache.replication_group.get name="idem_name" resource_id="resource_id"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.elasticache.replication_group.get(
                    ctx, name=name, resource_id=resource_id
                )
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.elasticache.describe_replication_groups(
        ctx=ctx,
        ReplicationGroupId=resource_id,
    )
    if not ret["result"]:
        if "ReplicationGroupNotFoundFault" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.elasticache.replication_group", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] = list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["ReplicationGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.elasticache.replication_group", name=name
            )
        )
        return result
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    resource = ret["ret"]["ReplicationGroups"][0]
    before_tag = await hub.exec.boto3.client.elasticache.list_tags_for_resource(
        ctx, ResourceName=resource.get("ARN")
    )
    if not before_tag["result"]:
        result["result"] = False
        result["comment"] += list(before_tag["comment"])
        return result
    resource["Tags"] = before_tag["ret"].get("TagList", [])
    result[
        "ret"
    ] = await hub.tool.aws.elasticache.conversion_utils.convert_raw_elasticache_replication_group_to_present_async(
        ctx, raw_resource=resource, idem_resource_name=name
    )
    return result
