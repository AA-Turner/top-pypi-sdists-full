"""Exec module for managing EC2 FlowLogs."""
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name,
    resource_id: str = None,
    filters: List = None,
) -> Dict:
    """Get a flow_log resource from AWS.

    If more than one resource is found, the first resource returned from AWS
    will be used. The function returns None when no resource is found.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str, Optional):
            Aws flow_log id to identify the resource.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_flow_logs
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.ec2.flow_log.search_raw(
        ctx=ctx,
        name=name,
        resource_id=resource_id,
        filters=filters,
    )
    if not ret["result"]:
        if "InvalidParameterValue" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.flow_log", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["FlowLogs"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.flow_log", name=name
            )
        )
        return result

    resource = ret["ret"]["FlowLogs"][0]
    if len(ret["ret"]["FlowLogs"]) > 1:
        result["comment"].append(
            f"More than one aws.ec2.flow_log resource was found. Use resource {resource.get('FlowLogId')}"
        )
    result["ret"] = hub.tool.aws.ec2.conversion_utils.convert_raw_flow_log_to_present(
        resource
    )
    return result


async def list_(hub, ctx, name: str = None, filters: List = None) -> Dict:
    """Fetch a list of flow_logs from AWS.

    The function returns empty list when no resource is found.

    Args:
        name(str, Optional):
            The name of the Idem state.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_flow_logs
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.tool.aws.ec2.flow_log.search_raw(
        ctx=ctx,
        name=name,
        filters=filters,
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["FlowLogs"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.flow_log", name=name
            )
        )
        return result
    for flow_log in ret["ret"]["FlowLogs"]:
        result["ret"].append(
            hub.tool.aws.ec2.conversion_utils.convert_raw_flow_log_to_present(flow_log)
        )
    return result
