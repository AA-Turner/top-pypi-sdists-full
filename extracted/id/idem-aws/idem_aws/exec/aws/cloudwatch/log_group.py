"""Exec module for managing Cloudwatch Log_Groups."""
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name,
    resource_id: str = None,
) -> Dict:
    """Get a log_group resource from AWS.

    If more than one resource is found, the first resource returned from AWS
    will be used. The function returns None when no resource is found.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str, Optional):
            Aws logGroupNamePrefix (The prefix to match.)
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.cloudwatch.log_group.search_raw(
        ctx=ctx,
        name=name,
        resource_id=resource_id,
    )
    if not ret["result"]:
        if "InvalidParameterException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.cloudwatch.log_group", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["logGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.cloudwatch.log_group", name=name
            )
        )
        return result

    resource = ret["ret"]["logGroups"][0]
    if len(ret["ret"]["logGroups"]) > 1:
        result["comment"].append(
            f"More than one aws.cloudwatch.log_group resource was found. Use resource {resource.get('logGroupName')}"
        )
    result[
        "ret"
    ] = await hub.tool.aws.cloudwatch.conversion_utils.convert_raw_log_group_to_present_async(
        ctx=ctx, raw_resource=resource, idem_resource_name=name
    )
    return result


async def list_(
    hub,
    ctx,
    name: str = None,
) -> Dict:
    """Fetch a list of log_group from AWS.
    The function returns empty list when no resource is found.

    Args:
        name (str, Optional):
            The name of the Idem state.
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.tool.aws.cloudwatch.log_group.search_raw(
        ctx=ctx,
        name=name,
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["logGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.cloudwatch.log_group", name=name
            )
        )
        return result
    for log_group in ret["ret"]["logGroups"]:
        result["ret"].append(
            await hub.tool.aws.cloudwatch.conversion_utils.convert_raw_log_group_to_present_async(
                ctx=ctx, raw_resource=log_group, idem_resource_name=name
            )
        )
    return result
