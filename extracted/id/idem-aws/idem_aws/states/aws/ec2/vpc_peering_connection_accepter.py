"""State module for managing EC2 VPC Peering Connection Accepter."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str,
    connection_status: str = None,
    tags: Dict[str, str] = None,
) -> Dict[str, Any]:
    """Requests to modify the VPC peering connection accepter.

    If you are creating a VPC peering connection in the same AWS account, you must both create and accept the request yourself.
    A VPC peering connection that's in the pending-acceptance state must be accepted by the owner of the accepter VPC to be activated.
    Updating the status only makes sense when the vpc peering connection is in pending-acceptance mode.
    When updating the status is attempted to be made through the VPC peering connection resource,
    it can only take place when the two VPCs are in the same region and have the same owner.
    If that is not true, the acceptance is controlled by this particular resource - VPC peering connection accepter.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str):
            An identifier of the resource in the provider. It is an identifier of the
            vpc peering connection of which the options are part of.

        connection_status(str, Optional):
            The desired status for the VPC peering connection, but in practice,
            an update will be attempted only if this status is set to "active".

        tags(Dict, Optional):
            Dict in the format of {tag-key: tag-value} The tags to assign to the peering connection.
            Each tag consists of a key name and an associated value. Defaults to None.

    Request Syntax:
        .. code-block:: sls

            [vpc-peering-connection-id]:
              aws.ec2.vpc_peering_connection_accepter.present:
                - resource_id: "string"
                - connection_status: "string"
                - tags: "Dict"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            pcx-ae89ce9b:
              aws.ec2.vpc_peering_connection_accepter.present:
                - resource_id: pcx-ae89ce9b
                - connection_status: "active"
                - tags:
                    first_key: first_value
                    second_key: second_value
                    third_key: third_value
                    fourth_key: fourth_value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    if not resource_id:
        result["result"] = False
        result[
            "comment"
        ] = hub.tool.aws.comment_utils.invalid_parameter_provided_comment(
            "resource_id", "aws.ec2.vpc_peering_connection_accepter", name
        )
        return result
    else:
        before = await hub.exec.aws.ec2.vpc_peering_connection_accepter.get(
            ctx, name=name, resource_id=resource_id
        )

        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = before["ret"]
        plan_state = copy.deepcopy(result["old_state"])

        # Update status - activate the connection
        # The only update possible is status activation - accepting the connection.
        # All the other statuses a connection could have are changed on their own,
        # for example: failed, expired, rejected...
        # The deleted status could be set by calling the absent function on this resource.
        if (
            connection_status == "active"
            and connection_status != result["old_state"]["connection_status"]
        ):
            accept_ret = await hub.tool.aws.ec2.vpc_peering_connection_utils.activate_vpc_peering_connection(
                ctx,
                "aws.ec2.vpc_peering_connection_accepter",
                name,
                resource_id,
                before["ret"]["connection_status"],
                connection_status,
            )

            result["result"] = accept_ret["result"]
            result["comment"] += accept_ret["comment"]
            if not accept_ret["result"]:
                return result

            resource_updated = resource_updated or bool(accept_ret["ret"])

        if resource_updated and ctx.get("test", False):
            plan_state["connection_status"] = accept_ret["ret"]["connection_status"]

        if resource_updated:
            if ctx.get("test", False):
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    "aws.ec2.vpc_peering_connection_accepter", name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    "aws.ec2.vpc_peering_connection_accepter", name
                )
        else:
            result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
                "aws.ec2.vpc_peering_connection_accepter", name
            )

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

        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not result["old_state"]) or resource_updated:
            after = await hub.exec.aws.ec2.vpc_peering_connection_accepter.get(
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
    """A No-Op function for vpc_peering_connection_accepter.

    This is a configuration resource of the vpc_peering_connection resource.
    It's not possible to delete vpc_peering_connection_accepter,
    You need to delete the vpc_peering_connection resource by calling vpc_peering_connection.absent,
    while providing the vpc_peering_connection id.
    If you want to modify the vpc_peering_connection_accepter resource,
    use the vpc_peering_connection_options.present.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The id of the vpc peering connection.

    Request Syntax:
        .. code-block:: sls

            [vpc-peering-connection-id]:
              aws.ec2.vpc_peering_connection_accepter.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            pcx-ae89ce9b:
              aws.ec2.vpc_peering_connection_accepter.absent:
                - name: pcx-ae89ce9b
                - resource_id: pcx-ae89ce9b

    """
    result = dict(
        comment=(
            "No-Op: The VPC peering connection accepter can not be deleted as it is not an AWS resource",
        ),
        old_state=None,
        new_state=None,
        name=name,
        result=True,
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Describes one or more of your VPC peering connection accepters.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.vpc_peering_connection_accepter.py
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
        vpc_peering_connection_accepter_translated = hub.tool.aws.ec2.conversion_utils.convert_raw_vpc_peering_connection_accepter_to_present(
            raw_resource=vpc_peering_connection, idem_resource_name=resource_id
        )

        result[vpc_peering_connection_accepter_translated["resource_id"]] = {
            "aws.ec2.vpc_peering_connection_accepter.present": [
                vpc_peering_connection_accepter_translated
            ]
        }

    return result
