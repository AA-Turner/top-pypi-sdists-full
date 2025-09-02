"""State module for managing EC2 subnets."""
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
            "aws.ec2.nat_gateway.absent",
            "aws.ec2.elastic_ip.absent",
            "aws.ec2.route_table.absent",
            "aws.eks.cluster.absent",
        ],
    },
    "present": {
        "require": [
            "aws.ec2.vpc.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    vpc_id: str,
    cidr_block: str,
    resource_id: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
    availability_zone: str = None,
    availability_zone_id: str = None,
    ipv6_cidr_block: str = None,
    outpost_arn: str = None,
    map_public_ip_on_launch: bool = None,
    assign_ipv6_address_on_creation: bool = None,
    map_customer_owned_ip_on_launch: bool = None,
    customer_owned_ipv4_pool: str = None,
    enable_dns_64: bool = None,
    private_dns_name_options_on_launch: Dict[str, Any] = None,
    enable_lni_at_device_index: int = None,
    disable_lni_at_device_index: bool = None,
) -> Dict[str, Any]:
    """Create an AWS Subnet.

    Creates a subnet in a specified VPC. You must specify an IPv4 CIDR block for the subnet. After you create a
    subnet, you can't change its CIDR block. The allowed block size is between a /16 netmask (65,536 IP addresses)
    and /28 netmask (16 IP addresses). The CIDR block must not overlap with the CIDR block of an existing subnet in
    the VPC. If you've associated an IPv6 CIDR block with your VPC, you can create a subnet with an IPv6 CIDR block
    that uses a /64 prefix length.   Amazon Web Services reserves both the first four and the last IPv4 address in
    each subnet's CIDR block. They're not available for use.  If you add more than one subnet to a VPC, they're set
    up in a star topology with a logical router in the middle. When you stop an instance in a subnet, it retains its
    private IPv4 address. It's therefore possible to have a subnet with no running instances (they're all stopped),
    but no remaining IP addresses available. For more information about subnets, see Your VPC and subnets in the
    Amazon Virtual Private Cloud User Guide.

    Args:
        name(str):
            An Idem name of the resource.

        vpc_id(str):
            ID of the VPC.

        cidr_block(str):
            The IPv4 network range for the subnet, in CIDR notation. For example, 10.0.0.0/24. We modify the
            specified CIDR block to its canonical form; for example, if you specify 100.68.0.18/18, we
            modify it to 100.68.0.0/18.

        resource_id(str, Optional):
            AWS Subnet ID.

        tags(dict or list, Optional):
            Dict in the format of {tag-key: tag-value} or List of tags in the format of
            [{"Key": tag-key, "Value": tag-value}] to associate with the subnet.
            Each tag consists of a key name and an associated value. Defaults to None.

            * Key (str):
                The key name that can be used to look up or retrieve the associated value. For example,
                Department or Cost Center are common choices.

            * Value (str):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.

        availability_zone(str, Optional):
            The Availability Zone or Local Zone for the subnet. Default: Amazon Web Services selects one for
            you. If you create more than one subnet in your VPC, we do not necessarily select a different
            zone for each subnet. To create a subnet in a Local Zone, set this value to the Local Zone ID,
            for example us-west-2-lax-1a. For information about the Regions that support Local Zones, see
            Available Regions in the Amazon Elastic Compute Cloud User Guide. To create a subnet in an
            Outpost, set this value to the Availability Zone for the Outpost and specify the Outpost ARN. Defaults to None.

        availability_zone_id(str, Optional):
            The AZ ID or the Local Zone ID of the subnet. Defaults to None.

        ipv6_cidr_block(str, Optional):
            The IPv6 network range for the subnet, in CIDR notation. The subnet size must use a /64 prefix length. Defaults to None.

        outpost_arn(str, Optional):
            The Amazon Resource Name (ARN) of the Outpost. If you specify an Outpost ARN, you must also
            specify the Availability Zone of the Outpost subnet. Defaults to None.

        map_public_ip_on_launch (bool, Optional):
            Indicates whether instances launched in this subnet receive a public IPv4 address.

        assign_ipv6_address_on_creation (bool, Optional):
            Specify true to indicate that network interfaces created in the specified subnet should be assigned an IPv6 address.
            This includes a network interface that's created when launching an instance into the subnet (the instance therefore receives an IPv6 address).

        map_customer_owned_ip_on_launch (bool, Optional):
            Specify true to indicate that network interfaces attached to instances created in the specified subnet should be assigned a customer-owned IPv4 address.

        customer_owned_ipv4_pool (str, Optional):
            The customer-owned IPv4 address pool associated with the subnet. You must set this value when you specify true for MapCustomerOwnedIpOnLaunch .

        enable_dns_64 (bool, Optional):
            Indicates whether DNS queries made to the Amazon-provided DNS Resolver in this subnet should return synthetic IPv6 addresses for IPv4-only destinations.

        enable_lni_at_device_index (int, Optional):
            Indicates the device position for local network interfaces in this subnet.

        private_dns_name_options_on_launch (dict[str, Any])
            The type of hostnames to assign to instances in the subnet at launch. An instance hostname is based on the IPv4 address or ID of the instance.

            * HostnameType (str):
                The type of hostname for EC2 instances. For IPv4 only subnets, an instance DNS name must be based on the instance IPv4 address.
                For IPv6 only subnets, an instance DNS name must be based on the instance ID. For dual-stack subnets, you can specify whether DNS names use the instance IPv4 address or the instance ID.
            * EnableResourceNameDnsARecord (bool):
                Indicates whether to respond to DNS queries for instance hostnames with DNS A records.
            * EnableResourceNameDnsAAAARecord (bool):
                Indicates whether to respond to DNS queries for instance hostname with DNS AAAA records.

        disable_lni_at_device_index (bool):
            Specify true to indicate that local network interfaces at the current position should be disabled.

    Request Syntax:
       .. code-block:: sls

          [subnet-resource-name]:
            aws.ec2.subnet.present:
              - resource_id: 'string'
              - cidr_block: 'string'
              - ipv6_cidr_block: 'string'
              - vpc_id: 'string'
              - availability_zone: 'string'
              - availability_zone_id: 'string'
              - outpost_arn: 'string'
              - map_public_ip_on_launch: bool
              - assign_ipv6_address_on_creation: bool
              - map_customer_owned_ip_on_launch: bool
              - enable_dns_64: bool
              - private_dns_name_options_on_launch:
                  EnableResourceNameDnsAAAARecord: bool
                  EnableResourceNameDnsARecord: bool
                  HostnameType: 'string'
              - tags:
                  'string': 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            my-subnet:
              aws.ec2.subnet.present:
                - vpc_id: vpc-07123af5a5zwqcc0
                - cidr_block: 10.10.10.0/28
                - availability_zone: eu-west-2c
                - tags:
                    Name: Idem-test-subnet
                - ipv6_cidr_block: 2a05:d01c:74f:7200::/64
                - map_public_ip_on_launch: true
                - assign_ipv6_address_on_creation: false
                - map_customer_owned_ip_on_launch: false
                - enable_dns_64: false
                - private_dns_name_options_on_launch:
                    EnableResourceNameDnsAAAARecord: false
                    EnableResourceNameDnsARecord: false
                    HostnameType: ip-name
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    before = None

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if resource_id:
        before = await hub.exec.aws.ec2.subnet.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.ec2.subnet", name=resource_id
        )
        # Update ipv6 cidr block
        ipv6_cidr_block_association_set = (
            hub.tool.aws.network_utils.get_associated_ipv6_cidr_blocks(
                before["ret"].get("Ipv6CidrBlockAssociationSet")
            )
        )
        if ipv6_cidr_block != (
            None
            if not ipv6_cidr_block_association_set
            else ipv6_cidr_block_association_set[0]
        ):
            update_ret = await hub.tool.aws.ec2.subnet.update_ipv6_cidr_blocks(
                ctx=ctx,
                subnet_id=before["ret"]["resource_id"],
                old_ipv6_cidr_block=None
                if not ipv6_cidr_block_association_set
                else ipv6_cidr_block_association_set[0],
                new_ipv6_cidr_block={"Ipv6CidrBlock": ipv6_cidr_block}
                if ipv6_cidr_block
                else None,
            )
            result["result"] = result["result"] and update_ret["result"]
            result["comment"] += update_ret["comment"]
            resource_updated = True
            if ctx.get("test", False) and update_ret["ret"] is not None:
                plan_state["ipv6_cidr_block"] = update_ret["ret"].get("ipv6_cidr_block")
        if tags is not None and tags != result["old_state"].get("tags"):
            # Update tags
            update_ret = await hub.tool.aws.ec2.tag.update_tags(
                ctx=ctx,
                resource_id=before["ret"]["resource_id"],
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )
            result["comment"] += update_ret["comment"]
            result["result"] = result["result"] and update_ret["result"]
            resource_updated = resource_updated or update_ret["result"]
            if ctx.get("test", False) and update_ret["result"]:
                plan_state["tags"] = update_ret["ret"]
        if resource_updated:
            if ctx.get("test", False):
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.ec2.subnet", name=name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.ec2.subnet", name=name
                )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "availability_zone": availability_zone,
                    "availability_zone_id": availability_zone_id,
                    "cidr_block": cidr_block,
                    "ipv6_cidr_block": ipv6_cidr_block,
                    "outpost_arn": outpost_arn,
                    "vpc_id": vpc_id,
                    "tags": tags,
                    "map_public_ip_on_launch": map_public_ip_on_launch,
                    "assign_ipv6_address_on_creation": assign_ipv6_address_on_creation,
                    "map_customer_owned_ip_on_launch": map_customer_owned_ip_on_launch,
                    "customer_owned_ipv4_pool": customer_owned_ipv4_pool,
                    "enable_dns_64": enable_dns_64,
                    "private_dns_name_options_on_launch": private_dns_name_options_on_launch,
                    "enable_lni_at_device_index": enable_lni_at_device_index,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ec2.subnet", name=name
            )
            return result
        ret = await hub.exec.boto3.client.ec2.create_subnet(
            ctx,
            **{
                "TagSpecifications": [
                    {
                        "ResourceType": "subnet",
                        "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
                    }
                ]
                if tags
                else None,
                "AvailabilityZone": availability_zone,
                "AvailabilityZoneId": availability_zone_id,
                "Ipv6CidrBlock": ipv6_cidr_block,
                "OutpostArn": outpost_arn,
                "VpcId": vpc_id,
                "CidrBlock": cidr_block,
            },
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.ec2.subnet", name=name
        )
        result[
            "new_state"
        ] = hub.tool.aws.ec2.conversion_utils.convert_raw_subnet_to_present(
            raw_resource=ret["ret"]["Subnet"], idem_resource_name=name
        )
        resource_id = result["new_state"]["resource_id"]

    if not before:
        new_res = result["new_state"]
    else:
        new_res = before["ret"]
    update_ret = await hub.tool.aws.ec2.subnet.update_subnet_attributes(
        ctx,
        before=new_res,
        resource_id=resource_id,
        map_public_ip_on_launch=map_public_ip_on_launch,
        assign_ipv6_address_on_creation=assign_ipv6_address_on_creation,
        map_customer_owned_ip_on_launch=map_customer_owned_ip_on_launch,
        customer_owned_ipv4_pool=customer_owned_ipv4_pool,
        enable_dns_64=enable_dns_64,
        private_dns_name_options_on_launch=private_dns_name_options_on_launch,
        enable_lni_at_device_index=enable_lni_at_device_index,
        disable_lni_at_device_index=disable_lni_at_device_index,
    )
    result["comment"] += update_ret["comment"]
    result["result"] = result["result"] and update_ret["result"]
    resource_updated = resource_updated or bool(update_ret["ret"])
    if update_ret["ret"] and ctx.get("test", False):
        plan_state.update(update_ret["ret"])

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not before) or resource_updated:
        after = await hub.exec.aws.ec2.subnet.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not after["result"] or not after["ret"]:
            result["result"] = False
            result["comment"] = after["comment"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the specified Subnet.

    You must terminate all running instances in the subnet before you can delete the subnet.

    Args:
        name(str): The Idem name of the subnet.
        resource_id(str, Optional): AWS Subnet ID. Idem automatically considers this resource being absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            [subnet-resource-id]:
              aws.ec2.subnet.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.ec2.subnet.absent:
                - name: idem-test-subnet
                - resource_id: Subnet123
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.subnet", name=name
        )
        return result

    before = await hub.exec.boto3.client.ec2.describe_subnets(
        ctx, SubnetIds=[resource_id]
    )
    if not before["result"]:
        if "InvalidSubnetID.NotFound" in str(before["comment"]):
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.ec2.subnet", name=name
            )
        else:
            result["comment"] = before["comment"]
            result["result"] = False
        return result
    if not before["ret"].get("Subnets"):
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.subnet", name=name
        )
    elif ctx.get("test", False):
        result[
            "old_state"
        ] = hub.tool.aws.ec2.conversion_utils.convert_raw_subnet_to_present(
            raw_resource=before["ret"]["Subnets"][0], idem_resource_name=name
        )
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.ec2.subnet", name=name
        )
        return result
    else:
        result[
            "old_state"
        ] = hub.tool.aws.ec2.conversion_utils.convert_raw_subnet_to_present(
            raw_resource=before["ret"]["Subnets"][0], idem_resource_name=name
        )
        try:
            ret = await hub.exec.boto3.client.ec2.delete_subnet(
                ctx, SubnetId=resource_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.ec2.subnet", name=name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Gets information about the AWS Subnets

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.subnet
    """
    result = {}
    ret = await hub.exec.boto3.client.ec2.describe_subnets(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe Subnets {ret['comment']}")
        return {}

    for subnet in ret["ret"]["Subnets"]:
        subnet_id = subnet.get("SubnetId")
        resource_translated = (
            hub.tool.aws.ec2.conversion_utils.convert_raw_subnet_to_present(
                raw_resource=subnet, idem_resource_name=subnet_id
            )
        )
        result[subnet_id] = {
            "aws.ec2.subnet.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
