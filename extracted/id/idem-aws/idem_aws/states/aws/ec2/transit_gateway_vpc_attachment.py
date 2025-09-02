"""
State module for managing EC2 Transit gateway VPC attachment
"""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]
__reconcile_wait__ = {"static": {"wait_in_seconds": 60}}
TREQ = {
    "present": {
        "require": ["aws.ec2.subnet.present", "aws.ec2.transit_gateway.present"],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    transit_gateway: str,
    vpc_id: str,
    subnet_ids: List[str],
    resource_id: str = None,
    options: make_dataclass(
        "CreateTransitGatewayVpcAttachmentRequestOptions",
        [
            ("DnsSupport", str, field(default=None)),
            ("Ipv6Support", str, field(default=None)),
            ("ApplianceModeSupport", str, field(default=None)),
        ],
    ) = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
) -> Dict[str, Any]:
    """Attaches the specified VPC to the specified transit gateway.

    If you attach a VPC with a CIDR range that overlaps the CIDR range of a VPC that is already attached, the new VPC
    CIDR range is not propagated to the default propagation route table. To send VPC traffic to an attached transit gateway,
    add a route to the VPC route table using CreateRoute.

    Args:
        name(str):
            Name of the resource.

        transit_gateway(str):
            The ID of the transit gateway.

        vpc_id(str):
            The ID of the VPC.

        subnet_ids(list):
            The IDs of one or more subnets. You can specify only one subnet per Availability Zone.
            You must specify at least one subnet, but we recommend that you specify two subnets for better availability.
            The transit gateway uses one IP address from each specified subnet.

        resource_id(str, Optional):
            AWS Transit gateway VPC attachment id.

        options(dict[str, Any], Optional):
            The VPC attachment options. Defaults to None.

            * DnsSupport (str, Optional):
                Enable or disable DNS support. The default is enable.

            * Ipv6Support (str, Optional):
                Enable or disable IPv6 support. The default is disable.

            * ApplianceModeSupport (str, Optional):
                Enable or disable support for appliance mode. If enabled, a traffic flow between a source and
                destination uses the same Availability Zone for the VPC attachment for the lifetime of that
                flow. The default is disable.

        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the transit gateway VPC attachment.
            Each tag consists of a key name and an associated value. Defaults to None.

            * Key (str, Optional):
                The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.

            * Value (str, Optional):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.

    Request Syntax:
        .. code-block:: sls

            [transit-gateway-resource-id]:
              aws.ec2.transit_gateway_vpc_attachment.present:
                - name: 'string'
                - resource_id: 'string'
                - transit_gateway: 'string'
                - vpc_id: 'string'
                - subnet_ids:
                   - 'string'
                - options:
                    ApplianceModeSupport: 'string'
                    DnsSupport: 'string'
                    Ipv6Support: 'string'
                - tags:
                    - Key: 'string'
                      Value: 'string'
    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            tgw-attach-0871e9c72becf0710:
              aws.ec2.transit_gateway_vpc_attachment.present:
                - name: tgw-attach-0871e9c72becf0710
                - resource_id: tgw-attach-0871e9c72becf0710
                - transit_gateway: tgw-02994a8dda824c337
                - vpc_id: vpc-0afa0d5fe3fc2785c
                - subnet_ids:
                   - subnet-07f91b9ebd252be49
                - options:
                    ApplianceModeSupport: disable
                    DnsSupport: enable
                    Ipv6Support: disable
                - tags:
                    - Key: Name
                      Value: test-transit-gateway-attachment

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if resource_id:
        before = await hub.tool.aws.ec2.transit_gateway_vpc_attachment.get_transit_gateway_vpc_attachment_by_id(
            ctx, resource_id
        )

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if before and before["ret"]:
        result[
            "old_state"
        ] = hub.tool.aws.ec2.conversion_utils.convert_raw_tg_vpc_attachment(
            before["ret"], name
        )

    try:
        if before and before["ret"]:
            plan_state = copy.deepcopy(result["old_state"])
            current_status = result["old_state"]["state"]
            if current_status == "available":
                if subnet_ids is not None:
                    update_ret = await hub.tool.aws.ec2.transit_gateway_vpc_attachment.update_transit_gateway_vpc_attachment(
                        ctx=ctx,
                        transit_gateway_vpc_attachment_id=resource_id,
                        old_subnets=before["ret"].get("SubnetIds"),
                        new_subnets=subnet_ids,
                        old_options=before["ret"].get("Options"),
                        new_options=options,
                    )
                    result["comment"] += update_ret["comment"]
                    result["result"] = update_ret["result"]
                    resource_updated = resource_updated or update_ret["ret"]
                    if ctx.get("test", False) and update_ret["ret"]:
                        if subnet_ids:
                            plan_state["subnet_ids"] = update_ret["ret"].get(
                                "subnet_ids"
                            )
                        if options:
                            plan_state["options"] = update_ret["ret"].get("options")
                if result["result"] and (
                    tags is not None and tags != result["old_state"].get("tags")
                ):
                    # Update tags
                    update_ret = await hub.tool.aws.ec2.tag.update_tags(
                        ctx=ctx,
                        resource_id=resource_id,
                        old_tags=before.get("Tags"),
                        new_tags=tags,
                    )
                    if not update_ret["result"]:
                        result["comment"] += update_ret["comment"]
                        result["result"] = update_ret["result"]
                    resource_updated = resource_updated or update_ret["result"]
                    if ctx.get("test", False) and update_ret["result"]:
                        plan_state["tags"] = update_ret["ret"]
                if resource_updated:
                    result["comment"] += [
                        f"'Updated aws.ec2.transit_gateway_vpc_attachment {name}'"
                    ]
                else:
                    result["comment"] += [f"no changes to update"]
            else:
                result["new_state"] = copy.deepcopy(result["old_state"])
                result["comment"] += [
                    f"aws.ec2.transit_gateway_vpc_attachment {name} is in {current_status} state"
                ]

        else:
            if ctx.get("test", False):
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state={
                        "name": name,
                        "transit_gateway": transit_gateway,
                        "vpc_id": vpc_id,
                        "subnet_ids": subnet_ids,
                        "options": options,
                        "tags": tags,
                    },
                )
                result["comment"] += [
                    f"Would create aws.ec2.transit_gateway_vpc_attachment {name}"
                ]
                return result

            ret = await hub.exec.boto3.client.ec2.create_transit_gateway_vpc_attachment(
                ctx,
                TransitGatewayId=transit_gateway,
                VpcId=vpc_id,
                SubnetIds=subnet_ids,
                Options=options,
                TagSpecifications=[
                    {
                        "ResourceType": "transit-gateway-attachment",
                        "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
                    }
                ]
                if tags
                else None,
            )

            if not ret["result"]:
                result["comment"] += ret["comment"]
                result["result"] = ret["result"]
                return result

            result["comment"] += [
                f"Created aws.ec2.transit_gateway_vpc_attachment '{name}'"
            ]
            resource_updated = resource_updated or ret["result"]
            resource_id = ret["ret"]["TransitGatewayVpcAttachment"][
                "TransitGatewayAttachmentId"
            ]

    except hub.tool.boto3.exception.ClientError as e:
        result["result"] = False
        result["comment"] += [f"{e.__class__.__name__}: {e}"]

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif resource_updated:
            after = await hub.tool.aws.ec2.transit_gateway_vpc_attachment.get_transit_gateway_vpc_attachment_by_id(
                ctx, resource_id
            )
            result[
                "new_state"
            ] = hub.tool.aws.ec2.conversion_utils.convert_raw_tg_vpc_attachment(
                after["ret"], name
            )
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """
    Deletes the specified VPC attachment.

    Args:
        name(str):
            Name of the resource.

        resource_id(str, Optional):
            AWS Transit gateway VPC attachment id. Idem automatically considers this resource being absent if this field
            is not specified.

    Request Syntax:
        .. code-block:: sls

            [transit_gateway_vpc_attachment-resource-id]:
              aws.ec2.transit_gateway_vpc_attachment.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            tgw-attach-0871e9c72becf0710
              aws.ec2.transit_gateway_vpc_attachment.absent:
                - name: tgw-attach-0871e9c72becf0710
                - resource_id: tgw-attach-0871e9c72becf0710
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] += [
            f"aws.ec2.transit_gateway_vpc_attachment '{name}' already absent"
        ]
        return result
    before = await hub.tool.aws.ec2.transit_gateway_vpc_attachment.get_transit_gateway_vpc_attachment_by_id(
        ctx, resource_id
    )
    if not before or not before["ret"]:
        result["comment"] += [
            f"aws.ec2.transit_gateway_vpc_attachment '{name}' already absent"
        ]
        return result
    before = before["ret"]
    if not before or (before["State"] and (before["State"] == "deleted")):
        result["comment"] += [
            f"aws.ec2.transit_gateway_vpc_attachment '{name}' is in deleted state."
        ]
    elif ctx.get("test", False):
        result[
            "old_state"
        ] = hub.tool.aws.ec2.conversion_utils.convert_raw_tg_vpc_attachment(
            before, name
        )
        result["comment"] += [
            f"Would delete aws.ec2.transit_gateway_vpc_attachment {name}"
        ]
        return result
    else:
        result[
            "old_state"
        ] = hub.tool.aws.ec2.conversion_utils.convert_raw_tg_vpc_attachment(
            before, name
        )
        try:
            ret = await hub.exec.boto3.client.ec2.delete_transit_gateway_vpc_attachment(
                ctx, TransitGatewayAttachmentId=resource_id
            )
            if not ret["result"]:
                result["comment"] += ret["comment"]
                result["result"] = ret["result"]
                return result
            after = await hub.tool.aws.ec2.transit_gateway_vpc_attachment.get_transit_gateway_vpc_attachment_by_id(
                ctx, resource_id
            )
            result[
                "new_state"
            ] = hub.tool.aws.ec2.conversion_utils.convert_raw_tg_vpc_attachment(
                after["ret"], name
            )
            result["comment"] += [
                f"Deleted aws.ec2.transit_gateway_vpc_attachment '{name}'"
            ]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Describes one or more VPC attachments. By default, all VPC attachments are described. Alternatively, you can
    filter the results.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.transit_gateway_vpc_attachment
    """

    result = {}

    ret = await hub.exec.boto3.client.ec2.describe_transit_gateway_vpc_attachments(ctx)
    if not ret["result"]:
        hub.log.warning(
            f"Could not describe aws.ec2.transit_gateway_vpc_attachment {ret['comment']}"
        )
        return {}
    for transit_gateway_vpc_attachment in ret["ret"]["TransitGatewayVpcAttachments"]:
        resource_id = transit_gateway_vpc_attachment.get("TransitGatewayAttachmentId")
        translated_resource = (
            hub.tool.aws.ec2.conversion_utils.convert_raw_tg_vpc_attachment(
                transit_gateway_vpc_attachment, resource_id
            )
        )
        result[resource_id] = {
            "aws.ec2.transit_gateway_vpc_attachment.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }

    return result


def is_pending(hub, ret):
    new_state = ret.get("new_state", None)
    status = None
    resource_id = None
    if new_state:
        status = new_state.get("state")
        resource_id = new_state.get("resource_id")
    if status and isinstance(status, str):
        hub.log.debug(
            f"Transit gateway VPC attachment: {resource_id} is_pending() status {status}"
        )
        if (
            status.casefold() == "available"
            or status.casefold() == "deleted"
            or status.casefold() == "failed"
            or status.casefold() == "rejected"
        ):
            hub.log.debug(
                f"No need to reconcile new state {new_state} for Transit gateway VPC attachment: {resource_id} with status {status}"
            )
            return False
        if (
            status.casefold() == "initiatingRequest"
            or status.casefold() == "pendingAcceptance"
            or status.casefold() == "rollingBack"
            or status.casefold() == "pending"
            or status.casefold() == "modifying"
            or status.casefold() == "deleting"
            or status.casefold() == "rejecting"
            or status.casefold() == "failing"
        ):
            hub.log.debug(
                f"Reconcile new state {new_state} for Transit gateway VPC attachment: {resource_id} with status {status}"
            )
            return True
    return (not ret["result"]) or bool(ret["changes"])
