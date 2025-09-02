from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, name, resource_id: str = None, filters: List = None):
    """
    Get a single route table from AWS. If more than one resource is found, the first resource returned from AWS will be used.

    The function returns None when no resource is found.

    Args:
        name(str):
            An Idem state name.

        resource_id(str, Optional):
            AWS route table ID to identify the resource.

        filters(list[dict[str, Any]], Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_route_tables
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.ec2.route_table.search_raw(
        ctx=ctx, resource_id=resource_id, filters=filters
    )
    if not ret["result"]:
        if "InvalidRouteTableID.NotFound" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.route_table", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["RouteTables"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.route_table", name=name
            )
        )
        return result

    resource = ret["ret"]["RouteTables"][0]
    if len(ret["ret"]["RouteTables"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type="aws.ec2.route_table",
                resource_id=resource.get("RouteTableId"),
            )
        )
    result[
        "ret"
    ] = hub.tool.aws.ec2.conversion_utils.convert_raw_route_table_to_present(
        raw_resource=resource, idem_resource_name=name
    )

    return result


async def list_(hub, ctx, name: str = None, filters: List = None) -> Dict:
    """
    Fetch a list of route table from AWS. The function returns empty list when no resource is found.

    Args:
        name(str, Optional):
            An Idem state name.

        filters(list[dict[str, Any]], Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_route_tables
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.tool.aws.ec2.route_table.search_raw(ctx=ctx, filters=filters)
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["RouteTables"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.route_table", name=name
            )
        )
        return result
    for resource in ret["ret"]["RouteTables"]:
        resource_id = resource.get("RouteTableId")
        result["ret"].append(
            hub.tool.aws.ec2.conversion_utils.convert_raw_route_table_to_present(
                raw_resource=resource, idem_resource_name=resource_id
            )
        )
    return result
