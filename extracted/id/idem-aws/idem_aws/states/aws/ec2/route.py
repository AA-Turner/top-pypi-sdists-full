import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    route_table_id: str,
    resource_id: str = None,
    destination_cidr_block: str = None,
    destination_ipv6_cidr_block: str = None,
    destination_prefix_list_id: str = None,
    vpc_endpoint_id: str = None,
    egress_only_internet_gateway_id: str = None,
    gateway_id: str = None,
    instance_id: str = None,
    nat_gateway_id: str = None,
    transit_gateway_id: str = None,
    local_gateway_id: str = None,
    carrier_gateway_id: str = None,
    network_interface_id: str = None,
    vpc_peering_connection_id: str = None,
    core_network_arn: str = None,
) -> Dict[str, Any]:
    """Creates a route in a route table within a VPC. You must specify one of the following targets: internet gateway
    or virtual private gateway, NAT instance, NAT gateway, VPC peering connection, network interface, egress-only
    internet gateway, or transit gateway. When determining how to route traffic, we use the route with the most
    specific match. For example, traffic is destined for the IPv4 address 192.0.2.3, and the route table includes
    the following two IPv4 routes:    192.0.2.0/24 (goes to some target A)    192.0.2.0/28 (goes to some target B)
    Both routes apply to the traffic destined for 192.0.2.3. However, the second route in the list covers a smaller
    number of IP addresses and is therefore more specific, so we use that route to determine where to target the
    traffic. For more information about route tables, see Route tables in the Amazon Virtual Private Cloud User
    Guide.

    Args:
        name(str): An Idem name of the resource.
        route_table_id(str): The ID of the route table for the route.
        resource_id(str, Optional): Unique identifier to identify the route in a route table. format of resource id is
            <route_table_id>/<destination_cidr_block or destination_ipv6_cidr_block or destination_prefix_list_id>
        destination_cidr_block(str, Optional): The IPv4 CIDR address block used for the destination match. Routing decisions are based on the
            most specific match. We modify the specified CIDR block to its canonical form; for example, if
            you specify 100.68.0.18/18, we modify it to 100.68.0.0/18. Defaults to None.
        destination_ipv6_cidr_block(str, Optional): The IPv6 CIDR block used for the destination match. Routing decisions are based on the most
            specific match. Defaults to None.
        destination_prefix_list_id(str, Optional): The ID of a prefix list used for the destination match. Defaults to None.
        vpc_endpoint_id(str, Optional): The ID of a VPC endpoint. Supported for Gateway Load Balancer endpoints only. Defaults to None.
        egress_only_internet_gateway_id(str, Optional): [IPv6 traffic only] The ID of an egress-only internet gateway. Defaults to None.
        gateway_id(str, Optional): The ID of an internet gateway or virtual private gateway attached to your VPC. Defaults to None.
        instance_id(str, Optional): The ID of a NAT instance in your VPC. The operation fails if you specify an instance ID unless
            exactly one network interface is attached. Defaults to None.
        nat_gateway_id(str, Optional): [IPv4 traffic only] The ID of a NAT gateway. Defaults to None.
        transit_gateway_id(str, Optional): The ID of a transit gateway. Defaults to None.
        local_gateway_id(str, Optional): The ID of the local gateway. Defaults to None.
        carrier_gateway_id(str, Optional): The ID of the carrier gateway. You can only use this option when the VPC contains a subnet which
            is associated with a Wavelength Zone. Defaults to None.
        network_interface_id(str, Optional): The ID of a network interface. Defaults to None.
        vpc_peering_connection_id(str, Optional): The ID of a VPC peering connection. Defaults to None.
        core_network_arn(str, Optional): The Amazon Resource Name (ARN) of the core network. Defaults to None.

    Request Syntax:
       .. code-block:: sls

          [route-table-id-destination]:
            aws.ec2.route.present:
              - name: "string"
              - route_table_id: "string"
              - destination_cidr_block: "string"
              - gateway_id: "string"
              - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            r-rtb-343452242424:
              aws.ec2.route.present:
                - name: r-rtb-343452242424
                - route_table_id: rtb-3434522
                - resource_id: r-rtb-343452242424
                - destination_cidr_block: 172.12.12.201
                - gateway_id: subnet-4923930130
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.ec2.route.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.ec2.route", name=resource_id
        )
        update_allowed_params = {
            "carrier_gateway_id": "CarrierGatewayId",
            "egress_only_internet_gateway_id": "EgressOnlyInternetGatewayId",
            "gateway_id": "GatewayId",
            "instance_id": "InstanceId",
            "local_gateway_id": "LocalGatewayId",
            "nat_gateway_id": "NatGatewayId",
            "network_interface_id": "NetworkInterfaceId",
            "transit_gateway_id": "TransitGatewayId",
            "vpc_endpoint_id": "VpcEndpointId",
            "vpc_peering_connection_id": "VpcPeeringConnectionId",
        }
        update_payload = {}
        for new_param, old_param in update_allowed_params.items():
            if (
                locals()[new_param] is not None
                and result["old_state"].get(new_param) != locals()[new_param]
            ):
                update_payload[old_param] = locals()[new_param]
                if destination_cidr_block:
                    update_payload["DestinationCidrBlock"] = destination_cidr_block
                elif destination_ipv6_cidr_block:
                    update_payload[
                        "DestinationIpv6CidrBlock"
                    ] = destination_ipv6_cidr_block
                elif destination_prefix_list_id:
                    update_payload[
                        "DestinationPrefixListId"
                    ] = destination_prefix_list_id

        if update_payload:
            if ctx.get("test", False):
                result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.ec2.route", name=name
                )
                for new_param, old_param in update_allowed_params.items():
                    plan_state[new_param] = locals()[new_param]
            else:
                update_ret = await hub.exec.boto3.client.ec2.replace_route(
                    ctx, RouteTableId=route_table_id, **update_payload
                )
                if not update_ret.get("result"):
                    result["comment"] = update_ret["comment"]
                    result["result"] = False
                    return result
                resource_updated = update_ret["result"]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "route_table_id": route_table_id,
                    "destination_cidr_block": destination_cidr_block,
                    "destination_ipv6_cidr_block": destination_ipv6_cidr_block,
                    "destination_prefix_list_id": destination_prefix_list_id,
                    "vpc_endpoint_id": vpc_endpoint_id,
                    "egress_only_internet_gateway_id": egress_only_internet_gateway_id,
                    "gateway_id": gateway_id,
                    "instance_id": instance_id,
                    "nat_gateway_id": nat_gateway_id,
                    "transit_gateway_id": transit_gateway_id,
                    "local_gateway_id": local_gateway_id,
                    "carrier_gateway_id": carrier_gateway_id,
                    "network_interface_id": network_interface_id,
                    "vpc_peering_connection_id": vpc_peering_connection_id,
                    "core_network_arn": core_network_arn,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ec2.route", name=name
            )
            return result
        ret = await hub.exec.boto3.client.ec2.create_route(
            ctx,
            DestinationCidrBlock=destination_cidr_block,
            DestinationIpv6CidrBlock=destination_ipv6_cidr_block,
            DestinationPrefixListId=destination_prefix_list_id,
            VpcEndpointId=vpc_endpoint_id,
            EgressOnlyInternetGatewayId=egress_only_internet_gateway_id,
            GatewayId=gateway_id,
            InstanceId=instance_id,
            NatGatewayId=nat_gateway_id,
            TransitGatewayId=transit_gateway_id,
            LocalGatewayId=local_gateway_id,
            CarrierGatewayId=carrier_gateway_id,
            NetworkInterfaceId=network_interface_id,
            RouteTableId=route_table_id,
            VpcPeeringConnectionId=vpc_peering_connection_id,
            CoreNetworkArn=core_network_arn,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.ec2.route", name=name
        )
        resource_id = f"{route_table_id}/{(destination_cidr_block or destination_ipv6_cidr_block or destination_prefix_list_id)}"
    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not result["old_state"]) or resource_updated:
        after = await hub.exec.aws.ec2.route.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not after["result"]:
            result["result"] = False
            result["comment"] += after["comment"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes the specified route from the specified route table.

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): Unique identifier to identify the route in a route table. format of resource id is
            <route_table_id>/<destination_cidr_block or destination_ipv6_cidr_block or destination_prefix_list_id>.
            Idem automatically considers this resource being absent if this field is not specified.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              aws.ec2.route.absent:
                - name: value
                - resource_id: value
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.route", name=name
        )
        return result

    before = await hub.exec.aws.ec2.route.get(
        ctx=ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.route", name=name
        )
    else:
        result["old_state"] = before["ret"]
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.ec2.route", name=name
            )
            return result
        else:
            ret = await hub.exec.boto3.client.ec2.delete_route(
                ctx,
                RouteTableId=result["old_state"]["route_table_id"],
                DestinationCidrBlock=result["old_state"].get("destination_cidr_block"),
                DestinationIpv6CidrBlock=result["old_state"].get(
                    "destination_ipv6_cidr_block"
                ),
                DestinationPrefixListId=result["old_state"].get(
                    "destination_prefix_list_id"
                ),
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                return result
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.ec2.route", name=name
            )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe aws.ec2.route
    """
    result = {}
    ret = await hub.exec.boto3.client.ec2.describe_route_tables(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe route tables {ret['comment']}")
        return result
    for route_table in ret["ret"]["RouteTables"]:
        route_table_id = route_table.get("RouteTableId")
        for route in route_table.get("Routes"):
            resource_key = f"{route_table_id}/{(route.get('DestinationCidrBlock') or route.get('DestinationIpv6CidrBlock') or route.get('DestinationPrefixListId'))}"
            resource_converted = (
                hub.tool.aws.ec2.conversion_utils.convert_raw_route_to_present(
                    raw_resource=route,
                    route_table_id=route_table_id,
                    idem_resource_name=resource_key,
                )
            )
            result[resource_key] = {
                "aws.ec2.route.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_converted.items()
                ]
            }
    return result
