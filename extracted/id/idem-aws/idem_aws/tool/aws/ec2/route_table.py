from typing import Any
from typing import Dict
from typing import List
from typing import Set

ALLOWED_ROUTE_DESTINATION_CIDR_BLOCKS = {
    "DestinationCidrBlock",
    "DestinationIpv6CidrBlock",
    "DestinationPrefixListId",
}

ALLOWED_ROUTE_TARGET_GATEWAYS = {
    "VpcEndpointId",
    "EgressOnlyInternetGatewayId",
    "GatewayId",
    "InstanceId",
    "NatGatewayId",
    "TransitGatewayId",
    "LocalGatewayId",
    "CarrierGatewayId",
    "NetworkInterfaceId",
    "RouteTableId",
    "VpcPeeringConnectionId",
    "CoreNetworkArn",
}

ALLOWED_DEFAULT_ROUTE_TARGET_GATEWAYS = {
    "VpcEndpointId",
    "GatewayId",
    "InstanceId",
    "NetworkInterfaceId",
}


async def search_raw(hub, ctx, resource_id: str = None, filters: List = None) -> Dict:
    """
    Fetch one or more route table from AWS. The return will be in the same format as what the boto3 api returns.

    Args:
        resource_id(str, Optional): AWS route table ID to identify the resource.
        filters(list, Optional): One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
         https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_route_tables

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}

    """
    result = dict(comment=[], ret=None, result=True)
    syntax_validation = hub.tool.aws.search_utils.search_filter_syntax_validation(
        filters=filters
    )
    if not syntax_validation["result"]:
        result["result"] = False
        result["comment"] = list(syntax_validation["comment"])
        return result
    boto3_filter = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )
    route_table_args = {}
    if boto3_filter:
        route_table_args["Filters"] = boto3_filter

    # Including None as RouteTableIds, throws ParamValidationError for describe_route_tables
    if resource_id:
        route_table_args["RouteTableIds"] = [resource_id]

    ret = await hub.exec.boto3.client.ec2.describe_route_tables(ctx, **route_table_args)
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result


def get_route_table_routes_modifications(
    hub, old_routes: List[Dict], new_routes: List[Dict]
):
    """
    Given old routes i.e, the routes of current route table and new_routes
    i.e, the routes we want to modify to, this function will compare differences between
    old and new routes and return routes to be added and removed

    Args:
        hub:
        old_routes(List):  routes of existing route table
        new_routes(List): new routes to update

    Returns:
        Dict[str, List]

    """
    result = dict(
        comment=[],
        routes_to_add=[],
        routes_to_delete=[],
        routes_to_replace=[],
        result=True,
    )
    routes_to_add = []
    routes_to_delete = []
    routes_to_replace = []
    old_routes_map = {}
    default_destination_cidr_block: str = ""
    # Creates a map of destination cidr block -> route to easily retrieve further
    for route in old_routes:
        if route.get("State") == "active":
            # Route table route allows three types of destinations
            # 1) DestinationCidrBlock,
            # 2) DestinationIpv6CidrBlock,
            # 3) DestinationPrefixListId,
            # We need to determine which type of  destination is used
            destination_cidr_key = get_common_key_in_dict(
                route, ALLOWED_ROUTE_DESTINATION_CIDR_BLOCKS
            )
            old_routes_map[route.get(destination_cidr_key)] = route
            if route.get("Origin") == "CreateRouteTable":
                default_destination_cidr_block = route.get(destination_cidr_key)
    new_destination_cidr_blocks = list()
    for new_route in new_routes:
        # Loop through new routes and determine which destination is used
        destination_cidr_key = get_common_key_in_dict(
            new_route, ALLOWED_ROUTE_DESTINATION_CIDR_BLOCKS
        )
        destination_cidr_block = new_route.get(destination_cidr_key)

        # checking for duplicate destination cidr blocks. There can be only unique destination cidr block
        if destination_cidr_block in new_destination_cidr_blocks:
            result["result"] = False
            result["comment"] = (
                "Duplicate destination cidr blocks are not allowed, they should be unique.",
            )
            return result
        else:
            new_destination_cidr_blocks.append(destination_cidr_block)
        allowed_targets = (
            ALLOWED_DEFAULT_ROUTE_TARGET_GATEWAYS
            if destination_cidr_block == default_destination_cidr_block
            else ALLOWED_ROUTE_TARGET_GATEWAYS
        )
        new_target_key = get_common_key_in_dict(new_route, allowed_targets)
        if new_target_key is None or destination_cidr_key is None:
            result["result"] = False
            result["comment"] += [
                "There should be at least one valid destination cidr block and one target"
            ]
            return result
        new_target_value = new_route.get(new_target_key)
        # Destination cidr is unique for a route. After retrieving destination cidr check in old routes
        # if the new route cidr block is not present in old routes we associate it to route table
        # if the destination cidr is already present in old routes we need to check if there is any changes in target
        # The allowed targets can be any one of Internet gateway, Virtual private gateway and many more.
        # If the target key is modified or value is modified we need to delete old route and create
        # a new route with updated values
        # example the target might be changed from an Internet gateway to Transit gateway the key changes
        # So we need to delete Internet gateway route and create Transit gateway route
        if destination_cidr_block not in old_routes_map:
            routes_to_add.append(
                {
                    destination_cidr_key: destination_cidr_block,
                    new_target_key: new_target_value,
                }
            )
        else:
            old_route = old_routes_map.get(destination_cidr_block)
            old_target_key = get_common_key_in_dict(
                old_route, ALLOWED_ROUTE_TARGET_GATEWAYS
            )
            old_target_value = old_route.get(old_target_key)
            if old_target_key != new_target_key or old_target_value != new_target_value:
                routes_to_replace.append(
                    {
                        destination_cidr_key: destination_cidr_block,
                        new_target_key: new_target_value,
                    }
                )
            del old_routes_map[destination_cidr_block]

    # delete the remaining routes which are still present in old routes and not in new routes
    for old_route in old_routes_map.values():
        destination_cidr_key = get_common_key_in_dict(
            old_route, ALLOWED_ROUTE_DESTINATION_CIDR_BLOCKS
        )
        destination_cidr_block = old_route.get(destination_cidr_key)
        if old_route.get("Origin") != "CreateRouteTable":
            if old_route.get("GatewayId"):
                if not old_route.get("GatewayId").startswith("vpce-"):
                    routes_to_delete.append(
                        {destination_cidr_key: destination_cidr_block}
                    )
            else:
                routes_to_delete.append({destination_cidr_key: destination_cidr_block})

    result["routes_to_add"] = routes_to_add
    result["routes_to_delete"] = routes_to_delete
    result["routes_to_replace"] = routes_to_replace
    return result


def get_common_key_in_dict(dict1: Dict, target_keys_list: Set):
    common_keys = set(dict1.keys()).intersection(target_keys_list)
    return common_keys.pop() if common_keys else None


def get_route_table_association_by_id(
    hub,
    resources: List,
    gateway_id: str = None,
    subnet_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    result = {"result": False, "resource_id": resource_id, "ret": None}
    if resource_id:
        key = "RouteTableAssociationId"
        value = resource_id
    elif subnet_id:
        key = "SubnetId"
        value = subnet_id
    else:
        key = "GatewayId"
        value = gateway_id
    if resources:
        for resource in resources:
            if key in resource and resource.get(key) == value:
                # Do not return ones that are in disassociated or disassociating state
                if resource["AssociationState"]["State"] == "associated":
                    result["ret"] = resource
                    result["result"] = True
                    break
    return result


async def update_routes(
    hub,
    ctx,
    route_table_id: str,
    old_routes: List = None,
    new_routes: List = None,
):
    """Update routes of a route table.

    This function compares the existing(old) routes of route table with new routes. Routes that are in the new route
    table but not in the old route table will be associated to route table. routes that are in the old route table  but
    not in the new route table will be disassociated from transit route table.

    Args:
        route_table_id(str):
            The AWS resource id of the existing route table

        old_routes(list):
            Routes of existing route table

        new_routes(list):
            New routes to update

    Returns:
        ``{"result": True|False, "comment": "A message", "ret": None}``

    """
    result = dict(comment=[], result=True, ret=None)

    # compare old_routes if routes are modified
    if new_routes is []:
        result["result"] = False
        result["comment"].append(
            "Route Table routes cannot be None. There should be at least one route in Route Table"
        )
        return result
    elif new_routes is not None:
        routes_to_modify = (
            hub.tool.aws.ec2.route_table.get_route_table_routes_modifications(
                old_routes, new_routes
            )
        )
        if not routes_to_modify["result"]:
            result["comment"] = routes_to_modify["comment"]
            result["result"] = False
            return result
        routes_to_add = routes_to_modify["routes_to_add"]
        routes_to_delete = routes_to_modify["routes_to_delete"]
        routes_to_replace = routes_to_modify["routes_to_replace"]

        if not ctx.get("test", False):
            if routes_to_delete:
                for route_to_delete in routes_to_delete:
                    ret = await hub.exec.boto3.client.ec2.delete_route(
                        ctx, RouteTableId=route_table_id, **route_to_delete
                    )
                    if not ret.get("result"):
                        result["comment"] += list(ret["comment"])
                        result["result"] = False
                        return result
                result["comment"].append(f"Deleted Routes: {routes_to_delete}")
            if routes_to_replace:
                for route_to_replace in routes_to_replace:
                    ret = await hub.exec.boto3.client.ec2.replace_route(
                        ctx, RouteTableId=route_table_id, **route_to_replace
                    )
                    if not ret.get("result"):
                        result["comment"] += list(ret["comment"])
                        result["result"] = False
                        return result
                result["comment"].append(f"Replace Routes: {routes_to_replace}")
            if routes_to_add:
                for route_to_add in routes_to_add:
                    ret = await hub.exec.boto3.client.ec2.create_route(
                        ctx, RouteTableId=route_table_id, **route_to_add
                    )
                    if not ret.get("result"):
                        result["comment"] += list(ret["comment"])
                        result["result"] = False
                        return result
                result["comment"].append(f"Added Routes: {routes_to_add}")
        if routes_to_add or routes_to_replace or routes_to_delete:
            result["comment"].append(f"Updated route table {route_table_id}")
    result["ret"] = {"routes": new_routes}
    return result
