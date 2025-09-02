"""State module for managing EC2 VPC Peering Connection Options."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str,
    peer_allow_remote_vpc_dns_resolution: bool = None,
    peer_allow_classic_link_to_remote_vpc: bool = None,
    peer_allow_vpc_to_remote_classic_link: bool = None,
    allow_remote_vpc_dns_resolution: bool = None,
    allow_classic_link_to_remote_vpc: bool = None,
    allow_vpc_to_remote_classic_link: bool = None,
) -> Dict[str, Any]:
    """Requests to modify the VPC peering connection options.

    If the peered VPCs are in the same AWS account, you can enable DNS resolution for queries from the local VPC.
    This ensures that queries from the local VPC resolve to private IP addresses in the peer VPC.
    This option is not available if the peered VPCs are in different AWS accounts or different Regions.
    For peered VPCs in different AWS accounts,
    each AWS account owner must initiate a separate request to modify the peering connection options.
    For inter-region peering connections,
    you must use the Region for the requester VPC to modify the requester VPC peering options
    and the Region for the accepter VPC to modify the accepter VPC peering options.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str):
            An identifier of the resource in the provider. It is an identifier of the
            vpc peering connection of which the options are part of.

        peer_allow_remote_vpc_dns_resolution(bool, Optional):
            VPC peering connection option for the accepter:
            Requester Indicates whether a local VPC can resolve public DNS hostnames to private IP addresses
            when queried from instances in a peer VPC.

        peer_allow_classic_link_to_remote_vpc(bool, Optional):
            VPC peering connection option for the accepter:
            Indicates whether a local ClassicLink connection can communicate with the peer VPC
            over the VPC peering connection.

        peer_allow_vpc_to_remote_classic_link(bool, Optional):
            VPC peering connection option for the accepter:
            Indicates whether a local VPC can communicate with a ClassicLink connection in the peer VPC
            over the VPC peering connection.

        allow_remote_vpc_dns_resolution(bool, Optional):
            VPC peering connection option for the requester:
            Requester Indicates whether a local VPC can resolve public DNS hostnames to private IP addresses
            when queried from instances in a peer VPC.

        allow_classic_link_to_remote_vpc(bool, Optional):
            VPC peering connection option for the requester:
            Indicates whether a local ClassicLink connection can communicate with the peer VPC
            over the VPC peering connection.

        allow_vpc_to_remote_classic_link(bool, Optional):
            VPC peering connection option for the requester:
            Indicates whether a local VPC can communicate with a ClassicLink connection in the peer VPC
            over the VPC peering connection.

    Request Syntax:
        .. code-block:: sls

            [vpc-peering-connection-id]:
              aws.ec2.vpc_peering_connection_options.present:
                - resource_id: "string"
                - peer_allow_remote_vpc_dns_resolution: True|False
                - peer_allow_classic_link_to_remote_vpc: True|False
                - peer_allow_vpc_to_remote_classic_link: True|False
                - allow_remote_vpc_dns_resolution: True|False
                - allow_classic_link_to_remote_vpc: True|False
                - allow_vpc_to_remote_classic_link: True|False

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            pcx-ae89ce9b:
                aws.ec2.vpc_peering_connection_options.present:
                    - resource_id: pcx-ae89ce9b
                    - peer_allow_classic_link_to_remote_vpc: true
                    - allow_vpc_to_remote_classic_link: true
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    if not resource_id:
        result["result"] = False
        result[
            "comment"
        ] = hub.tool.aws.comment_utils.invalid_parameter_provided_comment(
            "resource_id", "aws.ec2.vpc_peering_connection_options", name
        )
        return result
    else:
        before = await hub.exec.aws.ec2.vpc_peering_connection_options.get(
            ctx, name=name, resource_id=resource_id
        )

        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = before["ret"]
        plan_state = copy.deepcopy(result["old_state"])

        new_options = {
            "peer_allow_classic_link_to_remote_vpc": peer_allow_classic_link_to_remote_vpc,
            "peer_allow_remote_vpc_dns_resolution": peer_allow_remote_vpc_dns_resolution,
            "peer_allow_vpc_to_remote_classic_link": peer_allow_vpc_to_remote_classic_link,
            "allow_classic_link_to_remote_vpc": allow_classic_link_to_remote_vpc,
            "allow_remote_vpc_dns_resolution": allow_remote_vpc_dns_resolution,
            "allow_vpc_to_remote_classic_link": allow_vpc_to_remote_classic_link,
        }
        modify_options_ret = await hub.tool.aws.ec2.vpc_peering_connection_utils.update_vpc_peering_connection_options(
            ctx,
            name,
            resource_id,
            before,
            new_options,
        )

        result["result"] = modify_options_ret["result"]
        result["comment"] += modify_options_ret["comment"]
        if not modify_options_ret["result"]:
            return result

        options_updated = bool(modify_options_ret["ret"])
        resource_updated = resource_updated or options_updated
        if options_updated and ctx.get("test", False):
            for key, value in modify_options_ret["ret"].items():
                plan_state[key] = value

        if resource_updated:
            if ctx.get("test", False):
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    "aws.ec2.vpc_peering_connection_options", name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    "aws.ec2.vpc_peering_connection_options", name
                )
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                "aws.ec2.vpc_peering_connection_options", name
            )

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not result["old_state"]) or resource_updated:
        after = await hub.exec.aws.ec2.vpc_peering_connection_options.get(
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


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """A No-Op function for vpc_peering_connection_options.

    This is a configuration resource of the vpc_peering_connection resource.
    It's not possible to delete vpc_peering_connection_options,
    You need to delete the vpc_peering_connection resource by calling vpc_peering_connection.absent,
    while providing the vpc_peering_connection id.
    If you want to modify the vpc_peering_connection_options resource,
    use the vpc_peering_connection_options.present.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The id of the vpc peering connection.

    Request Syntax:
        .. code-block:: sls

            [vpc-peering-connection-id]:
              aws.ec2.vpc_peering_connection_options.absent:
                - name: "string"

    Returns:
        Dict[str, Any]
    """
    result = dict(
        comment=(
            "No-Op: The VPC peering connection options can not be deleted as it is not an AWS resource",
        ),
        old_state=None,
        new_state=None,
        name=name,
        result=True,
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Describes one or more of your VPC peering connection options.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.vpc_peering_connection_options.py
    """
    result = {}
    ret = await hub.exec.boto3.client.ec2.describe_vpc_peering_connections(ctx)

    if not ret["result"]:
        hub.log.warning(
            f"Could not describe aws.ec2.vpc_peering_connection {ret['comment']}"
        )
        return {}

    for vpc_peering_connection in ret["ret"]["VpcPeeringConnections"]:
        resource_id = vpc_peering_connection.get("VpcPeeringConnectionId")
        vpc_peering_connection_options_translated = hub.tool.aws.ec2.conversion_utils.convert_raw_vpc_peering_connection_options_to_present(
            raw_resource=vpc_peering_connection, idem_resource_name=resource_id
        )

        result[vpc_peering_connection_options_translated["resource_id"]] = {
            "aws.ec2.vpc_peering_connection_options.present": [
                vpc_peering_connection_options_translated
            ]
        }

    return result
