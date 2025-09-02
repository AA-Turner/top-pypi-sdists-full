"""
State module for managing EC2 Route Table.

hub.exec.boto3.client.ec2.associate_route_table
hub.exec.boto3.client.ec2.create_route_table
hub.exec.boto3.client.ec2.delete_route_table
hub.exec.boto3.client.ec2.describe_route_tables
hub.exec.boto3.client.ec2.disassociate_route_table
resource = await hub.tool.boto3.resource.create(ctx, "ec2", "RouteTable", name)
hub.tool.boto3.resource.exec(resource, associate_with_subnet, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, create_route, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, create_tags, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, delete, *args, **kwargs)
"""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    vpc_id: str,
    resource_id: str = None,
    routes: List[
        make_dataclass(
            "Route",
            [
                ("DestinationCidrBlock", str, field(default=None)),
                ("DestinationIpv6CidrBlock", str, field(default=None)),
                ("DestinationPrefixListId", str, field(default=None)),
                ("EgressOnlyInternetGatewayId", str, field(default=None)),
                ("GatewayId", str, field(default=None)),
                ("InstanceId", str, field(default=None)),
                ("InstanceOwnerId", str, field(default=None)),
                ("NatGatewayId", str, field(default=None)),
                ("TransitGatewayId", str, field(default=None)),
                ("LocalGatewayId", str, field(default=None)),
                ("CarrierGatewayId", str, field(default=None)),
                ("NetworkInterfaceId", str, field(default=None)),
                ("VpcPeeringConnectionId", str, field(default=None)),
                ("CoreNetworkArn", str, field(default=None)),
            ],
        )
    ] = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
) -> Dict[str, Any]:
    """Creates a route table for the specified VPC.

    For more information, see Route tables in the Amazon Virtual Private Cloud User Guide.

    Args:
        name(str):
            An Idem name to identify the route table resource.

        resource_id(str, Optional):
            AWS Route Table ID.

        vpc_id(str):
            AWS VPC ID.

        routes(list[dict[str, Any]], Optional):
            The network interfaces to associate with the instance. If you specify a network interface, you
            must specify any security groups and subnets as part of the network interface. Defaults to None.

            * DestinationCidrBlock (str, Optional):
                The IPv4 CIDR address block used for the destination match. Routing decisions are based on the
                most specific match. We modify the specified CIDR block to its canonical form; for example, if
                you specify 100.68.0.18/18, we modify it to 100.68.0.0/18. Defaults to None.

            * DestinationIpv6CidrBlock (str, Optional):
                The IPv6 CIDR block used for the destination match.
                Routing decisions are based on the most specific match. Defaults to None.

            * EgressOnlyInternetGatewayId (str, Optional):
                [IPv6 traffic only] The ID of an egress-only internet gateway. Defaults to None.

            * GatewayId (str, Optional):
                The ID of an internet gateway or virtual private gateway attached to your VPC. Defaults to None.

            * InstanceId (str, Optional):
                The ID of a NAT instance in your VPC. The operation fails if you specify an instance ID unless
                exactly one network interface is attached. Defaults to None.

            * InstanceOwnerId (str, Optional): T
                he ID of Amazon Web Services account that owns the instance. Defaults to None.

            * NatGatewayId (str, Optional):
                [IPv4 traffic only] The ID of a NAT gateway. Defaults to None.

            * (TransitGatewayId, str, Optional):
                The ID of a transit gateway. Defaults to None.

            * LocalGatewayId (str, Optional):
                The ID of the local gateway. Defaults to None.

            * CarrierGatewayId (str, Optional):
                The ID of the carrier gateway. You can only use this option when the VPC contains a subnet which
                is associated with a Wavelength Zone. Defaults to None.

            * NetworkInterfaceId (str, Optional):
                The ID of a network interface. Defaults to None.

            * VpcPeeringConnectionId (str, Optional):
                The ID of a VPC peering connection. Defaults to None.

            * CoreNetworkArn (str, Optional):
                The Amazon Resource Name (ARN) of the core network. Defaults to None.

        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the route table.
            Each tag consists of a key name and an associated value. Defaults to None.

            * Key (str, Optional):
                The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.

            * Value (str, Optional):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.

    Request Syntax:
        .. code-block:: sls

           [route_table-resource-name]:
             aws.ec2.route_table.present:
               - vpc_id: 'string'
               - resource_id: 'string'
               - routes:
                 - DestinationCidrBlock: 'string'
                   GatewayId: 'string'
               - tags:
                 - Key: 'string'
                   Value: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

           test_route-table:
             aws.ec2.route_table.present:
               - vpc_id: vpc-02850adfa9f6fc916
               - resource_id: route_table-3485hydfe5f6tb998
               - routes:
                 - DestinationCidrBlock: 198.31.0.0/16
                   GatewayId: local
               - tags:
                 - Key: Name
                   Value: route-table-association-test
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    update_successful = False
    plan_state = {}
    before = None
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
    if resource_id:
        try:
            before = await hub.exec.aws.ec2.route_table.get(
                ctx=ctx, name=name, resource_id=resource_id
            )
            if not before["result"] or not before["ret"]:
                result["result"] = False
                result["comment"] = before["comment"]
                return result
            result["old_state"] = copy.deepcopy(before["ret"])
            plan_state = copy.deepcopy(result["old_state"])
            result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.ec2.route_table", name=resource_id
            )
            update_ret = await hub.tool.aws.ec2.route_table.update_routes(
                ctx=ctx,
                route_table_id=resource_id,
                old_routes=result["old_state"].get("routes"),
                new_routes=routes,
            )
            result["comment"] += update_ret["comment"]
            update_successful = update_ret["result"]
            if not update_ret["result"]:
                result["result"] = False
            if update_ret["ret"] and ctx.get("test", False):
                if update_ret["ret"].get("routes") is not None:
                    plan_state["routes"] = update_ret["ret"].get("routes")
            if (
                update_successful
                and tags is not None
                and tags != result["old_state"].get("tags")
            ):
                # Update tags
                update_ret = await hub.tool.aws.ec2.tag.update_tags(
                    ctx=ctx,
                    resource_id=resource_id,
                    old_tags=result["old_state"].get("tags"),
                    new_tags=tags,
                )
                update_successful = update_ret["result"]
                result["comment"] += update_ret["comment"]
                result["result"] = update_ret["result"]
                if ctx.get("test", False) and update_ret["result"]:
                    plan_state["tags"] = update_ret["ret"]

        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "vpc_id": vpc_id,
                    "resource_id": name,
                    "routes": routes,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ec2.route_table", name=name
            )
            return result
        try:
            ret = await hub.exec.boto3.client.ec2.create_route_table(
                ctx,
                TagSpecifications=[
                    {
                        "ResourceType": "route-table",
                        "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
                    }
                ]
                if tags
                else None,
                VpcId=vpc_id,
            )
            result["result"] = ret["ret"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            resource_id = ret["ret"]["RouteTable"]["RouteTableId"]
            result["comment"] += [f"Created '{name}'"]
            # Associate routes if provided
            update_ret = await hub.tool.aws.ec2.route_table.update_routes(
                ctx=ctx,
                route_table_id=resource_id,
                old_routes=[],
                new_routes=routes,
            )
            result["comment"] += update_ret["comment"]
            result["result"] = result["result"] and update_ret["result"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif update_successful or not (before and before["result"]):
            after = await hub.exec.aws.ec2.route_table.get(
                ctx=ctx, name=name, resource_id=resource_id
            )
            if not after["result"]:
                result["result"] = False
                result["comment"] = after["comment"]
                return result
            result["new_state"] = copy.deepcopy(after["ret"])
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes the specified route table.

    You must disassociate the route table from any subnets before you can delete it. You can't delete the main route table.

    Args:
        name(str):
            An Idem name to identify the route table resource.

        resource_id(str, Optional):
            AWS Route Table ID. Idem automatically considers this resource being absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            [route_table-resource-id]:
              aws.ec2.route_table.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              aws.ec2.route_table.absent:
                - name: value
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.route_table", name=name
        )
        return result
    before = await hub.exec.aws.ec2.route_table.get(
        ctx=ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.route_table", name=name
        )
    else:
        result["old_state"] = before["ret"]
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.ec2.route_table", name=name
            )
            return result
        else:
            ret = await hub.exec.boto3.client.ec2.delete_route_table(
                ctx, RouteTableId=resource_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                result["result"] = False
                return result
            result["comment"] += hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.ec2.route_table", name=name
            )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Describes one or more of your route tables. Each subnet in your VPC must be associated with a route table. If a
    subnet is not explicitly associated with any route table, it is implicitly associated with the main route table.
    This command does not return the subnet ID for implicit associations. For more information, see Route tables in
    the Amazon Virtual Private Cloud User Guide.


    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe aws.ec2.route_table
    """

    result = {}
    ret = await hub.exec.boto3.client.ec2.describe_route_tables(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe route_table {ret['comment']}")
        return result
    for route_table in ret["ret"]["RouteTables"]:
        route_table_id = route_table.get("RouteTableId")
        resource_converted = (
            hub.tool.aws.ec2.conversion_utils.convert_raw_route_table_to_present(
                raw_resource=route_table,
                idem_resource_name=route_table_id,
            )
        )
        result[route_table_id] = {
            "aws.ec2.route_table.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_converted.items()
            ]
        }
    return result
