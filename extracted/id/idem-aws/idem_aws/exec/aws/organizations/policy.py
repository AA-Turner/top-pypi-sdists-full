"""Exec module for managing Organizations Policy."""


async def get(hub, ctx, name: str, resource_id: str):
    """Get Organization Policy from AWS.

    Provide Policy id as input.

    Args:
        name(str):
            An Idem name of the Organization policy.
        resource_id(str):
            AWS Organization policy ID

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The Organization Policy in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.organizations.policy.get name="idem_name" resource_id="resource_id"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.organizations.policy.get(
                    ctx, name=name, resource_id=resource_id
                )
    """
    result = dict(comment=[], ret=None, result=True)
    tags = []
    before = await hub.exec.boto3.client.organizations.describe_policy(
        ctx, PolicyId=resource_id
    )
    if not before["result"]:
        if "PolicyNotFoundException" in str(before["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.organizations.policy", name=name
                )
            )
            result["comment"] += list(before["comment"])
            return result
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    resource_tags = await hub.exec.boto3.client.organizations.list_tags_for_resource(
        ctx, ResourceId=resource_id
    )
    if not resource_tags["result"]:
        result["result"] = False
        result["comment"] = resource_tags["comment"]
        return result
    if before["ret"]:
        tags = resource_tags["ret"].get("Tags", [])

    result[
        "ret"
    ] = hub.tool.aws.organizations.conversion_utils.convert_raw_policy_to_present(
        before["ret"]["Policy"], tags=tags if tags else None
    )
    return result
