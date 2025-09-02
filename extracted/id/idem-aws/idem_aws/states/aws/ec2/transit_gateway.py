"""
State module for managing EC2 Transit gateway
"""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]
TREQ = {
    "absent": {
        "require": [
            "aws.ec2.transit_gateway_vpc_attachment.absent",
        ],
    },
}

__reconcile_wait__ = {"static": {"wait_in_seconds": 60}}


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    description: str = None,
    options: make_dataclass(
        "TransitGatewayRequestOptions",
        [
            ("AmazonSideAsn", int, field(default=None)),
            ("AutoAcceptSharedAttachments", str, field(default=None)),
            ("DefaultRouteTableAssociation", str, field(default=None)),
            ("DefaultRouteTablePropagation", str, field(default=None)),
            ("VpnEcmpSupport", str, field(default=None)),
            ("DnsSupport", str, field(default=None)),
            ("MulticastSupport", str, field(default=None)),
            ("TransitGatewayCidrBlocks", List[str], field(default=None)),
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
    """Creates a transit gateway.

    You can use a transit gateway to interconnect your virtual private clouds (VPC) and on-premises networks. After the
    transit gateway enters the available state, you can attach your VPCs and VPN connections to the transit gateway. To
    attach your VPCs, use CreateTransitGatewayVpcAttachment. To attach a VPN connection, use CreateCustomerGateway to
    create a customer gateway and specify the ID of the customer gateway and the ID of the transit gateway in a call to
    CreateVpnConnection.

    When you create a transit gateway, we create a default transit gateway route table and use it as the default
    association route table and the default propagation route table. You can use CreateTransitGatewayRouteTable to create
    additional transit gateway route tables. If you disable automatic route propagation, we do not create a default
    transit gateway route table. You can use EnableTransitGatewayRouteTablePropagation to propagate routes from a resource
    attachment to a transit gateway route table. If you disable automatic associations, you can use
    AssociateTransitGatewayRouteTable to associate a resource attachment with a transit gateway route table.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            AWS Transit gateway id.

        description(str, Optional):
            description for the transit gateway to identify the resource

        options(dict[str, Any], Optional):
            The transit gateway options. Defaults to None.

            * AmazonSideAsn (int, Optional):
                A private Autonomous System Number (ASN) for the Amazon side of a BGP session. The range is
                64512 to 65534 for 16-bit ASNs and 4200000000 to 4294967294 for 32-bit ASNs. The default is
                64512.

            * AutoAcceptSharedAttachments (str, Optional):
                Enable or disable automatic acceptance of attachment requests. Disabled by default.

            * DefaultRouteTableAssociation (str, Optional):
                Enable or disable automatic association with the default association route table. Enabled by
                default.

            * DefaultRouteTablePropagation (str, Optional):
                Enable or disable automatic propagation of routes to the default propagation route table.
                Enabled by default.

            * VpnEcmpSupport (str, Optional):
                Enable or disable Equal Cost Multipath Protocol support. Enabled by default.

            * DnsSupport (str, Optional):
                Enable or disable DNS support. Enabled by default.

            * MulticastSupport (str, Optional):
                Indicates whether multicast is enabled on the transit gateway

            * TransitGatewayCidrBlocks (list[str], Optional):
                One or more IPv4 or IPv6 CIDR blocks for the transit gateway. Must be a size /24 CIDR block or
                larger for IPv4, or a size /64 CIDR block or larger for IPv6.

        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of ``[{"Key": tag-key, "Value": tag-value}]``
            to associate with the transit gateway. Each tag consists of a key name and an associated value. Defaults to None.

            * Key (str, Optional):
                The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.

            * Value (str, Optional):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.

    Request Syntax:
        .. code-block:: sls

            [transit-gateway-resource-name]:
              aws.ec2.transit_gateway.present:
                - resource_id: 'string'
                - description: 'string'
                - options:
                    AmazonSideAsn: 'int'
                    AutoAcceptSharedAttachments: 'string'
                    DefaultRouteTableAssociation: 'string'
                    DefaultRouteTablePropagation: 'string'
                    VpnEcmpSupport: 'string'
                    DnsSupport: 'string'
                    MulticastSupport: 'string'
                    TransitGatewayCidrBlocks:
                      - 'string'
                      - 'string'
                - tags:
                  - Key: 'string'
                    Value: 'string'
    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            tgw-02994a8dda824c337:
              aws.ec2.transit_gateway.present:
                - resource_id: tgw-02994a8dda824c337
                - description: test transit gateway
                - options:
                    AmazonSideAsn: 64512
                    AutoAcceptSharedAttachments: enable
                    DefaultRouteTableAssociation: enable
                    DefaultRouteTablePropagation: enable
                    DnsSupport: enable
                    MulticastSupport: disable
                    TransitGatewayCidrBlocks:
                    - 10.0.0.0/24
                    - 198.0.0.0/16
                    VpnEcmpSupport: enable
                - tags:
                  - Key: BU
                    Value: vRA-CS-GR
                  - Key: Organization
                    Value: vmw
                  - Key: Name
                    Value: transit-gateway-2

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if resource_id:
        before = await hub.tool.aws.ec2.transit_gateway.get_transit_gateway_by_id(
            ctx, resource_id
        )
        if not before["result"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
    try:
        if before and before["ret"]:
            result[
                "old_state"
            ] = hub.tool.aws.ec2.conversion_utils.convert_raw_transit_gateway_to_present(
                raw_resource=before["ret"], idem_resource_name=name
            )
            plan_state = copy.deepcopy(result["old_state"])
            current_status = result["old_state"]["state"]
            if current_status == "available":
                update_ret = await hub.tool.aws.ec2.transit_gateway.update_options(
                    ctx=ctx,
                    transit_gateway_id=result["old_state"].get("resource_id"),
                    old_description=result["old_state"].get("description"),
                    new_description=description,
                    old_options=result["old_state"].get("options"),
                    new_options=options,
                )
                result["comment"] = update_ret["comment"]
                result["result"] = update_ret["result"]
                resource_updated = resource_updated or bool(update_ret["ret"])

                if update_ret["ret"] is not None and ctx.get("test", False):
                    if update_ret["ret"].get("options") is not None:
                        plan_state["options"] = update_ret["ret"].get("options")
                    if update_ret["ret"].get("description") is not None:
                        plan_state["description"] = update_ret["ret"].get("description")

                hub.tool.aws.tag_utils.convert_tag_dict_to_list(
                    result["old_state"].get("tags")
                )

                if tags is not None and tags != result["old_state"].get("tags"):
                    # Update tags
                    update_ret = await hub.tool.aws.ec2.tag.update_tags(
                        ctx=ctx,
                        resource_id=result["old_state"].get("resource_id"),
                        old_tags=result["old_state"].get("tags"),
                        new_tags=tags,
                    )
                    result["comment"] += update_ret["comment"]
                    result["result"] = result["result"] and update_ret["result"]
                    resource_updated = resource_updated or update_ret["result"]
                    if ctx.get("test", False) and update_ret["ret"] is not None:
                        plan_state["tags"] = update_ret["ret"]
            else:
                result["new_state"] = copy.deepcopy(result["old_state"])
                result["comment"] += [
                    f"aws.ec2.transit_gateway {name} is in {current_status} state"
                ]
        else:
            if ctx.get("test", False):
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state={
                        "name": name,
                        "description": description,
                        "options": options,
                        "tags": tags,
                    },
                )
                result["comment"] += [f"Would create aws.ec2.transit_gateway {name}"]
                return result
            ret = await hub.exec.boto3.client.ec2.create_transit_gateway(
                ctx,
                Description=description,
                Options=options,
                TagSpecifications=[
                    {
                        "ResourceType": "transit-gateway",
                        "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
                    }
                ]
                if tags
                else None,
            )

            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                return result

            resource_id = ret["ret"]["TransitGateway"]["TransitGatewayId"]
            result["comment"] += [f"Created '{resource_id}'"]
    except hub.tool.boto3.exception.ClientError as e:
        result["result"] = False
        result["comment"] += [f"{e.__class__.__name__}: {e}"]

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.tool.aws.ec2.transit_gateway.get_transit_gateway_by_id(
                ctx, resource_id
            )
            result[
                "new_state"
            ] = hub.tool.aws.ec2.conversion_utils.convert_raw_transit_gateway_to_present(
                raw_resource=after["ret"], idem_resource_name=name
            )
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """
    Deletes the specified transit gateway.

    Args:
        name(str):
            An Idem name of the transit gateway.

        resource_id(str, Optional):
            AWS Transit gateway id. Idem automatically considers this resource being absent if this field is not specified.

    Returns:
        Dict[str, Any]

    Request Syntax:
        .. code-block:: sls

            [transit-gateway-resource-name]:
              aws.ec2.transit_gateway.absent:
                - name: 'string'
                - resource_id: 'string'


    Examples:
        .. code-block:: sls

            tgw-02994a8dda824c337:
              aws.ec2.transit_gateway.absent:
                - name: value
                - resource_id: tgw-02994a8dda824c337
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.transit_gateway", name=name
        )
        return result
    before = await hub.tool.aws.ec2.transit_gateway.get_transit_gateway_by_id(
        ctx, resource_id
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    before = before["ret"]
    if not before:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.transit_gateway", name=name
        )
    elif before["State"] == "deleted":
        result["comment"] += [f"aws.ec2.transit_gateway '{name}' is in deleted state."]
    else:
        result[
            "old_state"
        ] = hub.tool.aws.ec2.conversion_utils.convert_raw_transit_gateway_to_present(
            raw_resource=before, idem_resource_name=name
        )
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.ec2.transit_gateway", name=name
            )
            return result
        try:
            ret = await hub.exec.boto3.client.ec2.delete_transit_gateway(
                ctx, TransitGatewayId=resource_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                result["result"] = False
                return result
            after = await hub.tool.aws.ec2.transit_gateway.get_transit_gateway_by_id(
                ctx, resource_id
            )
            result[
                "new_state"
            ] = hub.tool.aws.ec2.conversion_utils.convert_raw_transit_gateway_to_present(
                raw_resource=after["ret"], idem_resource_name=name
            )
            result["comment"] += [f"Deleted aws.ec2.transit_gateway '{name}'"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Describes one or more transit gateways. By default, all transit gateways are described. Alternatively, you can
    filter the results.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.transit_gateway
    """

    result = {}

    ret = await hub.exec.boto3.client.ec2.describe_transit_gateways(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe transit_gateway {ret['comment']}")
        return result
    for resource in ret["ret"]["TransitGateways"]:
        resource_id = resource.get("TransitGatewayId")
        resource_translated = (
            hub.tool.aws.ec2.conversion_utils.convert_raw_transit_gateway_to_present(
                raw_resource=resource, idem_resource_name=resource_id
            )
        )
        result[resource_id] = {
            "aws.ec2.transit_gateway.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
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
        hub.log.debug(f"Transit gateway: {resource_id} is_pending() status {status}")
        if status.casefold() == "available" or status.casefold() == "deleted":
            hub.log.debug(
                f"No need to reconcile new state {new_state} for Transit gateway: {resource_id} with status {status}"
            )
            return False
        if (
            status.casefold() == "pending"
            or status.casefold() == "modifying"
            or status.casefold() == "deleting"
        ):
            hub.log.debug(
                f"Reconcile new state {new_state} for Transit gateway: {resource_id} with status {status}"
            )
            return True
    return (not ret["result"]) or bool(ret["changes"])
