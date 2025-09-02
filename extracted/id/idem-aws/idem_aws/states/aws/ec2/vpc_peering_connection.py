"""State module for managing EC2 VPC Peering Connection."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    peer_owner_id: str = None,
    peer_vpc_id: str = None,
    vpc_id: str = None,
    peer_region: str = None,
    tags: Dict[str, str] = None,
    status: str = None,
) -> Dict[str, Any]:
    """Requests to create or update a VPC peering connection.

    Requests a VPC peering connection between two VPCs: a requester VPC that you own and an accepter VPC with which
    to create the connection. The accepter VPC can belong to another Amazon Web Services account and can be in a
    different Region to the requester VPC. The requester VPC and accepter VPC cannot have overlapping CIDR blocks.
    Limitations and rules apply to a VPC peering connection. For more information, see the limitations section in
    the VPC Peering Guide.  The owner of the accepter VPC must accept the peering request to activate the peering
    connection. The VPC peering connection request expires after 7 days, after which it cannot be accepted or
    rejected. If you create a VPC peering connection request between VPCs with overlapping CIDR blocks, the VPC
    peering connection has a status of failed.

    NOTE: These parameters - peer_owner_id, peer_vpc_id, vpc_id, peer_region
    can't be updated for a given VPC peering connection.
    Only tags and status can be updated for a VPC peering connection
    In case of an update attempt of the previously mentioned four parameters,
    where resource_id is passed for an existing connection, they will be ignored.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        peer_owner_id(str, Optional):
            The Amazon Web Services account ID of the owner of the accepter VPC.
            Default: Your Amazon Web Services account ID. Defaults to None.

        peer_vpc_id(str, Optional):
            The ID of the VPC with which you are creating the VPC peering connection.
            You must specify this parameter in the request. Defaults to None.

        vpc_id(str, Optional):
            The ID of the requester VPC. You must specify this parameter in the request.
            Defaults to None.

        peer_region(str, Optional):
            The Region code for the accepter VPC, if the accepter VPC is located in a Region
            other than the Region in which you make the request.
            Default: The Region in which you make the request. Defaults to None.

        tags(Dict, Optional):
            Dict in the format of {tag-key: tag-value} The tags to assign to the peering connection.
            Each tag consists of a key name and an associated value. Defaults to None.

        status: (str, Optional)
            The desired status for the VPC peering connection, but in practice,
            an update will be attempted only if this status is set to "active".

    Request Syntax:
       .. code-block:: sls

            [vpc-peering-connection-id]:
              aws.ec2.vpc_peering_connection.present:
              - resource_id: "string"
              - name: "string"
              - peer_owner_id: "string"
              - peer_region: "string"
              - peer_vpc_id: "string"
              - vpc_id: "string"
              - tags: "Dict"
              - status: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.ec2.vpc_peering_connection.present:
                - resource_id: pcx-ae89ce9b
                - name: pcx-ae89ce9b
                - peer_owner_id: '000000000000'
                - peer_region: us-west-2
                - peer_vpc_id: vpc-98c058ae
                - vpc_id: vpc-2c90d746
                - status: active
                - tags:
                    first_key: first_value
                    second_key: second_value
                    third_key: third_value
                    fourth_key: fourth_value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.ec2.vpc_peering_connection.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = before["ret"]
        plan_state = copy.deepcopy(result["old_state"])

        # Update tags
        if tags is not None and tags != result["old_state"].get("tags"):
            update_ret = await hub.tool.aws.ec2.tag.update_tags(
                ctx=ctx,
                resource_id=resource_id,
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )

            result["result"] = update_ret["result"]
            result["comment"] += update_ret["comment"]
            if not update_ret["result"]:
                return result

            resource_updated = resource_updated or bool(update_ret["ret"])
            if update_ret["ret"] is not None and ctx.get("test", False):
                plan_state["tags"] = update_ret["ret"]

        # Update status - activate the connection
        # The only update possible is status activation - accepting the connection.
        # All the other statuses a connection could have are changed on their own,
        # for example: failed, expired, rejected...
        # The deleted status could be set by calling the absent function on this resource.
        if status == "active" and status != result["old_state"].get("status"):
            accept_ret = await hub.tool.aws.ec2.vpc_peering_connection_utils.activate_vpc_peering_connection(
                ctx,
                "aws.ec2.vpc_peering_connection",
                name,
                resource_id,
                result["old_state"].get("status"),
                status,
            )

            result["result"] = accept_ret["result"]
            result["comment"] += accept_ret["comment"]
            if not accept_ret["result"]:
                return result

            resource_updated = resource_updated or bool(accept_ret["ret"])
            if accept_ret["ret"] is not None and ctx.get("test", False):
                plan_state["status"] = accept_ret["ret"]["connection_status"]

        if resource_updated:
            if ctx.get("test", False):
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    "aws.ec2.vpc_peering_connection", name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    "aws.ec2.vpc_peering_connection", name
                )
        else:
            result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
                "aws.ec2.vpc_peering_connection", name
            )
    else:
        if ctx.get("test", False):
            desired_status = status or "pending-acceptance"
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "peer_owner_id": peer_owner_id,
                    "peer_vpc_id": peer_vpc_id,
                    "vpc_id": vpc_id,
                    "peer_region": peer_region,
                    "tags": tags,
                    "status": desired_status,
                },
            )

            result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                "aws.ec2.vpc_peering_connection", name
            )

            if status == "active":
                result[
                    "comment"
                ] += hub.tool.aws.comment_utils.would_update_status_comment(
                    "aws.ec2.vpc_peering_connection", name, resource_id, status
                )

            return result

        tag_specifications = [
            {
                "ResourceType": "vpc-peering-connection",
                "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
            }
        ]

        create_ret = await hub.exec.boto3.client.ec2.create_vpc_peering_connection(
            ctx,
            **{
                "PeerOwnerId": peer_owner_id,
                "PeerVpcId": peer_vpc_id,
                "VpcId": vpc_id,
                "PeerRegion": peer_region,
                "TagSpecifications": tag_specifications,
            },
        )

        result["result"] = create_ret["result"]
        if not result["result"]:
            result["comment"] += create_ret["comment"]
            return result

        result["comment"] += hub.tool.aws.comment_utils.create_comment(
            "aws.ec2.vpc_peering_connection", name
        )

        new_vpc_peering_connection = create_ret["ret"]["VpcPeeringConnection"]
        resource_id = new_vpc_peering_connection["VpcPeeringConnectionId"]

        # The only status change possible is status activation - accepting the connection.
        # All the other statuses a connection could have are changed on their own,
        # for example: failed, expired, rejected...
        # The deleted status could be set by calling the absent function on this resource.
        if status == "active":
            accept_ret = await hub.tool.aws.ec2.vpc_peering_connection_utils.activate_vpc_peering_connection(
                ctx,
                "aws.ec2.vpc_peering_connection",
                name,
                resource_id,
                new_vpc_peering_connection["Status"]["Code"],
                status,
            )

            result["comment"] += accept_ret["comment"]
            result["result"] = accept_ret["result"]
            if not accept_ret["result"]:
                return result

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not result["old_state"]) or resource_updated:
        after = await hub.exec.aws.ec2.vpc_peering_connection.get(
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
    """Deletes a VPC peering connection.

    Either the owner of the requester VPC or the owner of the accepter VPC can
    delete the VPC peering connection if it's in the active state. The owner of the requester VPC can delete a VPC
    peering connection in the pending-acceptance state. You cannot delete a VPC peering connection that's in the
    failed state.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

    Request Syntax:
       .. code-block:: sls

            [vpc-peering-connection-id]:
              aws.ec2.vpc_peering_connection.absent:
              - resource_id: "string"
              - name: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.ec2.vpc_peering_connection.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            "aws.ec2.vpc_peering_connection", name
        )
        return result

    before = await hub.exec.aws.ec2.vpc_peering_connection.get(
        ctx=ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result
    if not before["ret"] or before["ret"]["status"] == "deleted":
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            "aws.ec2.vpc_peering_connection", name
        )
    else:
        result["old_state"] = before["ret"]

        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                "aws.ec2.vpc_peering_connection", name
            )
        else:
            # Deleting the vpc peering connection
            ret = await hub.exec.boto3.client.ec2.delete_vpc_peering_connection(
                ctx, **{"VpcPeeringConnectionId": resource_id}
            )

            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result

            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                "aws.ec2.vpc_peering_connection", name
            )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Describes one or more of your VPC peering connections.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.vpc_peering_connection
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
        vpc_peering_connection_translated = hub.tool.aws.ec2.conversion_utils.convert_raw_vpc_peering_connection_to_present(
            raw_resource=vpc_peering_connection, idem_resource_name=resource_id
        )

        result[vpc_peering_connection_translated["resource_id"]] = {
            "aws.ec2.vpc_peering_connection.present": [
                vpc_peering_connection_translated
            ]
        }

    return result
