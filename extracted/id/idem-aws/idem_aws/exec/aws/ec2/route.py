from typing import Any
from typing import Dict


async def get(
    hub,
    ctx,
    *,
    name: str,
    route_table_id: str = None,
    destination_cidr_block: str = None,
    destination_ipv6_cidr_block: str = None,
    destination_prefix_list_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Check if a route is attached to a route table.
    If resource_id is received as input search is done using only resource_id, If other parameters are specified
    they will be ignored. If resource_id is not specified then route_table_id and one of the destination should be
    specified. If more than one destination is specified search is done using only one destination in the priority order
    destination_cidr_block, destination_ipv6_cidr_block, destination_prefix_list_id

    Args:
        name(str): An Idem name of the resource
        route_table_id(str, Optional): The ID of the route table for the route.
        destination_cidr_block(str, Optional): The IPv4 CIDR address block used for the destination match. Routing decisions are based on the
            most specific match. We modify the specified CIDR block to its canonical form; for example, if
            you specify 100.68.0.18/18, we modify it to 100.68.0.0/18. Defaults to None.
        destination_ipv6_cidr_block(str, Optional): The IPv6 CIDR block used for the destination match. Routing decisions are based on the most
            specific match. Defaults to None.
        destination_prefix_list_id(str, Optional): The ID of a prefix list used for the destination match. Defaults to None.
        resource_id(str, Optional): Unique identifier to identify the route in a route table. format of resource id is
            <route_table_id>/<destination_cidr_block or destination_ipv6_cidr_block or destination_prefix_list_id>

    Returns
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The EC2 route in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.ec2.route.get name="idem_name" resource_id="resource_id"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.ec2.route.get(
                    ctx, name=name, resource_id=resource_id
                )

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.route.get
                - kwargs:
                    name: my_resource
                    resource_id: resource_id

    """
    result = dict(comment=[], result=True, ret=None)
    if resource_id:
        route_table_id, route_destination = resource_id.split("/", 1)
    elif route_table_id and (
        destination_cidr_block
        or destination_ipv6_cidr_block
        or destination_prefix_list_id
    ):
        if destination_cidr_block:
            route_destination = destination_cidr_block
        elif destination_ipv6_cidr_block:
            route_destination = destination_ipv6_cidr_block
        else:
            route_destination = destination_prefix_list_id
    else:
        result["result"] = False
        result["comment"] = [
            f"aws.ec2.route {name} either resource_id or both route table id and one of the destination"
            f" should be specified."
        ]
        return result

    ret = await hub.tool.aws.ec2.route_table.search_raw(
        ctx=ctx, resource_id=route_table_id
    )
    if not ret["result"]:
        if "InvalidRouteTableID.NotFound" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.route", name=name
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
                resource_type="aws.ec2.route", name=name
            )
        )
        return result

    resource = ret["ret"]["RouteTables"][0]
    routes_associated_with_route_table = resource["Routes"]
    route_found = None
    for route in routes_associated_with_route_table:
        if route["State"] == "active":
            if (
                "DestinationCidrBlock" in route
                and route_destination == route["DestinationCidrBlock"]
            ):
                route_found = route
                break
            elif (
                "DestinationIpv6CidrBlock" in route
                and route_destination == route["DestinationIpv6CidrBlock"]
            ):
                route_found = route
                break
            elif (
                "DestinationPrefixListId" in route
                and route_destination == route["DestinationPrefixListId"]
            ):
                route_found = route
                break

    if route_found:
        result["ret"] = hub.tool.aws.ec2.conversion_utils.convert_raw_route_to_present(
            raw_resource=route_found,
            route_table_id=route_table_id,
            idem_resource_name=name,
        )
    else:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.route", name=name
            )
        )
    return result
