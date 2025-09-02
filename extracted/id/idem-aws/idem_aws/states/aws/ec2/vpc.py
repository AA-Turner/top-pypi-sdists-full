"""State module for managing EC2 Virtual Private Gateways."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource", "allow_sync_sls_name_and_name_tag"]
TREQ = {
    "absent": {
        "require": [
            "aws.ec2.subnet.absent",
            "aws.ec2.security_group.absent",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    cidr_block_association_set: List[
        make_dataclass(
            "CidrBlockAssociationSet",
            [
                ("CidrBlock", str, field(default=None)),
                ("Ipv4IpamPoolId", str, field(default=None)),
                ("Ipv4NetmaskLength", int, field(default=None)),
            ],
        )
    ] = None,
    ipv6_cidr_block_association_set: List[
        make_dataclass(
            "Ipv6CidrBlockAssociationSet",
            [
                ("Ipv6CidrBlock", str, field(default=None)),
                ("Ipv6IpamPoolId", str, field(default=None)),
                ("Ipv6NetmaskLength", int, field(default=None)),
                ("Ipv6CidrBlockNetworkBorderGroup", str, field(default=None)),
                ("AmazonProvidedIpv6CidrBlock", bool, field(default=False)),
            ],
        )
    ] = None,
    instance_tenancy: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
    enable_dns_hostnames: bool = None,
    enable_dns_support: bool = None,
) -> Dict[str, Any]:
    """
    Creates a VPC with the specified IPv4 CIDR block. The smallest VPC you can create uses a /28 netmask (16 IPv4
    addresses), and the largest uses a /16 netmask (65,536 IPv4 addresses). For more information about how large to
    make your VPC, see Your VPC and subnets in the Amazon Virtual Private Cloud User Guide. You can optionally
    request an IPv6 CIDR block for the VPC. You can request an Amazon-provided IPv6 CIDR block from Amazon's pool of
    IPv6 addresses, or an IPv6 CIDR block from an IPv6 address pool that you provisioned through bring your own IP
    addresses (BYOIP). By default, each instance you launch in the VPC has the default DHCP options, which include
    only a default DNS server that we provide (AmazonProvidedDNS). For more information, see DHCP options sets in
    the Amazon Virtual Private Cloud User Guide. You can specify the instance tenancy value for the VPC when you
    create it. You can't change this value for the VPC after you create it. For more information, see Dedicated
    Instances in the Amazon Elastic Compute Cloud User Guide.

    Args:
        name (str): An Idem name of the resource.
        resource_id (str, Optional): AWS VPC ID
        cidr_block_association_set(List, Optional): Information about the IPv4 CIDR blocks associated with the VPC.
            Defaults to None.
            * CidrBlock (str) -- An IPv4 CIDR block to associate with the VPC.
            * Ipv4IpamPoolId (str) -- Associate a CIDR allocated from an IPv4 IPAM pool to a VPC.
            * Ipv4NetmaskLength (int) -- The netmask length of the IPv4 CIDR you would like to associate from an Amazon VPC IP Address Manager (IPAM) pool.
        ipv6_cidr_block_association_set (List, Optional): Information about the IPv6 CIDR blocks associated with the VPC.
            Defaults to None.
            * Ipv6CidrBlock (str) -- An IPv6 CIDR block from the IPv6 address pool. You must also specify Ipv6Pool in the request.
            * Ipv6IpamPoolId (str) -- Associates a CIDR allocated from an IPv6 IPAM pool to a VPC.
            * Ipv6NetmaskLength (int) -- The netmask length of the IPv6 CIDR you would like to associate from an
                Amazon VPC IP Address Manager (IPAM) pool.
            * Ipv6CidrBlockNetworkBorderGroup (str) -- The name of the location from which we advertise the IPV6 CIDR
                block. Use this parameter to limit the CIDR block to this location. You must set AmazonProvidedIpv6CidrBlock
                to true to use this parameter. You can have one IPv6 CIDR block association per network border group.
            * AmazonProvidedIpv6CidrBlock (boolean) -- Requests an Amazon-provided IPv6 CIDR block with a /56 prefix
                length for the VPC. You cannot specify the range of IPv6 addresses, or the size of the CIDR block.
        instance_tenancy (str, Optional): The tenancy options for instances launched into the VPC. For default, instances are launched
            with shared tenancy by default. You can launch instances with any tenancy into a shared tenancy
            VPC. For dedicated, instances are launched as dedicated tenancy instances by default. You can
            only launch instances with a tenancy of dedicated or host into a dedicated tenancy VPC.
            Important: The host value cannot be used with this parameter. Use the default or dedicated
            values only. Default: default. Defaults to None.
        tags (Dict or List, Optional): Dict in the format of {tag-key: tag-value} or List of tags in the format of
            [{"Key": tag-key, "Value": tag-value}] to associate with the VPC.
            Each tag consists of a key name and an associated value. Defaults to None.
            * Key (str, Optional): The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.
            * Value(str, Optional): The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.
        enable_dns_hostnames (bool, Optional): Indicates whether the instances launched in the VPC get DNS hostnames. If enabled, instances
            in the VPC get DNS hostnames; otherwise, they do not. You cannot modify the DNS resolution and DNS hostnames attributes in the same request.
            Use separate requests for each attribute. You can only enable DNS hostnames if you've enabled DNS support.
        enable_dns_support (bool, Optional): Indicates whether the DNS resolution is supported for the VPC. If enabled, queries to the Amazon provided
            DNS server at the 169.254.169.253 IP address, or the reserved IP address at the base of the VPC network range "plus two" succeed. If disabled,
            the Amazon provided DNS service in the VPC that resolves public DNS hostnames to IP addresses is not enabled. You cannot modify the DNS resolution
            and DNS hostnames attributes in the same request. Use separate requests for each attribute.

    Request Syntax:
        [vpc-resource-id]:
          aws.ec2.vpc.present:
          - resource_id: 'string'
          - cidr_block_association_set:
            - CidrBlock: 'string'
              Ipv4IpamPoolId: 'string'
              Ipv4NetmaskLength: 'integer'
          - ipv6_cidr_block_association_set:
            - Ipv6CidrBlock: 'string'
              Ipv6IpamPoolId: 'string'
              Ipv6NetmaskLength: 'integer'
              Ipv6CidrBlockNetworkBorderGroup: 'string'
              AmazonProvidedIpv6CidrBlock: True|False
          - instance_tenancy: 'default'|'dedicated'|'host'
          - tags:
            - Key: 'string'
              Value: 'string'
          - enable_dns_support: 'Boolean'
          - enable_dns_hostnames: 'Boolean'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            vpc-01234672f3336db8:
              aws.ec2.vpc.present:
              - cidr_block_association_set:
                - CidrBlock: 10.1.150.0/28
              - instance_tenancy: default
              - enable_dns_support: True
              - enable_dns_hostnames: False
              - tags:
                - Key: Name
                  Value: vpc-name
                - Key: vpc-tag-key-2
                  Value: vpc-tag-value-2
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    cidr_block_association_set = copy.deepcopy(cidr_block_association_set)
    ipv6_cidr_block_association_set = copy.deepcopy(ipv6_cidr_block_association_set)
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
    if resource_id:
        before = await hub.exec.aws.ec2.vpc.get(ctx, name=name, resource_id=resource_id)
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.ec2.vpc", name=resource_id
        )
        # Update cidr blocks
        update_ret = await hub.tool.aws.ec2.vpc.update_cidr_blocks(
            ctx=ctx,
            vpc_id=result["old_state"]["resource_id"],
            old_ipv4_cidr_blocks=result["old_state"].get(
                "cidr_block_association_set", []
            ),
            old_ipv6_cidr_blocks=result["old_state"].get(
                "ipv6_cidr_block_association_set", []
            ),
            new_ipv4_cidr_blocks=cidr_block_association_set,
            new_ipv6_cidr_blocks=ipv6_cidr_block_association_set,
        )
        result["comment"] += update_ret["comment"]
        result["result"] = update_ret["result"]
        resource_updated = resource_updated or bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            if update_ret["ret"].get("cidr_block_association_set") is not None:
                plan_state["cidr_block_association_set"] = update_ret["ret"].get(
                    "cidr_block_association_set"
                )
            if update_ret["ret"].get("ipv6_cidr_block_association_set") is not None:
                plan_state["ipv6_cidr_block_association_set"] = update_ret["ret"].get(
                    "ipv6_cidr_block_association_set"
                )
        # modify vpc attribute if the old and new attributes are not same
        if enable_dns_hostnames is not None or enable_dns_support is not None:
            update_ret = await hub.tool.aws.ec2.vpc.update_vpc_attributes(
                ctx,
                enable_dns_hostnames,
                enable_dns_support,
                result["old_state"].get("enable_dns_hostnames"),
                result["old_state"].get("enable_dns_support"),
                resource_id,
            )
            result["comment"] += update_ret["comment"]
            result["result"] = result["result"] and update_ret["result"]
            resource_updated = resource_updated or bool(update_ret["ret"])
            if update_ret["ret"] and ctx.get("test", False):
                if enable_dns_support is not None:
                    plan_state["enable_dns_support"] = enable_dns_support
                if enable_dns_hostnames is not None and enable_dns_support:
                    plan_state["enable_dns_hostnames"] = enable_dns_hostnames
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
            resource_updated = resource_updated or bool(update_ret["ret"])
            if ctx.get("test", False) and update_ret["result"]:
                plan_state["tags"] = update_ret["ret"]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "cidr_block_association_set": cidr_block_association_set,
                    "ipv6_cidr_block_association_set": ipv6_cidr_block_association_set,
                    "instance_tenancy": instance_tenancy,
                    "tags": tags,
                    "enable_dns_hostnames": enable_dns_hostnames,
                    "enable_dns_support": enable_dns_support,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ec2.vpc", name=name
            )
            return result
        cidr_request_payload = {}
        # Since boto3 only allows one cidr association when creating a vpc, we use the first cidr associations
        # during vpc creation, associate the rest after creation.
        if cidr_block_association_set:
            cidr_request_payload = (
                hub.tool.aws.network_utils.generate_cidr_request_payload_for_vpc(
                    cidr_block_association_set[0], "ipv4"
                )
            )
            cidr_block_association_set.pop(0)
        elif ipv6_cidr_block_association_set:
            cidr_request_payload = (
                hub.tool.aws.network_utils.generate_cidr_request_payload_for_vpc(
                    ipv6_cidr_block_association_set[0], "ipv6"
                )
            )
            ipv6_cidr_block_association_set.pop(0)

        ret = await hub.exec.boto3.client.ec2.create_vpc(
            ctx,
            InstanceTenancy=instance_tenancy,
            TagSpecifications=[
                {
                    "ResourceType": "vpc",
                    "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
                }
            ]
            if tags
            else None,
            **cidr_request_payload,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        resource_id = ret["ret"]["Vpc"]["VpcId"]
        # This makes sure the created VPC is saved to esm regardless if the subsequent update call fails or not.
        result["new_state"] = {"name": name, "resource_id": resource_id}
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.ec2.vpc", name=name
        )
        # Associate the rest cidr associations
        update_ret = await hub.tool.aws.ec2.vpc.update_cidr_blocks(
            ctx=ctx,
            vpc_id=resource_id,
            old_ipv4_cidr_blocks=[],
            old_ipv6_cidr_blocks=[],
            new_ipv4_cidr_blocks=cidr_block_association_set,
            new_ipv6_cidr_blocks=ipv6_cidr_block_association_set,
        )
        result["comment"] += update_ret["comment"]
        result["result"] = result["result"] and update_ret["result"]

        # modify vpc attribute if the old and new attributes are not same
        if enable_dns_hostnames is not None or enable_dns_support is not None:
            update_ret = await hub.tool.aws.ec2.vpc.update_vpc_attributes(
                ctx, enable_dns_hostnames, enable_dns_support, None, None, resource_id
            )
            result["comment"] += update_ret["comment"]
            result["result"] = result["result"] and update_ret["result"]

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not result["old_state"]) or resource_updated:
            after = await hub.exec.aws.ec2.vpc.get(
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
    """
    **Autogenerated function**

    Deletes the specified VPC. You must detach or delete all gateways and resources that are associated with the VPC
    before you can delete it. For example, you must terminate all instances running in the VPC, delete all security
    groups associated with the VPC (except the default one), delete all route tables associated with the VPC (except
    the default one), and so on.

    Args:
        name(str): The Idem name of the VPC.
        resource_id(str, Optional): AWS VPC ID. Idem automatically considers this resource being absent if this field is not specified.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            vpc-01234672f3336db8:
              aws.ec2.vpc.absent:
                - resource_id: value
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.vpc", name=name
        )
        return result
    before = await hub.exec.aws.ec2.vpc.get(ctx=ctx, name=name, resource_id=resource_id)
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.vpc", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.ec2.vpc", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.ec2.delete_vpc(ctx, VpcId=resource_id)
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.ec2.vpc", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    result = {}
    ret = await hub.exec.boto3.client.ec2.describe_vpcs(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe VPCs {ret['comment']}")
        return {}

    for resource in ret["ret"]["Vpcs"]:
        resource_id = resource.get("VpcId")
        resource_translated = (
            await hub.tool.aws.ec2.conversion_utils.convert_raw_vpc_to_present_async(
                ctx, raw_resource=resource, idem_resource_name=resource_id
            )
        )
        result[resource_id] = {
            "aws.ec2.vpc.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
