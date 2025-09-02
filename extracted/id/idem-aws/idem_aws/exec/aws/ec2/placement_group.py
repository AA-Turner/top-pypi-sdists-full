"""Exec module for managing EC2 placement groups."""
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
    """Get an EC2 placement group resource from AWS. Supply one of the inputs as the filter.

    Get a placement group by either resource_id (GroupName) or filters.

    Args:
        name(str):
            The name of the Idem state and the GroupName of the placement group.
        resource_id(str, Optional):
            AWS placement group group name to identify the resource.
        filters(list, Optional):
            One or more filters: for example, ``tag:<key>``, ``tag-key``.
            A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_placement_groups

    Request Syntax:
        .. code-block:: bash

            $ idem exec aws.ec2.placement_group.get name=string resouce_id=string filters=list

    Returns:
        Dict

    Examples:
        .. code-block:: bash

            $ idem exec aws.ec2.placement_group.get name=idem_placement_group_name
            $ idem exec aws.ec2.placement_group.get name=null resource_id=my_placement_group
            $ idem exec aws.ec2.placement_group.get name=null filters="[{'name': 'group-name', 'values':['my_placement_group']}]"
    """
    result = dict(comment=[], ret=None, result=True)

    ret = await hub.tool.aws.ec2.placement_group.search_raw(
        ctx=ctx,
        filters=filters,
        resource_id=resource_id,
    )

    if not ret["result"]:
        if "InvalidPlacementGroup.Unknown" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.placement_group", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["PlacementGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.placement_group", name=name
            )
        )
        return result

    resource = ret["ret"]["PlacementGroups"][0]
    if len(ret["ret"]["PlacementGroups"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type="aws.ec2.placement_group", resource_id=resource_id
            )
        )
    result[
        "ret"
    ] = hub.tool.aws.ec2.conversion_utils.convert_raw_placement_group_to_present(
        raw_resource=resource
    )
    return result


async def list_(hub, ctx, name: str = None, filters: List = None) -> Dict:
    """Get a list of EC2 placement group resources from AWS. Supply one of the inputs as the filter.

    Get a list of placement groups by idem name (group name) or filters.

    Args:
        name(str, Optional):
            The name of the Idem state.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key.
            A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_placement_groups

    Request Syntax:
        .. code-block:: bash

            $ idem exec aws.ec2.placement_group.get name=string filters=list

    Returns:
        Dict

    Examples:
        .. code-block:: bash

            $ idem exec aws.ec2.placement_group.get name=idem_placement_group_name
            $ idem exec aws.ec2.placement_group.get name=null filters="[{'name': 'group-name', 'values':['my_placement_group']}]"
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.tool.aws.ec2.placement_group.search_raw(
        ctx=ctx,
        filters=filters,
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["PlacementGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.placement_group", name=name
            )
        )
        return result
    for placement_group in ret["ret"]["PlacementGroups"]:
        result["ret"].append(
            hub.tool.aws.ec2.conversion_utils.convert_raw_placement_group_to_present(
                raw_resource=placement_group
            )
        )
    return result
